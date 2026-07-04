import pytest
from datetime import datetime, timezone
from backend.models import db, WorkflowStateRecord, EventRecord, PromptVersionRecord
from backend.services.orchestration.runtime.workflow_store import WorkflowStore
from backend.services.orchestration.runtime.event_bus import EventBus
from backend.services.orchestration.prompt_repository import PromptRepository
from backend.services.orchestration.prompts.registry import PromptRegistry

@pytest.fixture
def app():
    from backend.app import app as flask_app
    flask_app.config['TESTING'] = True
    with flask_app.app_context():
        db.create_all()
        try:
            from backend.models import ensure_privacy_schema
            ensure_privacy_schema(db.session)
        except Exception:
            pass
        yield flask_app

def test_workflow_store_persistence_and_recovery(app):
    with app.app_context():
        store = WorkflowStore()
        store.clear()
        
        # 1. Create a workflow
        wf_id = "wf-recovery-101"
        store.create_workflow(wf_id, "TutorAgent")
        
        # 2. Checkpoint state
        store.checkpoint_workflow(wf_id, {"step": "explaining_math", "context": {"problem": "2x + 5 = 15"}})
        
        # Verify persistence in DB
        rec = WorkflowStateRecord.query.get(wf_id)
        assert rec is not None
        assert rec.state_data.get("step") == "explaining_math"
        
        # Simulate crash by setting status to failed in DB
        rec.workflow_status = "failed"
        db.session.commit()
        
        # 3. Test retry recovery
        retried = store.recover_retry_workflows()
        assert len(retried) >= 1
        assert any(w["workflow_id"] == wf_id and w["workflow_status"] == "retrying" for w in retried)
        
        # 4. Test resume workflow
        resumed = store.resume_workflow(wf_id)
        assert resumed["workflow_status"] == "resumed"
        assert resumed["state_data"]["step"] == "explaining_math"

def test_event_bus_persistence_dlq_and_replay(app):
    with app.app_context():
        bus = EventBus()
        bus.clear()
        
        # 1. Test event persistence
        test_payload = {"idempotency_key": "evt-persist-1", "user_id": 1}
        bus.publish("user_enrolled", test_payload)
        
        rec = EventRecord.query.filter_by(event_type="user_enrolled").first()
        assert rec is not None
        assert rec.status == "PROCESSED"
        
        # 2. Test DLQ routing on handler failure
        def failing_handler(payload):
            raise ValueError("Simulated handler crash")
            
        bus.subscribe("risk_detected", failing_handler)
        dlq_payload = {"idempotency_key": "evt-dlq-1", "user_id": 2, "risk_score": 85}
        bus.publish("risk_detected", dlq_payload)
        
        dlq_events = bus.get_dlq_events()
        assert len(dlq_events) >= 1
        assert any(e["event_type"] == "risk_detected" for e in dlq_events)
        
        # 3. Test DLQ retry
        # Replace failing handler with succeeding handler
        bus._subscribers["risk_detected"] = [lambda p: None]
        dlq_target = [e for e in dlq_events if e["event_type"] == "risk_detected"][0]
        success = bus.retry_dlq_event(dlq_target["event_id"])
        assert success is True
        
        # 4. Test event replay
        replayed_count = bus.replay_events(event_type="user_enrolled")
        assert replayed_count >= 1

def test_prompt_repository_governance_and_rollback(app):
    with app.app_context():
        # 0. Clean prompt repository test records
        PromptVersionRecord.query.filter_by(prompt_id="tutor").delete()
        db.session.commit()

        # 1. Create initial prompt version
        prompt_id = "tutor"
        v1_content = "You are Tutor v1. Answer simply."
        PromptRepository.create_prompt(prompt_id, v1_content, semantic_version="1.0.0", status="APPROVED")
        
        # Verify active prompt content
        assert PromptRepository.get_active_prompt_content(prompt_id) == v1_content
        
        # 2. Verify integrity check
        assert PromptRepository.verify_prompt_integrity(prompt_id, "1.0.0") is True
        
        # 3. Create v2 in DRAFT
        v2_content = "You are Tutor v2. Answer with Socratic hints."
        PromptRepository.create_prompt(prompt_id, v2_content, semantic_version="2.0.0", status="DRAFT")
        
        # Active prompt should still be v1
        assert PromptRepository.get_active_prompt_content(prompt_id) == v1_content
        
        # 4. Approve v2
        PromptRepository.approve_prompt(prompt_id, "2.0.0", approver="QA_Lead")
        assert PromptRepository.get_active_prompt_content(prompt_id) == v2_content
        
        # 5. Rollback to v1
        PromptRepository.rollback_prompt(prompt_id, "1.0.0")
        assert PromptRepository.get_active_prompt_content(prompt_id) == v1_content
        
        # 6. Check backward compatibility with PromptRegistry
        reg = PromptRegistry()
        assert reg.get_prompt("TutorAgent") == v1_content
