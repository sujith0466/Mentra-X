import logging
import threading
from typing import Dict, Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class WorkflowStore:
    """
    In-memory Workflow Store for Agent Runtime layer.
    Tracks workflow state, progress, errors, and enables resumable execution.
    In a real production environment, this would be backed by Redis or Postgres.
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
            if workflow_id in self._workflows:
                raise ValueError(f"Workflow {workflow_id} already exists.")
            
            self._workflows[workflow_id] = {
                "workflow_id": workflow_id,
                "workflow_status": "started",
                "current_step": 0,
                "completed_steps": [],
                "current_agent": initial_agent,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "execution_events": [],
                "retry_count": 0,
                "error_context": None
            }
            return self._workflows[workflow_id]

    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        return self._workflows.get(workflow_id)

    def update_workflow(self, workflow_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            workflow = self._workflows.get(workflow_id)
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found.")
            
            for k, v in updates.items():
                workflow[k] = v
            
            workflow["updated_at"] = datetime.now(timezone.utc).isoformat()
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
                raise ValueError(f"Workflow {workflow_id} not found.")
            workflow["execution_events"].append(event)
            workflow["updated_at"] = datetime.now(timezone.utc).isoformat()

    def clear(self):
        """For testing purposes."""
        with self._lock:
            self._workflows.clear()
