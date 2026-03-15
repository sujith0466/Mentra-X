from __future__ import annotations

from typing import Optional

from services.ai.agents.base_agent import BaseAgent
from services.ai.interview import get_recent_interview_sessions
from services.ai.interview.interview_question_service import SUPPORTED_INTERVIEW_ROLES


def infer_role(message: str) -> str:
    lowered = (message or "").lower()
    for role in SUPPORTED_INTERVIEW_ROLES:
        if role.lower() in lowered:
            return role
    return "Full Stack Developer"


class InterviewAgent(BaseAgent):
    agent_name = "interview"

    def handle(self, user_id: Optional[int], message: str, **kwargs):
        role = infer_role(message)
        answer = f"Interview preparation is ready for {role}. Open /student/interview to review past sessions or /student/interview/start to launch a mock interview."
        data = {"hub_link": "/student/interview", "start_link": "/student/interview/start"}
        if user_id:
            recent = get_recent_interview_sessions(user_id)
            if recent:
                answer += f" Your latest mock interview score was {int(recent[0].score)}% for {recent[0].role}."
                data["recent_session_link"] = f"/student/interview/result/{recent[0].id}"
        answer += " Coding interview mode reuses Mentra coding challenges with interview-style prompts and time limits."
        return self.build_response(
            answer,
            suggestions=["Start mock interview", "Prepare me for backend interview", "Show coding interview practice"],
            data=data,
            intent=kwargs.get("intent", "interview_preparation"),
        )
