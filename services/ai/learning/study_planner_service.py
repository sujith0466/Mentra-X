from __future__ import annotations

from math import ceil
from typing import Dict, List

from models import Course, CourseModule, Enrollment, LessonProgress, Quiz, QuizAttempt, Video
from services.ai.ml.learning_difficulty_model import detect_learning_difficulty
from services.ai.skills.skill_graph_service import get_skill_progress_snapshot


def _remaining_lessons(user_id: int, course_id: int) -> List[str]:
    modules = CourseModule.query.filter_by(course_id=course_id).order_by(CourseModule.order_index.asc(), CourseModule.id.asc()).all()
    lessons_query = Video.query.filter_by(course_id=course_id).order_by(Video.order_number.asc(), Video.id.asc()).all()
    completed_ids = {
        row.lesson_id
        for row in LessonProgress.query.filter_by(user_id=user_id, course_id=course_id, completed=True).all()
    }

    module_titles = {module.id: module.title for module in modules}
    remaining_lessons: List[str] = []
    for lesson in lessons_query:
        if lesson.id in completed_ids:
            continue
        module_prefix = ""
        if lesson.module_id and lesson.module_id in module_titles:
            module_prefix = f"{module_titles[lesson.module_id]}: "
        remaining_lessons.append(f"{module_prefix}{lesson.title}")
    return remaining_lessons


def generate_study_plan(user_id: int, course_id: int, days: int) -> Dict[str, object]:
    enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
    course = Course.query.get_or_404(course_id)
    total_days = max(1, int(days or 1))

    if not enrollment:
        return {"course": course.title, "days": []}

    remaining_lessons = _remaining_lessons(user_id, course_id)

    if not remaining_lessons:
        return {
            "course": course.title,
            "days": [{"day": 1, "lessons": ["Course already completed. Use Smart Revision to revisit key topics."]}],
        }

    lessons_per_day = max(1, ceil(len(remaining_lessons) / total_days))
    planned_days = []
    for index in range(total_days):
        start = index * lessons_per_day
        end = start + lessons_per_day
        day_lessons = remaining_lessons[start:end]
        if not day_lessons:
            break
        planned_days.append({"day": index + 1, "lessons": day_lessons})

    return {"course": course.title, "days": planned_days}


def generate_adaptive_study_plan(user_id: int, course_id: int) -> Dict[str, object]:
    course = Course.query.get_or_404(course_id)
    remaining_lessons = _remaining_lessons(user_id, course_id)
    difficulty = detect_learning_difficulty(user_id)
    weak_topics = difficulty.get("weak_topics", [])

    if not remaining_lessons:
        return {
            "course": course.title,
            "days": [{"day": 1, "lessons": ["You have completed the course. Focus on revision, quizzes, and weak topics."]}],
            "mode": "adaptive",
        }

    if len(weak_topics) >= 3:
        total_days = max(5, len(remaining_lessons))
        lessons_per_day = 1
    elif len(weak_topics) >= 1:
        total_days = max(4, ceil(len(remaining_lessons) / 2))
        lessons_per_day = 2
    else:
        total_days = max(3, ceil(len(remaining_lessons) / 3))
        lessons_per_day = 3

    planned_days = []
    for index in range(total_days):
        start = index * lessons_per_day
        end = start + lessons_per_day
        day_lessons = remaining_lessons[start:end]
        if not day_lessons:
            break
        if index == 0 and weak_topics:
            day_lessons = day_lessons + [f"Revision focus: {weak_topics[0]}"]
        planned_days.append({"day": index + 1, "lessons": day_lessons})

    return {
        "course": course.title,
        "days": planned_days,
        "mode": "adaptive",
        "weak_topics": weak_topics[:3],
    }


def generate_adaptive_learning_path(user_id: int) -> Dict[str, object]:
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    difficulty = detect_learning_difficulty(user_id)
    weak_topics = difficulty.get("weak_topics", [])
    recommended_lessons: List[str] = []
    recommended_quizzes: List[str] = []
    revision_topics: List[str] = list(difficulty.get("recommended_revision", []))

    for enrollment in enrollments:
        if not enrollment.course:
            continue
        remaining = _remaining_lessons(user_id, enrollment.course_id)
        recommended_lessons.extend(remaining[:2])

        if weak_topics:
            quiz_rows = Quiz.query.filter_by(course_id=enrollment.course_id).order_by(Quiz.created_at.desc()).limit(2).all()
            recommended_quizzes.extend([quiz.title for quiz in quiz_rows])

        attempts = QuizAttempt.query.join(Quiz, QuizAttempt.quiz_id == Quiz.id).filter(
            QuizAttempt.user_id == user_id,
            Quiz.course_id == enrollment.course_id,
        ).all()
        if any((attempt.score_percentage or 0) < 60 for attempt in attempts):
            revision_topics.append(f"Extra revision suggested for {enrollment.course.title} due to low quiz performance.")

    low_skill_rows = [row for row in get_skill_progress_snapshot(user_id) if row.get("progress_percentage", 0) < 60]
    for row in low_skill_rows[:3]:
        revision_topics.append(f"Strengthen {row['skill_name']} by revisiting its linked modules.")

    return {
        "recommended_lessons": list(dict.fromkeys(recommended_lessons))[:6],
        "recommended_quizzes": list(dict.fromkeys(recommended_quizzes))[:6],
        "revision_topics": list(dict.fromkeys(revision_topics))[:6],
    }
