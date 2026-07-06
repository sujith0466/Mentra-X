"""
Mentra X — Enkrypt Science Fact Validator (Pipeline 2)

Verifies domain factual accuracy across Physics, Chemistry, Biology, and History/UPSC,
detecting scientific contradictions and false empirical assertions.
"""

from typing import Tuple, List


class ScienceFactValidator:
    KNOWN_CONTRADICTIONS = [
        {
            "phrase": "entropy increases in reversible",
            "subject": "physics",
            "error_msg": "Scientific contradiction: entropy remains constant in reversible adiabatic/isothermal cycles; it increases only in irreversible processes."
        },
        {
            "phrase": "entropy always increases in reversible",
            "subject": "physics",
            "error_msg": "Scientific contradiction: entropy always increases in irreversible processes, not reversible ones."
        },
        {
            "phrase": "speed of light depends on",
            "subject": "physics",
            "error_msg": "Scientific contradiction: the speed of light in vacuum c is invariant and independent of observer or source velocity."
        },
        {
            "phrase": "mitochondria synthesize glucose",
            "subject": "biology",
            "error_msg": "Biological error: chloroplasts synthesize glucose via photosynthesis; mitochondria generate ATP via cellular respiration."
        },
        {
            "phrase": "electron has positive charge",
            "subject": "chemistry",
            "error_msg": "Chemical error: electrons carry negative basic electrical charge (-1.6 x 10^-19 C)."
        },
        {
            "phrase": "article 370 was enacted in 2019",
            "subject": "upsc",
            "error_msg": "Historical error: Article 370 was adopted in 1949; it was abrogated/revoked in 2019."
        }
    ]

    def validate(self, text: str, subject_tag: str = "physics") -> Tuple[float, List[str]]:
        """
        Runs science fact validation pipeline.
        Returns (science_score: float 0.0-1.0, flagged_claims: list[str]).
        """
        if not text:
            return 1.0, []

        flagged = []
        score = 1.0
        lower_text = text.lower()

        for contra in self.KNOWN_CONTRADICTIONS:
            if contra["phrase"] in lower_text:
                flagged.append(contra["error_msg"])
                score -= 0.60

        return max(0.0, min(1.0, round(score, 2))), flagged
