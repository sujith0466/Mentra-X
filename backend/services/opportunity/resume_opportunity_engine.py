"""
Mentra X — Resume Opportunity Engine (Phase 10 Module 5)

Reuses `backend.services.career.resume_improver` to evaluate student resume text
against opportunity keywords, computing ATS score, missing keywords, and actionable tips.
"""

from typing import List, Set
from backend.services.opportunity.dto import OpportunityItemDTO, ResumeReadinessDTO
from backend.services.career.resume_improver import improve_resume


class ResumeOpportunityEngine:
    """
    Analyzes student resume text against target opportunity requirements.
    """

    def evaluate_resume_for_opportunity(
        self,
        opportunity: OpportunityItemDTO,
        raw_resume_text: str,
        base_ats_score: float = 78.0
    ) -> ResumeReadinessDTO:
        # 1. Reuse existing resume improver heuristics to clean up & get suggestions
        cleaned_text = raw_resume_text or ""
        improver_result = improve_resume(cleaned_text)
        improved_text = improver_result.get("improved_text", cleaned_text)
        suggestions = improver_result.get("suggestions", [])

        # 2. Extract opportunity keywords
        req_skills = opportunity.required_skills or []
        resume_lower = improved_text.lower()

        matched_keywords: List[str] = []
        missing_keywords: List[str] = []

        for skill in req_skills:
            if skill.lower() in resume_lower:
                matched_keywords.append(skill)
            else:
                missing_keywords.append(skill)

        # 3. Calculate dynamic ATS alignment score
        if req_skills:
            keyword_ratio = len(matched_keywords) / len(req_skills)
            ats_score = round(base_ats_score * 0.7 + (keyword_ratio * 30.0), 1)
        else:
            ats_score = base_ats_score

        ats_score = max(20.0, min(99.0, ats_score))

        # 4. Formulate missing projects note
        if missing_keywords:
            missing_projects_note = (
                f"Consider adding a capstone project explicitly showcasing: {', '.join(missing_keywords)}."
            )
        else:
            missing_projects_note = "Your projects strongly reflect all primary target keywords."

        # Ensure we always provide rich actionable bullet tips
        final_suggestions = list(suggestions)
        if missing_keywords:
            final_suggestions.append(
                f"Embed targeted bullet points featuring keywords: {', '.join(missing_keywords)}."
            )
        if not final_suggestions:
            final_suggestions.append("Quantify project impact metrics (e.g., 'Reduced latency by 45%').")

        return ResumeReadinessDTO(
            opportunity_id=opportunity.opportunity_id,
            ats_score=ats_score,
            matched_keywords=matched_keywords,
            missing_keywords=missing_keywords,
            suggested_improvements=final_suggestions,
            missing_projects_note=missing_projects_note
        )
