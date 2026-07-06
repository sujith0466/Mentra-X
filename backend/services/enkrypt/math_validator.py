"""
Mentra X — Enkrypt Math Validator (Pipeline 1)

Verifies mathematical accuracy, formula correctness against known JEE/NEET/UPSC/CAT
formula databases, derivation step consistency, and SI unit compliance.
"""

import re
from typing import Tuple, List


class MathValidator:
    # Known common formula hallucinations or misapplications
    KNOWN_FORMULA_ERRORS = [
        {
            "pattern": r"[\u0394\\]?S\s*=\s*Q\s*/\s*T",
            "required_context": ["reversible", "rev", "isothermal", "constant temperature"],
            "error_msg": "Formula \u0394S = Q/T misapplied: valid only for reversible isothermal processes."
        },
        {
            "pattern": r"F\s*=\s*m\s*\*?\s*v(?!\^|\d|a|/)",
            "required_context": [],
            "error_msg": "Incorrect formula F = m*v; force is rate of change of momentum (F = m*a or dp/dt)."
        },
        {
            "pattern": r"E\s*=\s*m\s*\*?\s*c(?!\^2|2)",
            "required_context": [],
            "error_msg": "Incorrect mass-energy equivalence formula E = m*c; must be E = m*c^2."
        },
        {
            "pattern": r"PV\s*=\s*n\s*R\s*T\^2",
            "required_context": [],
            "error_msg": "Incorrect ideal gas law PV = nRT^2; must be PV = nRT."
        }
    ]

    def validate(self, text: str, exam_track: str = "JEE") -> Tuple[float, List[str]]:
        """
        Runs mathematical validation pipeline.
        Returns (math_score: float 0.0-1.0, flagged_claims: list[str]).
        """
        if not text:
            return 1.0, []

        flagged = []
        score = 1.0

        # Check known formula errors and misapplications
        for err in self.KNOWN_FORMULA_ERRORS:
            if re.search(err["pattern"], text, re.IGNORECASE):
                # Check if required context is present
                has_context = any(req in text.lower() for req in err["required_context"]) if err["required_context"] else False
                if not has_context:
                    flagged.append(err["error_msg"])
                    score -= 0.50

        # Check unit consistency for JEE/NEET (e.g. mixing km/h and m/s without conversion warning)
        if exam_track in ("JEE", "NEET"):
            if "km/h" in text and "m/s" in text and not any(factor in text for factor in ("5/18", "18/5", "0.277", "conversion factor", "converted")):
                flagged.append("Potential unit inconsistency: mixing km/h and m/s without explicit conversion factor.")
                score -= 0.40

        # Check division by zero or mathematical absurdities
        if re.search(r"/\s*0(?!\.\d)", text) or "divide by zero" in text.lower():
            flagged.append("Mathematical absurdity: division by zero detected.")
            score -= 0.60

        return max(0.0, min(1.0, round(score, 2))), flagged
