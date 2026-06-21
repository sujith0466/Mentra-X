from services.ai.rulebased_chatbot_service import build_rulebased_chatbot_payload


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
    """Public entry point consumed by app.py /api/chatbot/ask.

    All requests now flow through the rule-based chatbot service.
    """
    context = context or {}
    return build_rulebased_chatbot_payload(
        question,
        context={
            "page": _normalize_page(context),
            "course": context.get("course"),
            "domain": context.get("domain"),
            "course_id": context.get("course_id"),
        },
        user_id=context.get("user_id"),
    )
