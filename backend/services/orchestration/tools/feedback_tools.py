from backend.services.orchestration.tools.registry import ToolRegistry, ToolDefinition
from backend.services.adaptive.feedback_engine import ProgressiveHintEngine, SocraticFeedbackEngine
import logging

logger = logging.getLogger(__name__)

def register_feedback_tools(registry: ToolRegistry):
    hint_engine = ProgressiveHintEngine()
    socratic_engine = SocraticFeedbackEngine()

    hint_def = ToolDefinition(
        name="generateProgressiveHint",
        description="Supply incremental study hints (conceptual nudge -> structural framework -> specific step -> full walkthrough) without giving immediate solutions.",
        version="1.0.0",
        owner="AdaptiveLearningTeam",
        permissions="tutor:read",
        is_mutable=False,
        supports_streaming=False,
        supports_parallel=True,
        deterministic=True,
        needs_verification=False,
        produces_events=["learning.hint_generated"],
        consumes_events=[],
        input_schema={
            "type": "object",
            "properties": {
                "concept": {"type": "string"},
                "current_hint_index": {"type": "integer"},
                "problem_context": {"type": "string"},
                "custom_hints": {"type": "array"}
            },
            "required": ["concept"]
        },
        output_schema={"type": "object"},
        timeout_ms=1000,
        retry_count=1
    )

    def hint_impl(kwargs: dict):
        concept = str(kwargs.get("concept", ""))
        idx = int(kwargs.get("current_hint_index", 0))
        ctx = kwargs.get("problem_context")
        custom = kwargs.get("custom_hints")
        dto = hint_engine.get_hint(concept, idx, ctx, custom)
        return dto.to_dict()

    socratic_def = ToolDefinition(
        name="formulateSocraticQuestion",
        description="Formulate guiding Socratic questions in response to student practice errors rather than flat corrections.",
        version="1.0.0",
        owner="AdaptiveLearningTeam",
        permissions="tutor:read",
        is_mutable=False,
        supports_streaming=False,
        supports_parallel=True,
        deterministic=True,
        needs_verification=False,
        produces_events=["learning.socratic_generated"],
        consumes_events=[],
        input_schema={
            "type": "object",
            "properties": {
                "concept": {"type": "string"},
                "student_answer": {"type": "string"},
                "expected_concept_rule": {"type": "string"},
                "is_correct": {"type": "boolean"}
            },
            "required": ["concept", "student_answer"]
        },
        output_schema={"type": "object"},
        timeout_ms=1000,
        retry_count=1
    )

    def socratic_impl(kwargs: dict):
        concept = str(kwargs.get("concept", ""))
        ans = kwargs.get("student_answer", "")
        rule = str(kwargs.get("expected_concept_rule", ""))
        is_corr = bool(kwargs.get("is_correct", False))
        dto = socratic_engine.generate_socratic_feedback(concept, ans, rule, is_corr)
        return dto.to_dict()

    registry.register_tool(hint_def, hint_impl)
    registry.register_tool(socratic_def, socratic_impl)
    logger.info("Registered real-time adaptive feedback tools.")
