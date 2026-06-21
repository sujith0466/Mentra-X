from __future__ import annotations

from typing import Optional

from backend.services.ai.agents.base_agent import BaseAgent
from backend.services.ai.devtools.coding_practice_service import generate_coding_problem
from backend.services.ai.devtools.debug_service import explain_error


class DebugAgent(BaseAgent):
    agent_name = "debug"

    def handle(self, user_id: Optional[int], message: str, **kwargs):
        lowered = (message or "").lower()
        if any(
            token in lowered
            for token in ["error", "traceback", "typeerror", "valueerror", "syntaxerror", "indexerror", "keyerror", "exception", "bug", "debug"]
        ):
            debug_payload = explain_error(message)
            answer = f"{debug_payload['explanation']} Suggested fix: {debug_payload['possible_fix']}"
            return self.build_response(
                answer,
                suggestions=["Explain the stack trace", "Give me a simpler fix", "Show a similar coding problem"],
                data=debug_payload,
                intent=kwargs.get("intent", "coding_help"),
            )

        problem = generate_coding_problem("Python")
        answer = f"Practice problem: {problem['title']}. {problem['description']}"
        return self.build_response(
            answer,
            suggestions=["Give me a Python coding problem", "How do I fix this Python error?", "Explain my codebase"],
            data=problem,
            intent=kwargs.get("intent", "coding_help"),
        )
