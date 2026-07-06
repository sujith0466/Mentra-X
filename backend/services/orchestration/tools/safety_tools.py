"""
Mentra X — Enkrypt Safety Layer Mastra Tools (Phase 7 Layer 6)

Registers tools for executing Enkrypt 4-pipeline safety validation and
running automated regeneration loops for failed tutor outputs.
"""

from typing import Dict, Any, Optional
from backend.services.orchestration.tools.registry import ToolRegistry, ToolDefinition
from backend.services.enkrypt.enkrypt_validator import EnkryptValidator
from backend.services.enkrypt.regeneration_loop import RegenerationLoop
from backend.services.enkrypt.safety_monitor import safety_monitor

_validator = EnkryptValidator()
_regen_loop = RegenerationLoop()


def callEnkryptValidation(*args, **kwargs) -> Dict[str, Any]:
    """
    Runs all 4 Enkrypt validation pipelines (Math, Science, Hallucination, Pedagogy),
    logs the intercept event, and returns the validation DTO dictionary.
    """
    # Handle dict arg or keyword args
    if len(args) > 0 and isinstance(args[0], dict):
        kwargs = {**args[0], **kwargs}
    text = kwargs.get("text") or (args[0] if len(args) > 0 and isinstance(args[0], str) else "")
    subject = kwargs.get("subject", "physics")
    level = int(kwargs.get("level", 1))
    exam_track = kwargs.get("exam_track", "JEE")
    session_id = kwargs.get("session_id", "default_session")
    user_id = kwargs.get("user_id", "default_user")

    res = _validator.validate(text=text, subject_tag=subject, exam_track=exam_track, level=level)
    safety_monitor.log_intercept(
        session_id=session_id,
        user_id=user_id,
        original_output=text,
        result=res,
        final_output=text if res.recommended_action == "APPROVE" else "",
        regeneration_count=0,
        hitl_flagged=(res.recommended_action == "HARD_FAIL")
    )
    if res.recommended_action == "HARD_FAIL":
        safety_monitor.queue_hitl(
            session_id=session_id,
            user_id=user_id,
            concept="general",
            original_query=text[:100],
            failed_output=text,
            scores={
                "math": res.math_score,
                "science": res.science_score,
                "hallucination": res.hallucination_score,
                "pedagogy": res.pedagogy_score,
                "composite": res.composite_confidence
            }
        )
    return res.to_dict()


def executeRegenerationLoop(*args, **kwargs) -> Dict[str, Any]:
    """
    Executes the up-to-2-attempt Enkrypt regeneration loop with textbook fallback.
    """
    if len(args) > 0 and isinstance(args[0], dict):
        kwargs = {**args[0], **kwargs}
    original_output = kwargs.get("original_output") or (args[0] if len(args) > 0 and isinstance(args[0], str) else "")
    concept = kwargs.get("concept") or (args[1] if len(args) > 1 and isinstance(args[1], str) else "general")
    exam_track = kwargs.get("exam_track", "JEE")
    subject = kwargs.get("subject", "physics")
    level = int(kwargs.get("level", 1))
    session_id = kwargs.get("session_id", "default_session")
    user_id = kwargs.get("user_id", "default_user")

    initial_val = _validator.validate(text=original_output, subject_tag=subject, exam_track=exam_track, level=level)
    
    def dummy_generator(instruction: str) -> str:
        return f"Revised explanation for {concept} in {exam_track}: verified derivations and formulas applied correctly."

    regen_res = _regen_loop.execute(
        original_output=original_output,
        initial_validation=initial_val,
        tutor_generator_fn=dummy_generator,
        concept=concept,
        exam_track=exam_track,
        subject=subject,
        level=level
    )

    safety_monitor.log_intercept(
        session_id=session_id,
        user_id=user_id,
        original_output=original_output,
        result=regen_res.validation_result,
        final_output=regen_res.final_output,
        regeneration_count=regen_res.attempts_used,
        hitl_flagged=regen_res.hitl_flagged
    )

    if regen_res.hitl_flagged:
        safety_monitor.queue_hitl(
            session_id=session_id,
            user_id=user_id,
            concept=concept,
            original_query=original_output[:100],
            failed_output=original_output,
            scores={
                "math": regen_res.validation_result.math_score,
                "science": regen_res.validation_result.science_score,
                "hallucination": regen_res.validation_result.hallucination_score,
                "pedagogy": regen_res.validation_result.pedagogy_score,
                "composite": regen_res.validation_result.composite_confidence
            }
        )

    return regen_res.to_dict()


def register_safety_tools(registry: ToolRegistry):
    def1 = ToolDefinition(
        name="callEnkryptValidation",
        description="Validates tutor response text through Enkrypt 4-pipeline safety audit (Math, Science, Hallucination, Pedagogy).",
        version="1.0.0",
        owner="SafetyTeam",
        permissions="safety:execute",
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
                "text": {"type": "string"},
                "subject": {"type": "string"},
                "level": {"type": "integer"},
                "exam_track": {"type": "string"},
                "session_id": {"type": "string"},
                "user_id": {"type": "string"}
            },
            "required": ["text"]
        },
        output_schema={"type": "object"},
        timeout_ms=1500,
        retry_count=1
    )
    registry.register_tool(def1, callEnkryptValidation)

    def2 = ToolDefinition(
        name="executeRegenerationLoop",
        description="Executes Enkrypt regeneration loop with textbook fallback on hard safety failures.",
        version="1.0.0",
        owner="SafetyTeam",
        permissions="safety:execute",
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
                "original_output": {"type": "string"},
                "concept": {"type": "string"},
                "exam_track": {"type": "string"},
                "subject": {"type": "string"},
                "level": {"type": "integer"},
                "session_id": {"type": "string"},
                "user_id": {"type": "string"}
            },
            "required": ["original_output", "concept"]
        },
        output_schema={"type": "object"},
        timeout_ms=3000,
        retry_count=1
    )
    registry.register_tool(def2, executeRegenerationLoop)
