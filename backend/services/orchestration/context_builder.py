import logging
from typing import Dict, Any, List

from backend.services.twin.twin_facade import TwinFacade
from backend.services.assessment.assessment_facade import AssessmentFacade
from backend.services.memory.memory_facade import MemoryFacade

logger = logging.getLogger(__name__)

class ContextBuilder:
    """
    Synchronously collects Static, Dynamic, and Execution context to build
    an immutable UnifiedContext object.
    """

    def __init__(self):
        self.twin_facade = TwinFacade()
        self.assessment_facade = AssessmentFacade()
        self.memory_facade = MemoryFacade()

    def build(self, user_id: int, workflow_id: str, current_agent: str, query: str = "") -> Dict[str, Any]:
        """
        Builds the unified context object for the orchestrator.
        """
        logger.info(f"Building unified context for user {user_id} in workflow {workflow_id}")

        # 1. Static Context
        try:
            twin_record = self.twin_facade.get_twin(user_id)
            import json
            learning_dna = json.loads(twin_record.learning_dna) if twin_record.learning_dna else {}
            
            static_context = {
                "user": {
                    "id": user_id,
                    "exam_track": twin_record.exam_track
                },
                "twin": {
                    "version": twin_record.twin_version,
                    "health": twin_record.twin_health,
                    "status": twin_record.twin_status
                },
                "learning_dna": learning_dna
            }
        except Exception as e:
            logger.error(f"Failed to build static context: {e}")
            static_context = {}

        # 2. Dynamic Context
        try:
            memory_points = []
            if query:
                # Naive top 3 retrieval for immediate context
                memory_points = self.memory_facade.retrieve_context(
                    collection_name="past_doubts", 
                    query_text=query, 
                    user_id=user_id, 
                    limit=3
                )
            
            dynamic_context = {
                "assessment": {
                    "active_session_id": None # To be populated by AssessmentFacade real implementation
                },
                "memory": {
                    "recent_doubts": memory_points
                },
                "weak_concepts": [], # Placeholder for twin parsing
                "opportunity_state": {}
            }
        except Exception as e:
            logger.error(f"Failed to build dynamic context: {e}")
            dynamic_context = {}

        # 3. Execution Context
        import time
        execution_context = {
            "workflow_metadata": {
                "workflow_id": workflow_id,
                "current_agent": current_agent,
                "attempt_number": 1
            },
            "runtime_metadata": {
                "timeout_budget_ms": 5000,
                "retry_count": 0
            },
            "trace_metadata": {
                "timestamp": time.time()
            }
        }

        return {
            "static_context": static_context,
            "dynamic_context": dynamic_context,
            "execution_context": execution_context
        }
