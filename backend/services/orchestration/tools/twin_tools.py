from backend.services.orchestration.tools.registry import ToolRegistry, ToolDefinition
from backend.services.twin.twin_facade import TwinFacade
import logging

logger = logging.getLogger(__name__)

def register_twin_tools(registry: ToolRegistry):
    twin_facade = TwinFacade()

    get_twin_def = ToolDefinition(
        name="get_digital_twin",
        description="Fetch the holistic profile of the student.",
        version="1.0.0",
        owner="TwinServiceTeam",
        permissions="twin:read",
        is_mutable=False,
        supports_streaming=False,
        supports_parallel=True,
        deterministic=True,
        needs_verification=False,
        produces_events=[],
        consumes_events=[],
        input_schema={"type": "object", "properties": {"user_id": {"type": "integer"}}, "required": ["user_id"]},
        output_schema={"type": "object"}, # Dict representation of twin
        timeout_ms=1500,
        retry_count=1
    )

    def get_digital_twin_impl(kwargs: dict):
        user_id = kwargs.get("user_id")
        twin = twin_facade.get_twin(user_id)
        # Convert to dict for safety
        return {
            "version": twin.twin_version,
            "status": twin.twin_status,
            "health": twin.twin_health,
            "exam_track": twin.exam_track,
            "academic_state": twin.academic_state,
            "skill_state": twin.skill_state,
            "learning_dna": twin.learning_dna,
            "career_state": twin.career_state,
            "project_state": twin.project_state,
            "opportunity_state": twin.opportunity_state,
        }

    registry.register_tool(get_twin_def, get_digital_twin_impl)
    logger.info("Registered twin tools.")
