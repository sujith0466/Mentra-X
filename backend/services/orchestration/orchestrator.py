import logging
from typing import Dict, Any
from backend.services.orchestration.context_builder import ContextBuilder
from backend.services.orchestration.runtime.runtime import AgentRuntime
from backend.services.orchestration.runtime.execution_manager import ExecutionManager
from backend.services.orchestration.agents.registry import AgentRegistry

logger = logging.getLogger(__name__)

class Orchestrator:
    """
    Central Orchestrator for the Mastra Cognitive Swarm.
    Responsible for routing, triggering the runtime, verifying, and dispatching events.
    Contains zero business logic.
    """
    def __init__(self):
        self.context_builder = ContextBuilder()
        self.runtime = AgentRuntime()
        self.agent_registry = AgentRegistry()

    def process_query(self, user_id: int, workflow_id: str, query: str) -> Dict[str, Any]:
        logger.info(f"Orchestrator received query for workflow {workflow_id}")

        # 1. Update Workflow Store (Initialization)
        wf_state = self.runtime.start_workflow(workflow_id, "PendingSelection")

        # 2. Select the proper Agent (Routing logic)
        agents = self.agent_registry.discover_agents()
        selected_agent = None
        for agent_meta in sorted(agents, key=lambda a: a.priority, reverse=True):
            # Skip Verification Agent for initial routing
            if agent_meta.name == "VerificationAgent":
                continue
                
            agent = self.agent_registry.get_agent(agent_meta.name)
            if agent.can_handle(query):
                selected_agent = agent
                break
                
        if not selected_agent:
            # Fallback to TutorAgent if none explicitly handle
            selected_agent = self.agent_registry.get_agent("TutorAgent")

        self.runtime.workflow_store.update_workflow(workflow_id, {"current_agent": selected_agent.metadata.name})

        # 3. Build UnifiedContext
        unified_context = self.context_builder.build(
            user_id=user_id, 
            workflow_id=workflow_id, 
            current_agent=selected_agent.metadata.name,
            query=query
        )

        # 4. Invoke Runtime
        exec_manager = ExecutionManager(
            timeout_ms=selected_agent.metadata.timeout_ms,
            retries=selected_agent.metadata.retry_count,
            max_tokens=selected_agent.metadata.max_tokens
        )
        
        try:
            # 4.1 Execute Primary Agent
            primary_response = self.runtime.execute_agent_task(
                workflow_id=workflow_id,
                task_func=selected_agent.execute,
                execution_manager=exec_manager,
                unified_context=unified_context,
                query=query
            )

            # 5. Trigger Verification Agent
            verification_agent = self.agent_registry.get_agent("VerificationAgent")
            verify_manager = ExecutionManager(
                timeout_ms=verification_agent.metadata.timeout_ms,
                retries=verification_agent.metadata.retry_count
            )
            
            # Note: We pass primary_response as a string or serialized representation to verification
            verification_result = self.runtime.execute_agent_task(
                workflow_id=workflow_id,
                task_func=verification_agent.execute,
                execution_manager=verify_manager,
                unified_context=unified_context,
                agent_response=str(primary_response)
            )

            if not verification_result.get("is_safe", False):
                raise ValueError("Verification failed: " + verification_result.get("reason", "Unknown"))

            # 6. Publish Events (Mocking fan-out of events based on tools used)
            tools_used = primary_response.get("tools_used", [])
            for tool in tools_used:
                # We would normally look up the tool in ToolRegistry and emit `produces_events`
                # Here we just emit a generic event for the tool
                event_payload = {
                    "workflow_id": workflow_id,
                    "idempotency_key": f"{workflow_id}_{tool}",
                    "source_agent": selected_agent.metadata.name,
                    "tool": tool
                }
                self.runtime.emit_event(f"{tool}_executed", event_payload)

            # 7. Update Workflow Store (Completion)
            self.runtime.workflow_store.mark_completed(workflow_id)

            # 8. Return Final Response
            return primary_response

        except Exception as e:
            logger.error(f"Orchestration failed for workflow {workflow_id}: {e}")
            self.runtime.workflow_store.mark_failed(workflow_id, {"error": str(e)})
            raise
