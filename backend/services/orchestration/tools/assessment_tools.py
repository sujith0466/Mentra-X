from backend.services.orchestration.tools.registry import ToolRegistry, ToolDefinition
from backend.services.assessment.assessment_facade import AssessmentFacade
import logging

logger = logging.getLogger(__name__)

def register_assessment_tools(registry: ToolRegistry):
    assessment_facade = AssessmentFacade()

    start_assessment_def = ToolDefinition(
        name="start_assessment_session",
        description="Spin up a Bayesian tracking session.",
        version="1.0.0",
        owner="AssessmentServiceTeam",
        permissions="assessment:write",
        is_mutable=True,
        supports_streaming=False,
        supports_parallel=False,
        deterministic=True,
        needs_verification=False,
        produces_events=["AssessmentStarted"],
        consumes_events=[],
        input_schema={
            "type": "object", 
            "properties": {
                "user_id": {"type": "integer"},
                "track": {"type": "string"}
            }, 
            "required": ["user_id", "track"]
        },
        output_schema={"type": "object"},
        timeout_ms=3000,
        retry_count=0
    )

    def start_assessment_impl(kwargs: dict):
        # We assume the facade returns a serializable dict or object
        return assessment_facade.start_assessment(
            user_id=kwargs["user_id"],
            track=kwargs["track"]
        )

    registry.register_tool(start_assessment_def, start_assessment_impl)
    logger.info("Registered assessment tools.")
