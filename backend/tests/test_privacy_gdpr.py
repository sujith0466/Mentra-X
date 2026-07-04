import pytest
from datetime import datetime, timezone, timedelta
from flask import Flask
from backend.models import db, User, UserConsent, PrivacyAuditLog, Enrollment, QuizAttempt, StudentTwinRecord, AssessmentSession, Course, Domain, Quiz
from backend.services.privacy import ConsentService, PrivacyService, require_consent, has_consent
from backend.services.memory.memory_facade import MemoryFacade
from backend.services.orchestration.runtime.workflow_store import WorkflowStore
from backend.app import app as flask_app

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    with flask_app.app_context():
        db.create_all()
        try:
            from backend.models import ensure_privacy_schema
            ensure_privacy_schema(db.session)
        except Exception:
            pass
        yield flask_app
        try:
            db.session.rollback()
            # Clean up created test data cleanly without dropping schema tables
            UserConsent.query.delete()
            PrivacyAuditLog.query.delete()
            AssessmentSession.query.filter(AssessmentSession.session_id.in_(["old-gdpr-1", "rec-gdpr-1"])).delete()
            users = User.query.filter((User.email.like("%@gdpr.test")) | (User.email.like("%@mentra.research"))).all()
            for u in users:
                Enrollment.query.filter_by(user_id=u.id).delete()
                QuizAttempt.query.filter_by(user_id=u.id).delete()
                StudentTwinRecord.query.filter_by(user_id=u.id).delete()
                db.session.delete(u)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

@pytest.fixture
def client(app):
    return app.test_client()

import uuid

@pytest.fixture
def sample_user(app):
    user = User(
        name="Test Student",
        email="student@gdpr.test",
        password="pass",
        role="student",
        referral_code=f"GDPR_{uuid.uuid4().hex[:6]}"
    )
    db.session.add(user)
    db.session.commit()
    return user

def test_consent_service(app, sample_user):
    # Check default consent
    assert ConsentService.get_user_consent(sample_user.id, "AI_TUTORING") == "GRANTED"
    
    # Revoke consent
    res = ConsentService.update_user_consent(sample_user.id, "AI_TUTORING", "REVOKED", ip_address="127.0.0.1")
    assert res["status"] == "REVOKED"
    assert ConsentService.get_user_consent(sample_user.id, "AI_TUTORING") == "REVOKED"
    
    # Check all consents
    all_consents = ConsentService.get_all_consents(sample_user.id)
    assert all_consents["AI_TUTORING"] == "REVOKED"
    assert all_consents["SEMANTIC_MEMORY_STORAGE"] == "GRANTED"
    
    # Verify audit log created
    logs = PrivacyAuditLog.query.filter_by(user_id=sample_user.id).all()
    assert len(logs) >= 1
    assert any(l.action == "CONSENT_UPDATED" for l in logs)

def test_privacy_middleware_routes(client, sample_user):
    # 1. With default consent (GRANTED)
    res = client.get(f"/api/privacy/test-protected?user_id={sample_user.id}")
    assert res.status_code == 200
    assert res.data == b"Access Granted"

    # 2. After revoking consent
    ConsentService.update_user_consent(sample_user.id, "AI_TUTORING", "REVOKED")
    res2 = client.get(f"/api/privacy/test-protected?user_id={sample_user.id}")
    assert res2.status_code == 403
    assert "Consent Revoked" in res2.get_json()["error"]

def test_privacy_middleware_tools(app, sample_user):
    @require_consent("SEMANTIC_MEMORY_STORAGE")
    def tool_function(user_id: int, data: str):
        return f"Stored: {data}"

    # 1. GRANTED
    assert tool_function(user_id=sample_user.id, data="test") == "Stored: test"

    # 2. REVOKED
    ConsentService.update_user_consent(sample_user.id, "SEMANTIC_MEMORY_STORAGE", "REVOKED")
    res = tool_function(user_id=sample_user.id, data="test")
    assert "[PRIVACY BYPASS]" in res

def test_memory_facade_consent_bypass(app, sample_user, mocker):
    facade = MemoryFacade()
    upsert_mock = mocker.patch.object(facade.mutator, "upsert_learning_dna", return_value=True)

    # 1. GRANTED - calls mutator
    facade.store_learning_dna(sample_user.id, "1.0", "Visual learner")
    assert upsert_mock.call_count == 1

    # 2. REVOKED - skips mutator
    ConsentService.update_user_consent(sample_user.id, "SEMANTIC_MEMORY_STORAGE", "REVOKED")
    facade.store_learning_dna(sample_user.id, "1.0", "Auditory learner")
    assert upsert_mock.call_count == 1 # unchanged

def _get_or_create_course_and_quiz():
    course = Course.query.first()
    if not course:
        domain = Domain.query.first()
        if not domain:
            domain = Domain(name="GDPR Domain", description="Test Domain")
            db.session.add(domain)
            db.session.flush()
        course = Course(title="GDPR Course", description="Test", domain_id=domain.id, price=0.0, instructor="QA", status="published")
        db.session.add(course)
        db.session.commit()
    quiz = Quiz.query.first()
    if not quiz:
        quiz = Quiz(course_id=course.id, title="GDPR Quiz", description="Test", question_count_target=1, passing_percentage=60.0, time_limit_minutes=10)
        db.session.add(quiz)
        db.session.commit()
    return course, quiz

def test_export_user_data(app, sample_user):
    course, quiz = _get_or_create_course_and_quiz()
    # Add enrollment and quiz attempt
    e = Enrollment(user_id=sample_user.id, course_id=course.id, progress=50.0)
    qa = QuizAttempt(user_id=sample_user.id, quiz_id=quiz.id, score_percentage=85.0, passed=True)
    twin = StudentTwinRecord(user_id=sample_user.id, twin_version=1, learning_dna="visual")
    db.session.add_all([e, qa, twin])
    db.session.commit()

    # Add workflow history
    WorkflowStore().clear()
    WorkflowStore().create_workflow("wf-export-1", "TutorAgent")
    WorkflowStore().update_workflow("wf-export-1", {"user_id": sample_user.id})

    bundle = PrivacyService.export_user_data(sample_user.id)
    assert bundle["user_profile"]["email"] == "student@gdpr.test"
    assert len(bundle["enrollments"]) >= 1
    assert len(bundle["quiz_attempts"]) >= 1
    assert len(bundle["digital_twin"]) >= 1
    assert len(bundle["orchestration_history"]) >= 1

    logs = PrivacyAuditLog.query.filter_by(user_id=sample_user.id, action="EXPORT_REQUESTED").all()
    assert len(logs) >= 1

def test_rectify_user_data(app, sample_user):
    twin = StudentTwinRecord(user_id=sample_user.id, twin_version=1, learning_dna="visual")
    db.session.add(twin)
    db.session.commit()

    res = PrivacyService.rectify_user_data(sample_user.id, {
        "name": "Rectified Name",
        "twin_learning_dna_override": "auditory"
    })
    assert res["status"] == "RECTIFIED"
    
    user = User.query.get(sample_user.id)
    assert user.name == "Rectified Name"
    updated_twin = StudentTwinRecord.query.filter_by(user_id=sample_user.id).order_by(StudentTwinRecord.updated_at.desc()).first()
    assert updated_twin.learning_dna == "auditory"

def test_anonymize_user(app, sample_user):
    PrivacyService.anonymize_user(sample_user.id)
    user = User.query.get(sample_user.id)
    assert "Anonymized Student" in user.name
    assert "anon_" in user.email
    assert "@mentra.research" in user.email

def test_retention_policy(app, sample_user):
    old_date = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=35)
    recent_date = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=5)
    
    sess_old = AssessmentSession(session_id="old-gdpr-1", user_id=sample_user.id, exam_track="JEE", status="completed")
    sess_old.started_at = old_date
    sess_recent = AssessmentSession(session_id="rec-gdpr-1", user_id=sample_user.id, exam_track="JEE", status="completed")
    sess_recent.started_at = recent_date
    
    db.session.add_all([sess_old, sess_recent])
    db.session.commit()

    res = PrivacyService.enforce_retention_policies()
    assert res["purged_assessment_sessions"] >= 1
    assert AssessmentSession.query.filter_by(session_id="old-gdpr-1").count() == 0
    assert AssessmentSession.query.filter_by(session_id="rec-gdpr-1").count() == 1

def test_erase_user_data(app, sample_user):
    course, _ = _get_or_create_course_and_quiz()
    user_id = sample_user.id
    e = Enrollment(user_id=user_id, course_id=course.id, progress=50.0)
    db.session.add(e)
    db.session.commit()

    success = PrivacyService.erase_user_data(user_id)
    assert success is True
    assert User.query.get(user_id) is None
    assert Enrollment.query.filter_by(user_id=user_id).count() == 0

    complete_logs = PrivacyAuditLog.query.filter_by(action="ERASURE_COMPLETED").all()
    assert len(complete_logs) >= 1
    assert any(l.details.get("purged_user_id") == user_id for l in complete_logs)

def test_privacy_api_endpoints(client, sample_user):
    # GET consent
    res = client.get(f"/api/privacy/consent?user_id={sample_user.id}")
    assert res.status_code == 200
    assert "consents" in res.get_json()

    # PUT consent
    res = client.put("/api/privacy/consent", json={
        "user_id": sample_user.id,
        "consent_type": "BAYESIAN_PROFILING",
        "status": "REVOKED"
    })
    assert res.status_code == 200
    assert res.get_json()["status"] == "REVOKED"

    # GET export
    res = client.get(f"/api/privacy/export?user_id={sample_user.id}")
    assert res.status_code == 200
    assert "user_profile" in res.get_json()

    # PUT rectify
    res = client.put("/api/privacy/rectify", json={
        "user_id": sample_user.id,
        "name": "API Rectified Student"
    })
    assert res.status_code == 200
    assert "name" in res.get_json()["updated_fields"]

    # POST anonymize
    res = client.post("/api/privacy/anonymize", json={"user_id": sample_user.id})
    assert res.status_code == 200

    # POST retention enforce
    res = client.post("/api/privacy/retention/enforce")
    assert res.status_code == 200

    # POST erase
    res = client.post("/api/privacy/erase", json={"user_id": sample_user.id})
    assert res.status_code == 200
    assert User.query.get(sample_user.id) is None
