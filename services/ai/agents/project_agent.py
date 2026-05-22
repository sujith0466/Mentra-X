from __future__ import annotations

from typing import Optional

from services.ai.agents.base_agent import BaseAgent
from services.ai.project_idea_service import generate_project_ideas, normalize_domain
from services.ai.projects.project_blueprint_service import generate_project_blueprint
from services.ai.projects.project_progress_service import get_recent_student_projects


DOMAIN_KEYWORDS = ["AI", "Web Development", "Python", "Data Science", "Machine Learning", "Cybersecurity", "Mobile Apps"]


def infer_domain(message: str, domain: Optional[str]) -> str:
    if domain:
        return normalize_domain(domain)
    lowered = (message or "").lower()
    for label in DOMAIN_KEYWORDS:
        if label.lower() in lowered:
            return normalize_domain(label)
    return "AI"


class ProjectAgent(BaseAgent):
    agent_name = "project"

    def handle(self, user_id: Optional[int], message: str, **kwargs):
        selected_domain = infer_domain(message, kwargs.get("domain"))
        ideas = generate_project_ideas(selected_domain, user_id=user_id)
        answer = f"Project ideas for {selected_domain}: " + "; ".join(item["title"] for item in ideas[:3]) + "."
        answer += " Open /student/projects to browse saved ideas or /student/projects/generate to create a new guided project."
        payload = {"ideas": ideas, "hub_link": "/student/projects", "generate_link": "/student/projects/generate"}
        if ideas:
            payload["blueprint_preview"] = generate_project_blueprint(ideas[0]["title"], selected_domain, "Intermediate")
        if user_id:
            payload["recent_projects"] = [
                {
                    "id": item.id,
                    "progress_percentage": item.progress_percentage,
                    "title": item.project_idea.title if item.project_idea else "Project",
                }
                for item in get_recent_student_projects(user_id)
            ]
        return self.build_response(
            answer,
            suggestions=["Generate a new project", "How do I build a portfolio?", "Recommend courses for this domain"],
            data=payload,
            intent=kwargs.get("intent", "project_ideas"),
        )
