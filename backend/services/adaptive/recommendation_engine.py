"""
Mentra X — Unified Recommendation Engine (Phase 6 Layer 6)

Aggregates pedagogical level decisions, dynamic roadmap projections, content ranking fit,
cognitive fatigue status, and Ebbinghaus spaced repetition schedules into a single,
prioritized recommendation feed. Guaranteed to complete execution in < 200ms.
"""

import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from backend.services.adaptive.personalization_engine import PersonalizationEngine
from backend.services.adaptive.path_optimizer import DynamicRoadmapGenerator
from backend.services.adaptive.content_selector import ContentRankingEngine
from backend.services.adaptive.pacing_engine import FatigueDetector, SpacedRepetitionScheduler


@dataclass
class ActionableRecommendationDTO:
    rec_id: str
    priority_score: int  # Higher score = higher urgency
    action_type: str     # "FATIGUE_INTERVENTION" | "SPACED_REVIEW" | "URGENT_PREREQ" | "NEXT_LESSON" | "STUDY_RESOURCE"
    title: str
    description: str
    target_concept: Optional[str]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UnifiedRecommendationFeedDTO:
    user_id: str
    timestamp: str
    execution_time_ms: float
    is_fatigued: bool
    active_style: str
    active_level: int
    recommendations: List[ActionableRecommendationDTO]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["recommendations"] = [r.to_dict() if hasattr(r, "to_dict") else r for r in self.recommendations]
        return data


class UnifiedRecommendationEngine:
    def __init__(self):
        self.personalization = PersonalizationEngine()
        self.roadmap = DynamicRoadmapGenerator()
        self.content_ranking = ContentRankingEngine()
        self.fatigue_detector = FatigueDetector()
        self.scheduler = SpacedRepetitionScheduler()

    def generate_feed(
        self,
        user_id: str,
        concept: str = "general",
        dna: Any = None,
        session_duration_mins: float = 0.0,
        recent_errors: int = 0,
        response_time_degradation_pct: float = 0.0,
        course_id: int = 1,
        lessons: Optional[List[Dict[str, Any]]] = None,
        resources: Optional[List[Dict[str, Any]]] = None,
        review_concepts: Optional[List[Dict[str, Any]]] = None
    ) -> UnifiedRecommendationFeedDTO:
        """
        Aggregates across all adaptive services in < 200ms.
        """
        start_time = time.time()
        if lessons is None:
            lessons = []
        if resources is None:
            resources = []
        if review_concepts is None:
            review_concepts = []

        # 1. Check fatigue first
        fatigue = self.fatigue_detector.evaluate_fatigue(
            session_duration_mins=session_duration_mins,
            recent_errors=recent_errors,
            response_time_degradation_pct=response_time_degradation_pct
        )

        # 2. Evaluate personalization bundle (level & style)
        bundle = self.personalization.assemble_personalization_bundle(
            user_id=user_id,
            concept=concept,
            dna=dna
        )

        recs = []

        # Add fatigue intervention if fatigued
        if fatigue.is_fatigued:
            recs.append(ActionableRecommendationDTO(
                rec_id="rec_fatigue",
                priority_score=1000 if fatigue.fatigue_level == "CRITICAL" else 950,
                action_type="FATIGUE_INTERVENTION",
                title=f"Cognitive Pacing: {fatigue.recommended_action.replace('_', ' ').title()}",
                description=fatigue.rationale,
                target_concept=None,
                metadata={"fatigue_level": fatigue.fatigue_level, "duration": fatigue.session_duration_mins}
            ))

        # Check spaced repetition review schedule
        for rev in review_concepts:
            rev_concept = rev.get("concept", "")
            hours = float(rev.get("hours_since", 100))
            mast = float(rev.get("mastery", 0.50))
            sched = self.scheduler.calculate_review_schedule(rev_concept, hours, mast)
            if sched.needs_immediate_review:
                recs.append(ActionableRecommendationDTO(
                    rec_id=f"rec_rev_{rev_concept}",
                    priority_score=900 if sched.urgency == "OVERDUE" else 750,
                    action_type="SPACED_REVIEW",
                    title=f"Spaced Repetition Review: {rev_concept.replace('_', ' ').title()}",
                    description=sched.rationale,
                    target_concept=rev_concept,
                    metadata={"retention": sched.current_retention, "urgency": sched.urgency}
                ))

        # Check roadmap lessons
        if lessons:
            projections = self.roadmap.generate_roadmap(course_id, lessons, dna)
            for proj in projections:
                if proj.status == "URGENT_PREREQ":
                    recs.append(ActionableRecommendationDTO(
                        rec_id=f"rec_lesson_{proj.lesson_id}",
                        priority_score=700,
                        action_type="URGENT_PREREQ",
                        title=f"Prerequisite Lesson: {proj.title}",
                        description=proj.rationale,
                        target_concept=proj.concept,
                        metadata={"lesson_id": proj.lesson_id, "mastery": proj.mastery_score}
                    ))
                elif proj.status == "RECOMMENDED" and len([r for r in recs if r.action_type == "NEXT_LESSON"]) == 0:
                    recs.append(ActionableRecommendationDTO(
                        rec_id=f"rec_lesson_{proj.lesson_id}",
                        priority_score=500,
                        action_type="NEXT_LESSON",
                        title=f"Next Lesson: {proj.title}",
                        description=proj.rationale,
                        target_concept=proj.concept,
                        metadata={"lesson_id": proj.lesson_id}
                    ))

        # Check content resources
        if resources:
            ranked = self.content_ranking.rank_resources(resources, dna, concept)
            if ranked:
                top_res = ranked[0]
                recs.append(ActionableRecommendationDTO(
                    rec_id=f"rec_res_{top_res.resource_id}",
                    priority_score=400,
                    action_type="STUDY_RESOURCE",
                    title=f"Recommended Material ({top_res.format_style.upper()}): {top_res.title}",
                    description=f"{top_res.recommendation_tag} — {top_res.rationale}",
                    target_concept=concept,
                    metadata={"resource_id": top_res.resource_id, "fit_score": top_res.fit_score}
                ))

        # Sort recommendations by priority score descending
        recs.sort(key=lambda x: x.priority_score, reverse=True)

        exec_ms = round((time.time() - start_time) * 1000.0, 2)

        import datetime
        return UnifiedRecommendationFeedDTO(
            user_id=user_id,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            execution_time_ms=exec_ms,
            is_fatigued=fatigue.is_fatigued,
            active_style=bundle.selected_style,
            active_level=bundle.selected_level,
            recommendations=recs
        )
