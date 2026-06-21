from __future__ import annotations

from typing import Dict, List, Optional

from backend.models import Course, Enrollment
from backend.services.ai.mentor_service import mentor_service


PAGE_OPTIONS: Dict[str, List[str]] = {
    "homepage": [
        "Which course should I start with?",
        "Show beginner friendly tracks",
        "How do certificates work?",
    ],
    "courses": [
        "Recommend a course for beginners",
        "How should I pick the right domain?",
        "Which course has projects?",
    ],
    "course": [
        "What should I complete first in this course?",
        "How do quizzes and assignments help?",
        "What project can I build after this course?",
    ],
    "dashboard": [
        "How can I improve my progress this week?",
        "Recommend my next course",
        "How do I build a portfolio from my work?",
    ],
    "contact": [
        "How quickly does support reply?",
        "Where can I report a technical issue?",
        "How do I request course help?",
    ],
    "about": [
        "What makes Mentra different?",
        "How does the learning model work?",
        "How do referral rewards work?",
    ],
    "general": [
        "Give me study tips",
        "How do I practice coding better?",
        "How should I plan my career roadmap?",
    ],
}


def _normalize_page(page: Optional[str]) -> str:
    raw = (page or "").strip().lower()
    if not raw:
        return "general"
    if any(key in raw for key in ["home", "landing", "index"]):
        return "homepage"
    if any(key in raw for key in ["courses", "catalog", "browse_courses"]):
        return "courses"
    if any(key in raw for key in ["course_detail", "course_videos", "course"]):
        return "course"
    if "dashboard" in raw:
        return "dashboard"
    if "contact" in raw:
        return "contact"
    if "about" in raw:
        return "about"
    if "admin" in raw:
        return "general"
    return "general"


def _safe_int(value) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _load_course_context(course_id: Optional[int], course_name: Optional[str]) -> Optional[Dict[str, object]]:
    course = None
    if course_id:
        course = Course.query.get(course_id)
    if not course and course_name:
        course = Course.query.filter(Course.title.ilike(f"%{course_name.strip()}%")).order_by(Course.id.asc()).first()
    if not course:
        return None

    return {
        "id": course.id,
        "title": course.title,
        "domain": course.domain.name if course.domain else None,
        "instructor": course.instructor or "Mentra Faculty",
        "price": float(course.price or 0.0),
        "lesson_count": len(course.videos or []),
        "syllabus_count": len(course.syllabuses or []),
        "enrollment_count": Enrollment.query.filter_by(course_id=course.id).count(),
    }


def _page_prefix(page: str, course_ctx: Optional[Dict[str, object]]) -> str:
    if page == "homepage":
        return "You are on Mentra Home. I can help you choose the best starting path quickly."
    if page == "courses":
        return "You are in the Courses catalog. I can help you shortlist the right course by goal and level."
    if page == "course" and course_ctx:
        return (
            f"You are viewing {course_ctx['title']} in {course_ctx.get('domain') or 'General'}."
            f" It has {course_ctx['lesson_count']} lessons and {course_ctx['syllabus_count']} syllabus topics."
        )
    if page == "dashboard":
        return "You are on your student dashboard. I can guide your next action from progress and skills."
    if page == "contact":
        return "You are on Contact page. I can help you send the right support message faster."
    if page == "about":
        return "You are on About page. I can explain Mentra model, mission, and learner value."
    return "I can help with courses, progress, projects, coding practice, and career direction."


def _course_specific_response(message: str, course_ctx: Dict[str, object]) -> Optional[str]:
    text = (message or "").lower()
    if any(k in text for k in ["price", "cost", "free"]):
        if course_ctx["price"] > 0:
            return f"This course is priced at Rs. {course_ctx['price']:.0f}. You can enroll directly from the course page."
        return "This course is currently free. You can enroll directly from the course page."
    if any(k in text for k in ["syllabus", "topic", "module"]):
        return (
            f"{course_ctx['title']} includes {course_ctx['syllabus_count']} syllabus topics."
            " Start from topic 1, complete each lesson in order, then attempt the quiz and assignment."
        )
    if any(k in text for k in ["video", "lesson", "duration"]):
        return (
            f"{course_ctx['title']} currently has {course_ctx['lesson_count']} lessons."
            " Complete lessons sequentially for best progress tracking."
        )
    if any(k in text for k in ["enroll", "start course", "begin"]):
        return (
            f"To start {course_ctx['title']}, click Enroll Now. After enrollment, use Continue Learning"
            " to access lessons, quizzes, and assignments."
        )
    return None


def _user_learning_snapshot(user_id: Optional[int]) -> Optional[Dict[str, object]]:
    if not user_id:
        return None
    enrollments = (
        Enrollment.query
        .filter_by(user_id=user_id)
        .order_by(Enrollment.enrolled_date.desc())
        .all()
    )
    if not enrollments:
        return {
            "total_enrollments": 0,
            "completed_courses": 0,
            "in_progress_courses": 0,
            "top_course": None,
        }

    completed = 0
    in_progress = 0
    top_course = None
    top_progress = -1.0
    for row in enrollments:
        progress = float(row.progress_percentage or row.progress or 0.0)
        if row.completed or progress >= 100:
            completed += 1
        elif progress > 0:
            in_progress += 1
        if progress > top_progress and row.course:
            top_progress = progress
            top_course = row.course.title

    return {
        "total_enrollments": len(enrollments),
        "completed_courses": completed,
        "in_progress_courses": in_progress,
        "top_course": top_course,
    }


def _user_specific_response(message: str, snapshot: Dict[str, object]) -> Optional[str]:
    text = (message or "").lower()
    if any(k in text for k in ["my progress", "progress", "where am i", "status"]):
        return (
            f"You are enrolled in {snapshot['total_enrollments']} courses,"
            f" completed {snapshot['completed_courses']}, and currently in progress on {snapshot['in_progress_courses']}."
            + (f" Your strongest active course is {snapshot['top_course']}." if snapshot.get("top_course") else "")
        )
    if any(k in text for k in ["what next", "next step", "next course", "what should i do next"]):
        if snapshot["total_enrollments"] == 0:
            return "Start with one beginner-friendly course in your target domain, then complete the first 2 lessons today."
        if snapshot["in_progress_courses"] > 0 and snapshot.get("top_course"):
            return f"Best next step: continue {snapshot['top_course']} and complete one lesson + one quiz attempt today."
        return "Pick one new course aligned with your goal and follow module order to keep steady progress."
    if any(k in text for k in ["support", "contact", "helpdesk"]):
        return "For account, enrollment, or technical issues, open Contact page and submit a detailed message with screenshots if possible."
    return None


def build_rulebased_chatbot_payload(
    question: str,
    *,
    context: Optional[Dict[str, object]] = None,
    user_id: Optional[int] = None,
) -> Dict[str, object]:
    context = context or {}
    page = _normalize_page((context or {}).get("page"))
    course_name = (context or {}).get("course")
    domain = (context or {}).get("domain")
    course_id = _safe_int((context or {}).get("course_id"))

    course_ctx = _load_course_context(course_id, course_name)
    if course_ctx and not domain:
        domain = course_ctx.get("domain")
    if course_ctx and not course_name:
        course_name = course_ctx.get("title")
    snapshot = _user_learning_snapshot(user_id)

    page_hint = _page_prefix(page, course_ctx)
    special_response = _course_specific_response(question, course_ctx) if course_ctx else None
    user_response = _user_specific_response(question, snapshot) if snapshot else None

    mentor_payload = mentor_service.get_structured_response(
        question,
        current_page=page,
        course_name=course_name,
        domain=domain,
    )

    answer_core = user_response or special_response or mentor_payload.get("answer") or "I can help you with your next learning step."
    answer = f"{page_hint}\n\n{answer_core}".strip()

    options = list(PAGE_OPTIONS.get(page, PAGE_OPTIONS["general"]))
    mentor_options = mentor_payload.get("options") or []
    for item in mentor_options:
        if item not in options:
            options.append(item)
    if snapshot:
        for item in ["Show my progress summary", "What should I do next?", "Help me prioritize one course"]:
            if item not in options:
                options.append(item)
    options = options[:4]

    return {
        "answer": answer,
        "response": answer,
        "options": options,
        "suggestions": options,
        "agent": "rulebased_mentor",
        "intent": "rule_based",
        "page_context": page,
        "course_context": course_ctx,
        "user_id": user_id,
    }
