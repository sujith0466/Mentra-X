import logging
from typing import Dict, Any, Callable
from backend.services.orchestration.runtime.workflow_store import WorkflowStore
from backend.services.orchestration.runtime.event_bus import EventBus
from backend.services.orchestration.runtime.execution_manager import ExecutionManager
from backend.services.orchestration.runtime.telemetry import trace_execution

logger = logging.getLogger(__name__)

class AgentRuntime:
    """
    Central entry point for orchestrator interactions.
    Provides methods to start workflows, manage agents, and emit events.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentRuntime, cls).__new__(cls)
            cls._instance.workflow_store = WorkflowStore()
            cls._instance.event_bus = EventBus()
        return cls._instance

    @trace_execution(name="start_workflow")
    def start_workflow(self, workflow_id: str, initial_agent: str) -> Dict[str, Any]:
        """
        Initializes a new tracking state in the Workflow Store.
        """
        logger.info(f"Starting workflow {workflow_id} with agent {initial_agent}")
        return self.workflow_store.create_workflow(workflow_id, initial_agent)

    @trace_execution(name="execute_agent_task")
    def execute_agent_task(self, 
                           workflow_id: str, 
                           task_func: Callable, 
                           execution_manager: ExecutionManager, 
                           *args, **kwargs) -> Any:
        """
        Executes a specific agent task with full execution policies and observability.
        """
        try:
            result = execution_manager.execute(task_func, *args, **kwargs)
            self.workflow_store.add_execution_event(workflow_id, {
                "type": "agent_execution_success",
                "func": task_func.__name__
            })
            return result
        except Exception as e:
            logger.error(f"Task {task_func.__name__} failed in workflow {workflow_id}: {e}")
            self.workflow_store.mark_failed(workflow_id, {"error": str(e)})
            raise

    @trace_execution(name="emit_event")
    def emit_event(self, event_type: str, payload: Dict[str, Any]):
        """
        Routes an event through the Event Bus.
        """
        self.event_bus.publish(event_type, payload)
