import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ConfidenceResult:
    def __init__(
        self,
        confidence_score: float,
        uncertainty_score: float,
        explanation: str,
        signal_breakdown: Dict[str, float]
    ):
        self.confidence_score = round(max(0.0, min(1.0, confidence_score)), 2)
        self.uncertainty_score = round(max(0.0, min(1.0, uncertainty_score)), 2)
        self.explanation = explanation
        self.signal_breakdown = signal_breakdown

    def to_dict(self) -> Dict[str, Any]:
        return {
            "confidence_score": self.confidence_score,
            "uncertainty_score": self.uncertainty_score,
            "explanation": self.explanation,
            "signal_breakdown": self.signal_breakdown
        }


class ConfidenceEngine:
    """
    Computes AI response confidence (0.00-1.00) using multiple signals:
    retrieval similarity, assessment confidence, digital twin completeness,
    retrieved memory count, verification score, and prompt evaluation score.
    """
    # Signal weighting configuration
    WEIGHTS = {
        "retrieval_similarity": 0.20,
        "assessment_confidence": 0.20,
        "twin_completeness": 0.15,
        "memory_density": 0.10,
        "verification_score": 0.25,
        "prompt_eval_score": 0.10,
    }

    @classmethod
    def calculate_confidence(
        cls,
        retrieval_similarity: float = 0.85,
        assessment_confidence: float = 0.80,
        twin_completeness: float = 0.75,
        retrieved_memory_count: int = 3,
        verification_score: float = 0.95,
        prompt_eval_score: float = 0.90
    ) -> ConfidenceResult:
        # Normalize memory density (0 to 5+ memories mapped to 0.0 - 1.0)
        memory_density = min(1.0, retrieved_memory_count / 5.0)
        
        signals = {
            "retrieval_similarity": max(0.0, min(1.0, retrieval_similarity)),
            "assessment_confidence": max(0.0, min(1.0, assessment_confidence)),
            "twin_completeness": max(0.0, min(1.0, twin_completeness)),
            "memory_density": round(memory_density, 2),
            "verification_score": max(0.0, min(1.0, verification_score)),
            "prompt_eval_score": max(0.0, min(1.0, prompt_eval_score)),
        }

        # Weighted sum
        total_score = sum(signals[k] * cls.WEIGHTS[k] for k in cls.WEIGHTS)
        uncertainty = 1.0 - total_score

        # Generate narrative explanation
        reasons = []
        if signals["verification_score"] >= 0.90:
            reasons.append("verification checks passed with high certainty")
        if signals["retrieval_similarity"] >= 0.80:
            reasons.append("semantic memory retrieval found strong contextual matches")
        if signals["assessment_confidence"] >= 0.75:
            reasons.append("student assessment mastery data is well-established")
        if signals["twin_completeness"] < 0.50:
            reasons.append("note that Digital Twin profile is partially incomplete")
        
        if not reasons:
            reasons.append("multiple baseline AI indicators were evaluated")
            
        explanation_str = f"Confidence is computed at {total_score:.2f} because " + "; ".join(reasons) + "."

        return ConfidenceResult(
            confidence_score=total_score,
            uncertainty_score=uncertainty,
            explanation=explanation_str,
            signal_breakdown=signals
        )
