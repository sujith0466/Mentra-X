from __future__ import annotations

from datetime import date, timedelta
from typing import Dict, List

from models import Course, Enrollment, LearningStreak, LessonProgress, QuizAttempt, Quiz, Video


def get_revision_topics(user_id: int) -> List[Dict[str, object]]:
    suggestions: List[Dict[str, object]] = []
    today = date.today()
    streak = LearningStreak.query.filter_by(user_id=user_id).first()
    streak_inactive = not streak or not streak.last_learning_date or streak.last_learning_date <= today - timedelta(days=2)

    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    for enrollment in enrollments:
        course = Course.query.get(enrollment.course_id)
        if not course:
            continue

        completed_ids = {
            row.lesson_id
            for row in LessonProgress.query.filter_by(user_id=user_id, course_id=course.id, completed=True).all()
        }
        next_incomplete_query = Video.query.filter(Video.course_id == course.id)
        if completed_ids:
            next_incomplete_query = next_incomplete_query.filter(~Video.id.in_(completed_ids))
        next_incomplete = next_incomplete_query.order_by(Video.order_number.asc(), Video.id.asc()).first()
        if next_incomplete:
            reason = "Needs revision because the lesson is still incomplete."
            if streak_inactive:
                reason = "Needs revision because the lesson is incomplete and your recent learning activity has slowed down."
            suggestions.append({"course": course.title, "lesson": next_incomplete.title, "reason": reason})

        failed_attempt = (
            QuizAttempt.query
            .join(Quiz, QuizAttempt.quiz_id == Quiz.id)
            .filter(QuizAttempt.user_id == user_id, Quiz.course_id == course.id, QuizAttempt.passed == False)
            .order_by(QuizAttempt.submitted_at.desc(), QuizAttempt.id.desc())
            .first()
        )
        if failed_attempt and failed_attempt.quiz:
            lesson_name = failed_attempt.quiz.title
            if failed_attempt.quiz.module_id:
                related_lesson = (
                    Video.query
                    .filter_by(course_id=course.id, module_id=failed_attempt.quiz.module_id)
                    .order_by(Video.order_number.asc(), Video.id.asc())
                    .first()
                )
                if related_lesson:
                    lesson_name = related_lesson.title
            suggestions.append(
                {
                    "course": course.title,
                    "lesson": lesson_name,
                    "reason": "Needs revision because a recent quiz attempt was unsuccessful.",
                }
            )

    unique = []
    seen = set()
    for item in suggestions:
        key = (item["course"], item["lesson"], item["reason"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique[:8]
