"""
Mentra X — Skill Gap Intelligence Engine (Phase 10 Module 4)

Produces structured skill bridge analytics:
Current Skills -> Missing Skills -> Learning Path -> Estimated Completion Time -> Expected Match Increase
"""

from typing import List, Set
from backend.services.opportunity.dto import OpportunityItemDTO, SkillGapDTO


class SkillGapEngine:
    """
    Computes exact missing skills and constructs a targeted remediation bridge.
    """

    def analyze_skill_gap(
        self,
        opportunity: OpportunityItemDTO,
        student_skills: List[str],
        current_match_pct: float
    ) -> SkillGapDTO:
        student_lower: Set[str] = {s.strip().lower() for s in student_skills}
        req_skills = opportunity.required_skills or []

        matched_skills = [s for s in req_skills if s.strip().lower() in student_lower]
        missing_skills = [s for s in req_skills if s.strip().lower() not in student_lower]

        learning_path_steps: List[str] = []
        estimated_days = 0

        for missing in missing_skills:
            clean = missing.strip()
            if clean.lower() in ["system design", "distributed systems"]:
                learning_path_steps.append(f"Complete 4-Module System Design & Load Balancing Path ({clean})")
                estimated_days += 6
            elif clean.lower() in ["docker", "kubernetes", "cloud architecture"]:
                learning_path_steps.append(f"Complete Containerization & Cloud Deployment Bootcamp ({clean})")
                estimated_days += 5
            elif clean.lower() in ["machine learning", "deep learning"]:
                learning_path_steps.append(f"Complete Practical Neural Networks & PyTorch Path ({clean})")
                estimated_days += 7
            else:
                learning_path_steps.append(f"Complete Accelerated Primer & Coding Exercises on {clean}")
                estimated_days += 3

        # Calculate expected match increase
        if not missing_skills:
            expected_after = current_match_pct
            estimated_days = 0
            learning_path_steps = ["All required competencies verified in your Digital Twin."]
        else:
            gain = min(98.0 - current_match_pct, len(missing_skills) * 8.5)
            expected_after = min(98.0, round(current_match_pct + gain, 1))

        return SkillGapDTO(
            opportunity_id=opportunity.opportunity_id,
            current_skills=matched_skills or student_skills[:4],
            missing_skills=missing_skills,
            learning_path_steps=learning_path_steps,
            estimated_readiness_days=estimated_days,
            current_match_pct=current_match_pct,
            expected_match_after_remediation_pct=expected_after
        )
