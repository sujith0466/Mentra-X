from services.ai.assistant_service import mentor_assistant


def _normalize_page(context):
    page = (context or {}).get("page", "")
    page = (page or "").lower()
    if "home" in page:
        return "homepage"
    if "dashboard" in page:
        return "dashboard"
    if "course" in page:
        return "course"
    return "general"


def get_chatbot_response(question, context=None):
    context = context or {}
    return mentor_assistant(
        context.get("user_id"),
        question,
        current_page=_normalize_page(context),
        course_name=context.get("course"),
        domain=context.get("domain"),
    )
