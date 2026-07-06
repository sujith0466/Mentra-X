"""
Mentra X — Enkrypt Main Validator Orchestration (Phase 7 Layer 6)

Orchestrates the 4 validation pipelines (Math, Science, Hallucination, Pedagogy),
computes weighted composite confidence score, and determines safety action thresholds:
- confidence >= 0.90 -> APPROVE
- 0.70 <= confidence < 0.90 -> REGENERATE
- confidence < 0.70 -> HARD_FAIL
"""

from typing import List, Dict, Any
from backend.services.enkrypt.dto import ValidationResultDTO
from backend.services.enkrypt.math_validator import MathValidator
from backend.services.enkrypt.science_validator import ScienceFactValidator
from backend.services.enkrypt.hallucination_detector import HallucinationDetector
from backend.services.enkrypt.pedagogy_evaluator import PedagogyEvaluator


class EnkryptValidator:
    def __init__(self):
        self.math_val = MathValidator()
        self.sci_val = ScienceFactValidator()
        self.hal_val = HallucinationDetector()
        self.ped_val = PedagogyEvaluator()

    def validate(
        self,
        text: str,
        subject_tag: str = "physics",
        exam_track: str = "JEE",
        level: int = 1
    ) -> ValidationResultDTO:
        """
        Runs all 4 validation pipelines and returns composite ValidationResultDTO.
        """
        math_score, math_flags = self.math_val.validate(text, exam_track)
        sci_score, sci_flags = self.sci_val.validate(text, subject_tag)
        hal_score, hal_flags = self.hal_val.validate(text, subject_tag)
        ped_score, ped_flags = self.ped_val.validate(text, level, exam_track)

        composite = round(
            0.40 * math_score +
            0.30 * sci_score +
            0.20 * hal_score +
            0.10 * ped_score,
            3
        )

        all_flags: List[str] = math_flags + sci_flags + hal_flags + ped_flags

        if composite >= 0.90:
            action = "APPROVE"
            failure_context = ""
        elif 0.70 <= composite < 0.90:
            action = "REGENERATE"
            failure_context = f"Composite confidence {composite*100:.1f}% below 90% approval threshold. Issues identified: {'; '.join(all_flags)}"
        else:
            action = "HARD_FAIL"
            failure_context = f"Severe safety failure (confidence {composite*100:.1f}% < 70%). Issues: {'; '.join(all_flags)}"

        return ValidationResultDTO(
            math_score=math_score,
            science_score=sci_score,
            hallucination_score=hal_score,
            pedagogy_score=ped_score,
            composite_confidence=composite,
            flagged_claims=all_flags,
            recommended_action=action,
            failure_context=failure_context
        )
