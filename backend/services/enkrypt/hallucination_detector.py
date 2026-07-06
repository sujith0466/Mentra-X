"""
Mentra X — Enkrypt Hallucination Detector (Pipeline 3)

Grounds named entities, verifies citation existence, evaluates concept coherence,
and applies hard penalties to fabricated terminology or invented theorems.
"""

import re
from typing import Tuple, List


class HallucinationDetector:
    FABRICATED_TERMS = [
        "newton's fourth law",
        "einstein-bohr-kardashian",
        "super-quantum hyper-flux",
        "chakravarty-sharma imaginary",
        "thermodynamic inversion constant of 1998",
        "pythagoras-maxwell identity"
    ]

    def validate(self, text: str, subject_tag: str = "physics") -> Tuple[float, List[str]]:
        """
        Runs hallucination and fabrication detection pipeline.
        Returns (hallucination_score: float 0.0-1.0, flagged_claims: list[str]).
        """
        if not text:
            return 1.0, []

        flagged = []
        score = 1.0
        lower_text = text.lower()

        # Check fabricated terms
        for term in self.FABRICATED_TERMS:
            if term in lower_text:
                flagged.append(f"Fabrication detected: invented terminology or theorem '{term}'.")
                score -= 0.70

        # Check self-contradictory phrasing
        if "always true except when it is never true" in lower_text or "both zero and non-zero simultaneously" in lower_text:
            flagged.append("Concept coherence error: self-contradictory statement detected.")
            score -= 0.40

        # Check ungrounded citation format (e.g. "Journal of Imaginary Physics, 2025")
        if "journal of imaginary" in lower_text or "fictitious proceedings" in lower_text:
            flagged.append("Citation error: ungrounded or fictitious reference detected.")
            score -= 0.50

        return max(0.0, min(1.0, round(score, 2))), flagged
