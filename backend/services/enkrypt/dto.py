"""
Mentra X — Enkrypt Safety Layer DTOs (Phase 7)

Defines data transfer objects for validation results, regeneration outcomes,
and textbook fallback content.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field


@dataclass
class ValidationResultDTO:
    math_score: float            # 0.0–1.0
    science_score: float         # 0.0–1.0
    hallucination_score: float   # 0.0–1.0
    pedagogy_score: float        # 0.0–1.0
    composite_confidence: float  # Weighted composite (0.40*math + 0.30*sc + 0.20*hal + 0.10*ped)
    flagged_claims: List[str] = field(default_factory=list)
    recommended_action: str = "APPROVE"  # "APPROVE" | "REGENERATE" | "HARD_FAIL"
    failure_context: str = ""    # Attached to regeneration prompt

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FallbackContentDTO:
    concept_tag: str
    exam_track: str
    subject: str
    content_text: str
    source: str
    tagline: str = "Showing verified reference content. Our AI tutor will improve with more feedback."

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RegenerationResultDTO:
    final_output: str
    validation_result: ValidationResultDTO
    attempts_used: int
    was_fallback_served: bool
    hitl_flagged: bool

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if hasattr(self.validation_result, "to_dict"):
            data["validation_result"] = self.validation_result.to_dict()
        return data
