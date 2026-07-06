"""
Mentra X — Enkrypt Regeneration Loop (Phase 7 Layer 6)

Controls the automated refinement loop when Tutor Agent outputs fail initial Enkrypt validation.
Attempts up to 2 revisions by attaching Enkrypt failure contexts to the prompt.
If double failure occurs, serves human-authored textbook fallback content and raises an HITL flag.
"""

from typing import Callable, Any
from backend.services.enkrypt.dto import ValidationResultDTO, RegenerationResultDTO
from backend.services.enkrypt.enkrypt_validator import EnkryptValidator
from backend.services.enkrypt.textbook_fallback import TextbookFallbackService


class RegenerationLoop:
    MAX_ATTEMPTS = 2

    def __init__(self):
        self.validator = EnkryptValidator()
        self.fallback_service = TextbookFallbackService()

    def execute(
        self,
        original_output: str,
        initial_validation: ValidationResultDTO,
        tutor_generator_fn: Callable[[str], str],
        concept: str,
        exam_track: str = "JEE",
        subject: str = "physics",
        level: int = 1
    ) -> RegenerationResultDTO:
        """
        Executes the up-to-2-attempt regeneration loop.
        tutor_generator_fn is a callback that takes a prompt instruction and returns a new AI string.
        """
        if initial_validation.recommended_action == "APPROVE":
            return RegenerationResultDTO(
                final_output=original_output,
                validation_result=initial_validation,
                attempts_used=0,
                was_fallback_served=False,
                hitl_flagged=False
            )

        current_val = initial_validation
        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            if attempt == 1:
                instruction = f"Previous response failed Enkrypt safety audit: {current_val.failure_context}. Please revise explanation for {concept} at Level {level} with strict scientific and mathematical accuracy."
            else:
                instruction = f"CRITICAL REVISION (Attempt {attempt}): {current_val.failure_context}. You MUST ensure zero formula errors, proper SI unit conversions (e.g. 5/18), and no fabricated terms."

            try:
                new_output = tutor_generator_fn(instruction)
            except Exception:
                new_output = ""

            if not new_output:
                break

            current_val = self.validator.validate(new_output, subject, exam_track, level)
            if current_val.recommended_action == "APPROVE" or current_val.composite_confidence >= 0.90:
                return RegenerationResultDTO(
                    final_output=f"{new_output}\n\n[Enkrypt Verified after refinement]",
                    validation_result=current_val,
                    attempts_used=attempt,
                    was_fallback_served=False,
                    hitl_flagged=False
                )

        # Double failure or hard fail exhaustion -> Serve textbook fallback & flag HITL
        fallback = self.fallback_service.get_fallback(concept, exam_track, subject)
        fallback_text = f"{fallback.content_text}\n\nSource: {fallback.source}\n\n{fallback.tagline}"

        return RegenerationResultDTO(
            final_output=fallback_text,
            validation_result=current_val,
            attempts_used=self.MAX_ATTEMPTS,
            was_fallback_served=True,
            hitl_flagged=True
        )
