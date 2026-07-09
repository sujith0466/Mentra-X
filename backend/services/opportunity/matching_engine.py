"""
Mentra X — Student Matching & Explainability Engine (Phase 10 Module 3)

Computes multi-factor match percentage (0-100%) and detailed explainability
for why each opportunity was recommended or penalized.
"""

from typing import List, Dict, Any, Set
from backend.services.opportunity.dto import (
    OpportunityItemDTO,
    MatchedOpportunityDTO,
    MatchExplanationDTO
)


class StudentMatchingEngine:
    """
    Evaluates student profile vectors against opportunity requirements
    and generates explainable match scoring.
    """

    def match_opportunity(
        self,
        opportunity: OpportunityItemDTO,
        student_skills: List[str],
        habit_score: float,
        ats_score: float,
        completed_courses_count: int
    ) -> MatchedOpportunityDTO:
        explanations: List[MatchExplanationDTO] = []
        student_skills_lower: Set[str] = {s.strip().lower() for s in student_skills}

        # Base score starting at 50.0
        score = 50.0

        # 1. Skill Overlap Analysis (Up to +35%)
        req_skills = opportunity.required_skills or []
        if req_skills:
            matched_skills = [s for s in req_skills if s.strip().lower() in student_skills_lower]
            missing_skills = [s for s in req_skills if s.strip().lower() not in student_skills_lower]
            ratio = len(matched_skills) / len(req_skills)

            skill_delta = round(ratio * 35.0, 1)
            score += skill_delta
            if matched_skills:
                explanations.append(
                    MatchExplanationDTO(
                        factor="Skill Alignment",
                        impact="POSITIVE",
                        detail=f"Strong proficiency in {', '.join(matched_skills)} (+{skill_delta}%)",
                        score_delta=skill_delta
                    )
                )
            if missing_skills:
                penalty = round(len(missing_skills) * 5.0, 1)
                score = max(10.0, score - penalty)
                explanations.append(
                    MatchExplanationDTO(
                        factor="Prerequisite Gap",
                        impact="NEGATIVE",
                        detail=f"Missing required skills: {', '.join(missing_skills)} (-{penalty}%)",
                        score_delta=-penalty
                    )
                )
        else:
            explanations.append(
                MatchExplanationDTO(
                    factor="Open Skill Eligibility",
                    impact="POSITIVE",
                    detail="No rigid skill prerequisites required (+15%)",
                    score_delta=15.0
                )
            )
            score += 15.0

        # 2. Autonomous Habit Score & Consistency Analysis (+15%)
        if habit_score >= 80.0:
            explanations.append(
                MatchExplanationDTO(
                    factor="Autonomous Learning Consistency",
                    impact="POSITIVE",
                    detail=f"High Habit Index ({habit_score:.1f}/100) indicates strong follow-through (+12%)",
                    score_delta=12.0
                )
            )
            score += 12.0
        elif habit_score >= 65.0:
            explanations.append(
                MatchExplanationDTO(
                    factor="Learning Velocity",
                    impact="POSITIVE",
                    detail=f"Solid active study cadence ({habit_score:.1f}/100) (+6%)",
                    score_delta=6.0
                )
            )
            score += 6.0

        # 3. Resume ATS Readiness Contribution (+10%)
        if ats_score >= 75.0:
            explanations.append(
                MatchExplanationDTO(
                    factor="ATS Resume Strength",
                    impact="POSITIVE",
                    detail=f"Resume formatting and keyword density score {ats_score:.0f}/100 (+8%)",
                    score_delta=8.0
                )
            )
            score += 8.0

        # Clamp score between 15% and 98%
        final_match = max(15.0, min(98.0, round(score, 1)))

        # Determine Readiness Level
        if final_match >= 85.0:
            readiness = "IMMEDIATE_READY"
        elif final_match >= 70.0:
            readiness = "NEAR_READY"
        else:
            readiness = "TARGET_GOAL"

        return MatchedOpportunityDTO(
            opportunity=opportunity,
            match_percentage=final_match,
            readiness_level=readiness,
            explanations=explanations,
            lifecycle_status="RECOMMENDED"
        )
