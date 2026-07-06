"""
Mentra X — Dynamic Roadmap Generator / Path Optimizer (Phase 6 Layer 6)

Provides dynamic curriculum sequencing that projects an optimized, personalized study
order over static LMS course syllabi. Re-orders incomplete lessons based on real-time
concept mastery vectors without mutating core relational enrollment tables.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class LessonProjectionDTO:
    lesson_id: int
    title: str
    concept: str
    original_order: int
    recommended_order: int
    mastery_score: float
    status: str  # "URGENT_PREREQ" | "RECOMMENDED" | "OPTIONAL_REVIEW" | "COMPLETED"
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DynamicRoadmapGenerator:
    def generate_roadmap(
        self,
        course_id: int,
        lessons: List[Dict[str, Any]],
        dna: Any,
        completed_lesson_ids: Optional[List[int]] = None
    ) -> List[LessonProjectionDTO]:
        """
        Re-orders course lessons based on student mastery:
        - Incomplete lessons with concept mastery < 0.60 move to top ("URGENT_PREREQ")
        - Incomplete lessons with mastery 0.60 - 0.85 are "RECOMMENDED"
        - Incomplete lessons with mastery >= 0.85 move to end ("OPTIONAL_REVIEW")
        - Completed lessons stay in place or move to bottom ("COMPLETED")
        """
        if completed_lesson_ids is None:
            completed_lesson_ids = []

        dna_dict = dna if isinstance(dna, dict) else getattr(dna, "__dict__", {})
        if not isinstance(dna_dict, dict):
            try:
                dna_dict = dna.to_dict()
            except Exception:
                dna_dict = {}

        mastery_map = dna_dict.get("mastery_per_concept", {})
        if not isinstance(mastery_map, dict):
            mastery_map = {}

        projections = []
        for idx, lesson in enumerate(lessons):
            if not isinstance(lesson, dict):
                continue

            l_id = int(lesson.get("id") or lesson.get("lesson_id") or (idx + 1))
            title = lesson.get("title", f"Lesson {l_id}")
            concept = lesson.get("concept") or lesson.get("topic") or title.lower().replace(" ", "_")
            orig_order = int(lesson.get("order") or lesson.get("sequence") or (idx + 1))

            mastery = float(mastery_map.get(concept, 0.50))
            is_completed = l_id in completed_lesson_ids or lesson.get("completed") is True

            if is_completed:
                status = "COMPLETED"
                rationale = "Lesson already completed."
                priority_weight = 1000 + orig_order
            elif mastery < 0.60:
                status = "URGENT_PREREQ"
                rationale = f"Foundational concept '{concept}' mastery is low ({mastery:.2f} < 0.60). Prioritized for review."
                priority_weight = 100 + int(mastery * 100)
            elif mastery >= 0.85:
                status = "OPTIONAL_REVIEW"
                rationale = f"High mastery achieved ({mastery:.2f}). You may skip or review lightly."
                priority_weight = 500 + orig_order
            else:
                status = "RECOMMENDED"
                rationale = f"Standard sequence progression (mastery: {mastery:.2f})."
                priority_weight = 200 + orig_order

            projections.append({
                "lesson_id": l_id,
                "title": title,
                "concept": concept,
                "original_order": orig_order,
                "mastery_score": mastery,
                "status": status,
                "rationale": rationale,
                "weight": priority_weight
            })

        # Sort by priority weight
        projections.sort(key=lambda x: x["weight"])

        # Create typed DTOs with updated recommended_order
        result_dtos = []
        for new_idx, item in enumerate(projections):
            dto = LessonProjectionDTO(
                lesson_id=item["lesson_id"],
                title=item["title"],
                concept=item["concept"],
                original_order=item["original_order"],
                recommended_order=new_idx + 1,
                mastery_score=item["mastery_score"],
                status=item["status"],
                rationale=item["rationale"]
            )
            result_dtos.append(dto)

        return result_dtos
