from __future__ import annotations

from typing import Dict, Optional


class BaseAgent:
    agent_name = "base"

    def build_response(
        self,
        response: str,
        *,
        suggestions: Optional[list[str]] = None,
        data: Optional[Dict[str, object]] = None,
        intent: Optional[str] = None,
    ) -> Dict[str, object]:
        return {
            "agent": self.agent_name,
            "response": response,
            "suggestions": suggestions or [],
            "data": data or {},
            "intent": intent or self.agent_name,
        }

    def handle(self, user_id: Optional[int], message: str, **kwargs) -> Dict[str, object]:
        raise NotImplementedError
