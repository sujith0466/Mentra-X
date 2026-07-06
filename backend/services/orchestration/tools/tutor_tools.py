from backend.services.orchestration.tools.registry import ToolRegistry, ToolDefinition
from backend.services.adaptive.personalization_engine import PersonalizationEngine
import logging

logger = logging.getLogger(__name__)

def register_tutor_tools(registry: ToolRegistry):
    engine = PersonalizationEngine()

    select_level_def = ToolDefinition(
        name="selectExplanationLevel",
        description="Select pedagogical explanation level and style based on student DNA and failure history.",
        version="1.0.0",
        owner="AdaptiveLearningTeam",
        permissions="tutor:read",
        is_mutable=False,
        supports_streaming=False,
        supports_parallel=True,
        deterministic=True,
        needs_verification=False,
        produces_events=["learning.strategy_escalated"],
        consumes_events=[],
        input_schema={
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "concept": {"type": "string"},
                "dna": {"type": "object"},
                "explanation_history": {"type": "array"}
            },
            "required": ["concept"]
        },
        output_schema={"type": "object"},  # Dict representation of PersonalizationBundleDTO
        timeout_ms=1500,
        retry_count=1
    )

    def select_explanation_level_impl(kwargs: dict):
        user_id = kwargs.get("user_id", "")
        concept = kwargs.get("concept", "")
        dna = kwargs.get("dna")
        explanation_history = kwargs.get("explanation_history", [])
        weak_concepts = kwargs.get("weak_concepts", [])

        bundle = engine.assemble_personalization_bundle(
            user_id=str(user_id) if user_id else "",
            concept=str(concept),
            dna=dna,
            explanation_history=explanation_history,
            weak_concepts=weak_concepts
        )
        return bundle.to_dict()

    registry.register_tool(select_level_def, select_explanation_level_impl)
    logger.info("Registered tutor tools.")
