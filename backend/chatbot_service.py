"""
AI Learning Assistant for Mentra.
Preserves the existing import contract used by public chatbot routes.
All requests now flow through the rule-based chatbot service.
"""

from backend.services.ai.rulebased_chatbot_service import build_rulebased_chatbot_payload


class ContextAwareAIAssistant:
    """Compatibility wrapper around the rule-based page-aware router."""

    def __init__(self):
        self.conversation_history = []

    def get_response(self, user_message, course_id=None, domain=None, current_page=None, course_name=None, user_id=None):
        payload = build_rulebased_chatbot_payload(
            user_message,
            context={
                "page": current_page,
                "course": course_name,
                "domain": domain,
                "course_id": course_id,
            },
            user_id=user_id,
        )
        answer = str(payload.get("answer", "") or payload.get("response", ""))
        options = payload.get("options") or payload.get("suggestions") or []
        if options:
            answer += "\n\nSuggested next questions:\n" + "\n".join(f"- {item}" for item in options[:3])
        return answer


chatbot = ContextAwareAIAssistant()

