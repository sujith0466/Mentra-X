"""
Mentra X — Enkrypt Pedagogy Evaluator (Pipeline 4)

Evaluates explanation clarity, structural compliance with tutoring levels
(e.g., Level 2 step-by-step, Level 4 analogy), depth, and completeness.
Softest validator — never triggers hard failures independently.
"""

from typing import Tuple, List


class PedagogyEvaluator:
    def validate(self, text: str, level: int = 1, exam_track: str = "JEE") -> Tuple[float, List[str]]:
        """
        Runs pedagogical evaluation pipeline.
        Returns (pedagogy_score: float 0.0-1.0, flagged_claims: list[str]).
        """
        if not text:
            return 1.0, []

        flagged = []
        score = 1.0
        lower_text = text.lower()

        # Check structure for Level 2 (should have steps or practice cues)
        if level == 2:
            has_steps = any(kw in lower_text for kw in ("step", "first", "next", "try", "practice", "let's solve", "1)", "2)"))
            if not has_steps and len(text) > 50:
                flagged.append("Pedagogical structure note: Level 2 guided practice lacks step-by-step or interactive cues.")
                score -= 0.20

        # Check structure for Level 4 (should have analogy or remedial foundation)
        if level == 4:
            has_analogy = any(kw in lower_text for kw in ("analogy", "imagine", "like a", "think of", "basic", "foundation", "simply"))
            if not has_analogy and len(text) > 50:
                flagged.append("Pedagogical structure note: Level 4 remedial explanation lacks intuitive analogy or foundational framing.")
                score -= 0.20

        # Check for extreme brevity when explaining complex concepts
        if len(text.split()) < 5 and level != 1:
            flagged.append("Pedagogical depth note: explanation is overly brief.")
            score -= 0.15

        return max(0.0, min(1.0, round(score, 2))), flagged
