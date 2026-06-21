from __future__ import annotations

from typing import Optional

from backend.services.ai.agents.base_agent import BaseAgent
from backend.services.ai.mentor_service import mentor_service


class MentorAgent(BaseAgent):
    agent_name = "mentor"

    def handle(self, user_id: Optional[int], message: str, **kwargs):
        fallback = mentor_service.get_structured_response(
            message,
            current_page=kwargs.get("current_page"),
            course_name=kwargs.get("course_name"),
            domain=kwargs.get("domain"),
        )
        return self.build_response(
            fallback.get("answer", ""),
            suggestions=fallback.get("options", []),
            data=fallback.get("context", {}) if isinstance(fallback.get("context"), dict) else {},
            intent=kwargs.get("intent", "general"),
        )
