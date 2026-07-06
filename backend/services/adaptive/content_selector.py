"""
Mentra X — Content Ranking & Selection Engine (Phase 6 Layer 6)

Automates study material ranking by scoring candidate learning resources against student
preferred cognitive style, concept mastery level, and historical Qdrant interaction outcomes.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class RankedResourceDTO:
    resource_id: str
    title: str
    format_style: str
    difficulty: float
    fit_score: float
    rank: int
    recommendation_tag: str
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ContentRankingEngine:
    STYLE_FORMAT_MAP = {
        "Visual": {"diagram", "video", "interactive", "infographic", "chart", "visual_analogy"},
        "Mathematical": {"formula", "step_by_step", "equation", "proof", "code_derivation"},
        "Narrative": {"article", "story", "podcast", "conceptual_text", "case_study"}
    }

    def rank_resources(
        self,
        resources: List[Dict[str, Any]],
        dna: Any,
        concept: str = "",
        failed_resource_ids: Optional[List[str]] = None
    ) -> List[RankedResourceDTO]:
        """
        Scores and ranks learning resources based on student DNA and failure avoidance.
        """
        if failed_resource_ids is None:
            failed_resource_ids = []
        failed_set = set(str(r) for r in failed_resource_ids)

        dna_dict = dna if isinstance(dna, dict) else getattr(dna, "__dict__", {})
        if not isinstance(dna_dict, dict):
            try:
                dna_dict = dna.to_dict()
            except Exception:
                dna_dict = {}

        adaptive_traits = dna_dict.get("adaptive_traits", {})
        preferred_style = adaptive_traits.get("preferred_style") or dna_dict.get("preferred_style") or "Default"
        mastery_map = dna_dict.get("mastery_per_concept", {})
        if not isinstance(mastery_map, dict):
            mastery_map = {}
        mastery = float(mastery_map.get(concept, 0.50))

        target_formats = self.STYLE_FORMAT_MAP.get(preferred_style, set())

        scored_items = []
        for idx, res in enumerate(resources):
            if not isinstance(res, dict):
                continue

            r_id = str(res.get("id") or res.get("resource_id") or f"res_{idx+1}")
            title = res.get("title", f"Resource {r_id}")
            fmt = str(res.get("format") or res.get("style") or "text").lower()
            diff = float(res.get("difficulty", 0.50))

            score = 50.0  # Base score
            rationale_parts = []

            # Check failure avoidance
            if r_id in failed_set:
                score -= 60.0
                rationale_parts.append("Penalized: previously associated with unsuccessful explanation attempt.")

            # Style alignment
            if fmt in target_formats or str(preferred_style).lower() in fmt:
                score += 35.0
                rationale_parts.append(f"Strong fit for your {preferred_style} learning style.")
            elif preferred_style != "Default":
                score += 10.0

            # Difficulty alignment (prefer resources close to student ability)
            diff_delta = abs(mastery - diff)
            if diff_delta <= 0.20:
                score += 20.0
                rationale_parts.append("Difficulty matches your current concept mastery.")
            elif diff_delta > 0.40:
                score -= 10.0
                rationale_parts.append("Difficulty is significantly higher or lower than your current ability.")

            if score >= 80.0:
                tag = f"Recommended for Your {preferred_style} Style" if preferred_style != "Default" else "Top Recommendation"
            elif score >= 50.0:
                tag = "Good Supplementary Resource"
            else:
                tag = "Optional / Challenging"

            scored_items.append({
                "resource_id": r_id,
                "title": title,
                "format_style": fmt,
                "difficulty": diff,
                "score": round(score, 1),
                "tag": tag,
                "rationale": " ".join(rationale_parts) or "Standard learning resource."
            })

        scored_items.sort(key=lambda x: x["score"], reverse=True)

        dtos = []
        for rank, item in enumerate(scored_items):
            dtos.append(RankedResourceDTO(
                resource_id=item["resource_id"],
                title=item["title"],
                format_style=item["format_style"],
                difficulty=item["difficulty"],
                fit_score=item["score"],
                rank=rank + 1,
                recommendation_tag=item["tag"],
                rationale=item["rationale"]
            ))

        return dtos
