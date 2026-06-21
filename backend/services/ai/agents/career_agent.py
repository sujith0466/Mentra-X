from __future__ import annotations

from typing import Optional

from backend.services.ai.agents.base_agent import BaseAgent
from backend.services.ai.career.resume_service import analyze_resume
from backend.services.ai.career.skill_gap_service import detect_skill_gap
from backend.services.ai.career_service import generate_career_roadmap


ROLE_KEYWORDS = [
    "Full Stack Developer",
    "Data Scientist",
    "AI Engineer",
    "Backend Developer",
    "Frontend Developer",
]


def infer_role(message: str) -> str:
    lowered = (message or "").lower()
    for role in ROLE_KEYWORDS:
        if role.lower() in lowered:
            return role
    return "Full Stack Developer"


class CareerAgent(BaseAgent):
    agent_name = "career"

    def handle(self, user_id: Optional[int], message: str, **kwargs):
        intent = kwargs.get("intent", "career_advice")

        if intent == "resume_help":
            sample_analysis = analyze_resume(message)
            answer = "Resume guidance: emphasize skills, project impact, and technologies used."
            if sample_analysis.get("missing_skills"):
                answer += " Missing areas to strengthen: " + ", ".join(sample_analysis["missing_skills"][:3]) + "."
            return self.build_response(
                answer,
                suggestions=["Open Resume Analyzer", "How do I build a portfolio?", "Show my skill gaps"],
                data=sample_analysis,
                intent=intent,
            )

        role = infer_role(message)
        roadmap = generate_career_roadmap(role)
        answer = f"Career guidance for {roadmap['role']}: focus on " + ", ".join(roadmap.get("skills", [])[:4]) + "."
        if user_id:
            gap = detect_skill_gap(user_id, roadmap["role"])
            missing = gap.get("skills_missing", [])[:3]
            if missing:
                answer += " Your current skill gaps include " + ", ".join(missing) + "."
            roadmap = {**roadmap, "skill_gap": gap}
        return self.build_response(
            answer,
            suggestions=["Create a career roadmap", "Show my skill gaps", "How do I improve my resume?"],
            data=roadmap,
            intent=intent,
        )
