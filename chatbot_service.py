"""
AI Learning Assistant for Mentra.
Preserves the existing import contract used by public chatbot routes.
"""

from services.ai.assistant_service import mentor_assistant


class ContextAwareAIAssistant:
    """Compatibility wrapper around the upgraded assistant router."""

    def __init__(self):
        self.conversation_history = []

    def get_response(self, user_message, course_id=None, domain=None, current_page=None, course_name=None, user_id=None):
        payload = mentor_assistant(
            user_id,
            user_message,
            current_page=current_page,
            course_name=course_name,
            domain=domain,
        )
        answer = str(payload.get("answer", ""))
        options = payload.get("options") or []
        if options:
            answer += "\n\nSuggested next questions:\n" + "\n".join(f"- {item}" for item in options[:3])
        return answer


chatbot = ContextAwareAIAssistant()
