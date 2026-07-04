import logging
import threading
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class WorkflowStore:
    """
    Persistent Workflow Store for Agent Runtime layer (Phase 5 Milestone 4).
    Tracks workflow state, progress, errors, checkpointing, and enables resumable execution.
    Backed by PostgreSQL / MySQL (via SQLAlchemy WorkflowStateRecord) with an in-memory L1 cache.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(WorkflowStore, cls).__new__(cls)
                cls._instance._workflows: Dict[str, Dict[str, Any]] = {}
        return cls._instance

    def create_workflow(self, workflow_id: str, initial_agent: str) -> Dict[str, Any]:
        with self._lock:
            if workflow_id in self._workflows or self._load_from_db(workflow_id):
                raise ValueError(f"Workflow {workflow_id} already exists.")
            
            now = datetime.now(timezone.utc).isoformat()
            self._workflows[workflow_id] = {
                "workflow_id": workflow_id,
                "workflow_status": "started",
                "current_step": 0,
                "completed_steps": [],
                "current_agent": initial_agent,
                "started_at": now,
                "updated_at": now,
                "execution_events": [],
                "retry_count": 0,
                "error_context": None,
                "consent_snapshot": None,
                "state_data": {}
            }
            self._sync_to_db(workflow_id)
            return self._workflows[workflow_id]

    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            wf = self._workflows.get(workflow_id)
            if not wf:
                wf = self._load_from_db(workflow_id)
            return wf

    def update_workflow(self, workflow_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            workflow = self._workflows.get(workflow_id)
            if not workflow:
                workflow = self._load_from_db(workflow_id)
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found.")
            
            for k, v in updates.items():
                workflow[k] = v
            
            if "user_id" in updates and workflow.get("consent_snapshot") is None:
                try:
                    from backend.services.privacy.consent_service import ConsentService
                    workflow["consent_snapshot"] = ConsentService.get_all_consents(int(updates["user_id"]))
                except Exception:
                    pass

            workflow["updated_at"] = datetime.now(timezone.utc).isoformat()
            self._sync_to_db(workflow_id)
            return workflow

    def mark_completed(self, workflow_id: str):
        return self.update_workflow(workflow_id, {"workflow_status": "completed"})

    def mark_failed(self, workflow_id: str, error_context: Dict[str, Any]):
        return self.update_workflow(workflow_id, {
            "workflow_status": "failed", 
            "error_context": error_context
        })

    def add_execution_event(self, workflow_id: str, event: Dict[str, Any]):
        with self._lock:
            workflow = self._workflows.get(workflow_id)
            if not workflow:
                workflow = self._load_from_db(workflow_id)
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found.")
            if "execution_events" not in workflow or not isinstance(workflow["execution_events"], list):
                workflow["execution_events"] = []
            workflow["execution_events"].append(event)
            workflow["updated_at"] = datetime.now(timezone.utc).isoformat()
            self._sync_to_db(workflow_id)

    def checkpoint_workflow(self, workflow_id: str, state_data: Dict[str, Any]) -> Dict[str, Any]:
        """Saves a checkpoint of the workflow's state_data and syncs to persistent storage."""
        with self._lock:
            workflow = self._workflows.get(workflow_id)
            if not workflow:
                workflow = self._load_from_db(workflow_id)
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found.")
            if "state_data" not in workflow or not isinstance(workflow["state_data"], dict):
                workflow["state_data"] = {}
            workflow["state_data"].update(state_data)
            workflow["updated_at"] = datetime.now(timezone.utc).isoformat()
            self._sync_to_db(workflow_id)
            return workflow

    def resume_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Resumes a checkpointed or interrupted workflow from persistent storage."""
        with self._lock:
            workflow = self._workflows.get(workflow_id)
            if not workflow:
                workflow = self._load_from_db(workflow_id)
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found.")
            if workflow["workflow_status"] in ["failed", "started", "recovered", "retrying"]:
                workflow["workflow_status"] = "resumed"
                workflow["updated_at"] = datetime.now(timezone.utc).isoformat()
                self._sync_to_db(workflow_id)
            return workflow

    def recover_crashed_workflows(self) -> List[Dict[str, Any]]:
        """Finds all started or crashed workflows in persistent storage and marks them ready for recovery."""
        recovered = []
        try:
            from backend.models import db, WorkflowStateRecord
            records = WorkflowStateRecord.query.filter(WorkflowStateRecord.workflow_status.in_(["started", "failed"])).all()
            for rec in records:
                rec.workflow_status = "recovered"
                db.session.commit()
                wf = self._load_from_db(rec.workflow_id)
                if wf:
                    recovered.append(wf)
        except Exception as e:
            logger.debug(f"Could not recover crashed workflows from DB: {e}")
        return recovered

    def recover_retry_workflows(self) -> List[Dict[str, Any]]:
        """Identifies failed workflows eligible for retry and increments their retry_count."""
        retried = []
        try:
            from backend.models import db, WorkflowStateRecord
            records = WorkflowStateRecord.query.filter_by(workflow_status="failed").all()
            for rec in records:
                if rec.retry_count < 3: # default max retry
                    rec.retry_count += 1
                    rec.workflow_status = "retrying"
                    db.session.commit()
                    wf = self._load_from_db(rec.workflow_id)
                    if wf:
                        retried.append(wf)
        except Exception as e:
            logger.debug(f"Could not recover retry workflows from DB: {e}")
        return retried

    def get_user_workflows(self, user_id: int) -> list:
        with self._lock:
            result = []
            try:
                from backend.models import WorkflowStateRecord
                records = WorkflowStateRecord.query.filter_by(user_id=user_id).all()
                for rec in records:
                    wf = self._load_from_db(rec.workflow_id)
                    if wf:
                        result.append(wf)
                return result
            except Exception:
                pass
            for wf in self._workflows.values():
                if wf.get("user_id") == user_id or any(ev.get("user_id") == user_id for ev in wf.get("execution_events", [])):
                    result.append(wf)
            return result

    def delete_user_workflows(self, user_id: int) -> int:
        with self._lock:
            try:
                from backend.models import db, WorkflowStateRecord
                WorkflowStateRecord.query.filter_by(user_id=user_id).delete()
                db.session.commit()
            except Exception:
                pass
            to_delete = [
                wfid for wfid, wf in self._workflows.items()
                if wf.get("user_id") == user_id or any(ev.get("user_id") == user_id for ev in wf.get("execution_events", []))
            ]
            for wfid in to_delete:
                del self._workflows[wfid]
            return len(to_delete)

    def list_all_workflows(self) -> List[Dict[str, Any]]:
        """Returns a list of all stored workflows for monitoring aggregation."""
        with self._lock:
            try:
                from backend.models import WorkflowStateRecord
                records = WorkflowStateRecord.query.all()
                res = []
                for rec in records:
                    res.append({
                        "workflow_id": rec.workflow_id,
                        "workflow_status": rec.workflow_status,
                        "current_step": rec.current_step,
                        "current_agent": rec.current_agent,
                        "retry_count": rec.retry_count,
                        "started_at": rec.started_at.isoformat() if rec.started_at else None,
                        "updated_at": rec.updated_at.isoformat() if rec.updated_at else None
                    })
                return res
            except Exception as e:
                logger.debug(f"Failed to list workflows from DB: {e}")
                return list(self._workflows.values())

    def get_store_metrics(self) -> Dict[str, Any]:
        """Returns aggregate metrics on workflow store health and execution status."""
        wfs = self.list_all_workflows()
        status_counts = {"started": 0, "completed": 0, "failed": 0, "retrying": 0, "waiting": 0}
        total_lat = 0.0
        lat_count = 0
        for wf in wfs:
            st = wf.get("workflow_status", "started")
            status_counts[st] = status_counts.get(st, 0) + 1
            if wf.get("retry_count", 0) > 0 and st == "started":
                status_counts["retrying"] = status_counts.get("retrying", 0) + 1
        return {
            "total_workflows": len(wfs),
            "status_counts": status_counts,
            "status": "HEALTHY"
        }

    def clear(self):
        """For testing purposes."""
        with self._lock:
            self._workflows.clear()
            try:
                from backend.models import db, WorkflowStateRecord
                WorkflowStateRecord.query.delete()
                db.session.commit()
            except Exception:
                pass

    def _sync_to_db(self, workflow_id: str):
        try:
            from backend.models import db, WorkflowStateRecord
            workflow = self._workflows.get(workflow_id)
            if not workflow:
                return
            rec = WorkflowStateRecord.query.get(workflow_id)
            if not rec:
                rec = WorkflowStateRecord(workflow_id=workflow_id)
                db.session.add(rec)
            rec.workflow_status = workflow.get("workflow_status", "started")
            rec.current_step = workflow.get("current_step", 0)
            rec.completed_steps = workflow.get("completed_steps", [])
            rec.current_agent = workflow.get("current_agent")
            user_id_val = workflow.get("user_id")
            rec.user_id = int(user_id_val) if user_id_val is not None else None
            rec.execution_events = workflow.get("execution_events", [])
            rec.retry_count = workflow.get("retry_count", 0)
            rec.error_context = workflow.get("error_context")
            rec.consent_snapshot = workflow.get("consent_snapshot")
            rec.state_data = workflow.get("state_data", {})
            db.session.commit()
        except Exception as e:
            try:
                from backend.models import db
                db.session.rollback()
            except Exception:
                pass

    def _load_from_db(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        try:
            from backend.models import WorkflowStateRecord
            rec = WorkflowStateRecord.query.get(workflow_id)
            if rec:
                wf = {
                    "workflow_id": rec.workflow_id,
                    "workflow_status": rec.workflow_status,
                    "current_step": rec.current_step,
                    "completed_steps": rec.completed_steps or [],
                    "current_agent": rec.current_agent,
                    "user_id": rec.user_id,
                    "execution_events": rec.execution_events or [],
                    "retry_count": rec.retry_count,
                    "error_context": rec.error_context,
                    "consent_snapshot": rec.consent_snapshot,
                    "state_data": rec.state_data or {},
                    "started_at": rec.started_at.isoformat() if rec.started_at else None,
                    "updated_at": rec.updated_at.isoformat() if rec.updated_at else None
                }
                self._workflows[workflow_id] = wf
                return wf
        except Exception:
            pass
        return None
