from __future__ import annotations

import io
import sys
import uuid
from pathlib import Path

from sqlalchemy import text

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import app
from backend.models import (
    Assignment,
    AssignmentSubmission,
    ChatbotConversation,
    CommunityAnswer,
    CommunityPost,
    Course,
    Domain,
    Enrollment,
    LearningStreak,
    LessonProgress,
    ProjectIdea,
    ProjectTask,
    Quiz,
    QuizAnswer,
    QuizAttempt,
    QuizQuestion,
    ReferralTransaction,
    StudentProject,
    UserBadge,
    UserXP,
    User,
    UserResume,
    Video,
    db,
    StudentTwinRecord,
    TwinKnowledgeStateRecord,
    TwinMutationLogRecord,
    QuestionMetadata,
    AssessmentSession,
    AssessmentResponse,
    AssessmentResult,
)


class SQLiteFixtureMixin:
    fixture_ids = {}
    fixture_token = ""

    @classmethod
    def create_base_fixture(cls):
        raw_token = uuid.uuid4().hex[:8]
        token = "".join(chr(97 + (int(ch, 16) % 26)) for ch in raw_token)
        cls.fixture_token = token
        with app.app_context():
            domain = Domain(name=f"Learning Domain {token}", description="Automation learning domain")
            db.session.add(domain)
            db.session.flush()

            course = Course(
                title=f"Learning Course {token}",
                description="Python basics. Flask patterns. SQL practice.",
                domain_id=domain.id,
                price=0.0,
                instructor="Mentra Instructor",
                status="published",
                demo_video_url="https://example.com/demo",
            )
            recommended_course = Course(
                title=f"Advanced Learning Course {token}",
                description="Advanced Python and Flask architecture patterns.",
                domain_id=domain.id,
                price=0.0,
                instructor="Mentra Instructor",
                status="published",
            )
            db.session.add_all([course, recommended_course])
            db.session.flush()

            video = Video(
                course_id=course.id,
                title=f"Learning Lesson {token}",
                video_url="https://example.com/video",
                description="Introduction to Python. Functions and Flask routing. SQL joins.",
                duration="10:00",
                order_number=1,
            )
            db.session.add(video)
            db.session.flush()

            quiz = Quiz(
                course_id=course.id,
                title=f"Learning Quiz {token}",
                description="Quiz for learning course",
                question_count_target=1,
                passing_percentage=60.0,
                time_limit_minutes=10,
                attempts_allowed=3,
                is_enabled=True,
            )
            db.session.add(quiz)
            db.session.flush()

            question = QuizQuestion(
                quiz_id=quiz.id,
                question_text="What language is used in Flask?",
                question_type="mcq",
                option_a="Python",
                option_b="Java",
                option_c="C#",
                option_d="Ruby",
                correct_answer="Python",
                order_index=1,
                order_number=1,
            )
            assignment = Assignment(
                course_id=course.id,
                title=f"Learning Assignment {token}",
                instructions="Submit a short explanation of Flask routing.",
                marks=100.0,
            )
            student = User(
                name=f"QA Student {token}",
                email=f"qa_student_{token}@example.com",
                role="student",
                referral_code=f"QASTU{token}"[:20],
                wallet_balance=0.0,
            )
            student.set_password("Password123")
            db.session.add_all([question, assignment, student])
            db.session.commit()

            cls.fixture_ids = {
                "domain_id": domain.id,
                "course_id": course.id,
                "recommended_course_id": recommended_course.id,
                "video_id": video.id,
                "quiz_id": quiz.id,
                "question_id": question.id,
                "assignment_id": assignment.id,
                "student_id": student.id,
                "student_email": student.email,
            }

    @classmethod
    def ensure_enrollment(cls, progress=0.0, completed=False):
        with app.app_context():
            enrollment = Enrollment.query.filter_by(
                user_id=cls.fixture_ids["student_id"],
                course_id=cls.fixture_ids["course_id"],
            ).first()
            if not enrollment:
                enrollment = Enrollment(
                    user_id=cls.fixture_ids["student_id"],
                    course_id=cls.fixture_ids["course_id"],
                    progress=progress,
                    progress_percentage=progress,
                    completed=completed,
                )
                db.session.add(enrollment)
            else:
                enrollment.progress = progress
                enrollment.progress_percentage = progress
                enrollment.completed = completed
            db.session.commit()
            return enrollment.id

    @classmethod
    def login_student(cls, client):
        with client.session_transaction() as session:
            session["user_id"] = cls.fixture_ids["student_id"]
            session["user_name"] = f"QA Student {cls.fixture_token}"
            session["user_role"] = "student"
            session["user_email"] = cls.fixture_ids["student_email"]

    @staticmethod
    def clear_session(client):
        with client.session_transaction() as session:
            session.clear()

    @classmethod
    def cleanup_fixture(cls):
        with app.app_context():
            if db.engine.dialect.name == 'mysql':
                db.session.execute(text('SET FOREIGN_KEY_CHECKS=0'))
                db.session.commit()
            student_id = cls.fixture_ids.get("student_id")
            
            if student_id:
                # Delete assessment and twin data
                session_ids = [s.id for s in AssessmentSession.query.filter_by(user_id=student_id).all()]
                if session_ids:
                    AssessmentResponse.query.filter(AssessmentResponse.session_id.in_(session_ids)).delete(synchronize_session=False)
                    AssessmentResult.query.filter(AssessmentResult.session_id.in_(session_ids)).delete(synchronize_session=False)
                AssessmentSession.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                
                # Delete twin records
                TwinKnowledgeStateRecord.query.filter(TwinKnowledgeStateRecord.twin_id.in_(
                    db.session.query(StudentTwinRecord.id).filter_by(user_id=student_id)
                )).delete(synchronize_session=False)
                StudentTwinRecord.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                TwinMutationLogRecord.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                
            attempt_ids = [row.id for row in QuizAttempt.query.filter_by(user_id=student_id).all()] if student_id else []
            if attempt_ids:
                QuizAnswer.query.filter(QuizAnswer.attempt_id.in_(attempt_ids)).delete(synchronize_session=False)
            if student_id:
                QuizAttempt.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                AssignmentSubmission.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                LessonProgress.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                Enrollment.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                LearningStreak.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                ChatbotConversation.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                student_project_ids = [row.id for row in StudentProject.query.filter_by(user_id=student_id).all()]
                if student_project_ids:
                    ProjectTask.query.filter(ProjectTask.project_id.in_(student_project_ids)).delete(synchronize_session=False)
                StudentProject.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                CommunityAnswer.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                CommunityPost.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                UserBadge.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                UserXP.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                UserResume.query.filter_by(user_id=student_id).delete(synchronize_session=False)
                ReferralTransaction.query.filter((ReferralTransaction.referrer_id == student_id) | (ReferralTransaction.new_user_id == student_id)).delete(synchronize_session=False)
                User.query.filter(User.email.like(f"qa_register_{cls.fixture_token}%@example.com")).delete(synchronize_session=False)
            
            # Deletion of global test metadata
            question_id = cls.fixture_ids.get("question_id")
            if question_id:
                QuestionMetadata.query.filter_by(question_id=question_id).delete(synchronize_session=False)
                
            for model, key in [
                (QuizQuestion, "question_id"),
                (Quiz, "quiz_id"),
                (Assignment, "assignment_id"),
                (Video, "video_id"),
                (Course, "course_id"),
                (Course, "recommended_course_id"),
                (Domain, "domain_id"),
                (User, "student_id"),
            ]:
                record_id = cls.fixture_ids.get(key)
                if record_id:
                    model.query.filter_by(id=record_id).delete(synchronize_session=False)
            
            if db.engine.dialect.name == 'mysql':
                db.session.execute(text('SET FOREIGN_KEY_CHECKS=1'))
            db.session.commit()

    @staticmethod
    def text_upload(content: str, filename: str = "resume.txt"):
        return io.BytesIO(content.encode("utf-8")), filename
