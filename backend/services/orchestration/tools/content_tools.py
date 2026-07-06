from backend.services.orchestration.tools.registry import ToolRegistry, ToolDefinition
from backend.services.adaptive.content_selector import ContentRankingEngine
from backend.services.adaptive.prerequisite_engine import PrerequisiteEngine
import logging

logger = logging.getLogger(__name__)

def register_content_tools(registry: ToolRegistry):
    ranking_engine = ContentRankingEngine()
    prereq_engine = PrerequisiteEngine()

    rank_content_def = ToolDefinition(
        name="rankContentForStudent",
        description="Rank candidate study materials and resources against student preferred learning style and failure avoidance.",
        version="1.0.0",
        owner="AdaptiveLearningTeam",
        permissions="content:read",
        is_mutable=False,
        supports_streaming=False,
        supports_parallel=True,
        deterministic=True,
        needs_verification=False,
        produces_events=[],
        consumes_events=[],
        input_schema={
            "type": "object",
            "properties": {
                "resources": {"type": "array"},
                "dna": {"type": "object"},
                "concept": {"type": "string"},
                "failed_resource_ids": {"type": "array"}
            },
            "required": ["resources"]
        },
        output_schema={"type": "array"},
        timeout_ms=1500,
        retry_count=1
    )

    def rank_content_impl(kwargs: dict):
        res = kwargs.get("resources", [])
        dna = kwargs.get("dna", {})
        concept = str(kwargs.get("concept", ""))
        failed = kwargs.get("failed_resource_ids", [])
        ranked = ranking_engine.rank_resources(res, dna, concept, failed)
        return [r.to_dict() for r in ranked]

    check_prereqs_def = ToolDefinition(
        name="checkPrerequisites",
        description="Check if student has sufficient concept mastery in foundational topics before advanced progression.",
        version="1.0.0",
        owner="AdaptiveLearningTeam",
        permissions="content:read",
        is_mutable=False,
        supports_streaming=False,
        supports_parallel=True,
        deterministic=True,
        needs_verification=False,
        produces_events=["learning.prerequisite_checked"],
        consumes_events=[],
        input_schema={
            "type": "object",
            "properties": {
                "target_concept": {"type": "string"},
                "dna": {"type": "object"},
                "mastery_threshold": {"type": "number"}
            },
            "required": ["target_concept"]
        },
        output_schema={"type": "object"},
        timeout_ms=1000,
        retry_count=1
    )

    def check_prereqs_impl(kwargs: dict):
        concept = str(kwargs.get("target_concept", ""))
        dna = kwargs.get("dna", {})
        thresh = float(kwargs.get("mastery_threshold", 0.60))
        return prereq_engine.check_prerequisites(concept, dna, mastery_threshold=thresh)

    registry.register_tool(rank_content_def, rank_content_impl)
    registry.register_tool(check_prereqs_def, check_prereqs_impl)
    logger.info("Registered intelligent content selection tools.")
