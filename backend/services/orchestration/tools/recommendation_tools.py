from backend.services.orchestration.tools.registry import ToolRegistry, ToolDefinition
from backend.services.adaptive.recommendation_engine import UnifiedRecommendationEngine
import logging

logger = logging.getLogger(__name__)

def register_recommendation_tools(registry: ToolRegistry):
    engine = UnifiedRecommendationEngine()

    rec_def = ToolDefinition(
        name="getUnifiedRecommendations",
        description="Aggregate pedagogical decisions, study roadmaps, content fit, cognitive fatigue, and Ebbinghaus review schedules into a prioritized recommendation feed in under 200ms.",
        version="1.0.0",
        owner="AdaptiveLearningTeam",
        permissions="recommendations:read",
        is_mutable=False,
        supports_streaming=False,
        supports_parallel=True,
        deterministic=True,
        needs_verification=False,
        produces_events=["learning.recommendation_generated"],
        consumes_events=[],
        input_schema={
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "concept": {"type": "string"},
                "dna": {"type": "object"},
                "session_duration_mins": {"type": "number"},
                "recent_errors": {"type": "integer"},
                "lessons": {"type": "array"},
                "resources": {"type": "array"},
                "review_concepts": {"type": "array"}
            },
            "required": ["user_id"]
        },
        output_schema={"type": "object"},
        timeout_ms=1000,
        retry_count=1
    )

    def rec_impl(kwargs: dict):
        uid = str(kwargs.get("user_id", ""))
        concept = str(kwargs.get("concept", "general"))
        dna = kwargs.get("dna")
        dur = float(kwargs.get("session_duration_mins", 0))
        errs = int(kwargs.get("recent_errors", 0))
        lessons = kwargs.get("lessons")
        res = kwargs.get("resources")
        rev = kwargs.get("review_concepts")
        dto = engine.generate_feed(uid, concept, dna, dur, errs, 0.0, 1, lessons, res, rev)
        return dto.to_dict()

    registry.register_tool(rec_def, rec_impl)
    logger.info("Registered unified recommendation engine tools.")
