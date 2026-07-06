from backend.services.orchestration.tools.registry import ToolRegistry, ToolDefinition
from backend.services.adaptive.pacing_engine import FatigueDetector, SpacedRepetitionScheduler
import logging

logger = logging.getLogger(__name__)

def register_pacing_tools(registry: ToolRegistry):
    fatigue_detector = FatigueDetector()
    scheduler = SpacedRepetitionScheduler()

    fatigue_def = ToolDefinition(
        name="detectStudentFatigue",
        description="Monitor real-time session duration and error velocity to identify cognitive burnout and suggest mandatory breaks or light review.",
        version="1.0.0",
        owner="AdaptiveLearningTeam",
        permissions="pacing:read",
        is_mutable=False,
        supports_streaming=False,
        supports_parallel=True,
        deterministic=True,
        needs_verification=False,
        produces_events=["learning.fatigue_detected"],
        consumes_events=[],
        input_schema={
            "type": "object",
            "properties": {
                "session_duration_mins": {"type": "number"},
                "recent_errors": {"type": "integer"},
                "response_time_degradation_pct": {"type": "number"}
            },
            "required": ["session_duration_mins"]
        },
        output_schema={"type": "object"},
        timeout_ms=1000,
        retry_count=1
    )

    def fatigue_impl(kwargs: dict):
        dur = float(kwargs.get("session_duration_mins", 0))
        errs = int(kwargs.get("recent_errors", 0))
        deg = float(kwargs.get("response_time_degradation_pct", 0))
        dto = fatigue_detector.evaluate_fatigue(dur, errs, deg)
        return dto.to_dict()

    schedule_def = ToolDefinition(
        name="scheduleSpacedReview",
        description="Calculate Ebbinghaus retention decay curves to schedule automated spaced repetition reviews before memory consolidation fades.",
        version="1.0.0",
        owner="AdaptiveLearningTeam",
        permissions="pacing:read",
        is_mutable=False,
        supports_streaming=False,
        supports_parallel=True,
        deterministic=True,
        needs_verification=False,
        produces_events=["learning.review_scheduled"],
        consumes_events=[],
        input_schema={
            "type": "object",
            "properties": {
                "concept": {"type": "string"},
                "hours_since_last_review": {"type": "number"},
                "initial_mastery": {"type": "number"}
            },
            "required": ["concept", "hours_since_last_review"]
        },
        output_schema={"type": "object"},
        timeout_ms=1000,
        retry_count=1
    )

    def schedule_impl(kwargs: dict):
        concept = str(kwargs.get("concept", ""))
        hours = float(kwargs.get("hours_since_last_review", 0))
        mast = float(kwargs.get("initial_mastery", 0.80))
        dto = scheduler.calculate_review_schedule(concept, hours, mast)
        return dto.to_dict()

    registry.register_tool(fatigue_def, fatigue_impl)
    registry.register_tool(schedule_def, schedule_impl)
    logger.info("Registered adaptive pacing and review tools.")
