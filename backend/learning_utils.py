from datetime import datetime, timezone
from backend.models import db, LessonProgress, Enrollment, Video
from backend.services.learning.streak_xp import update_streak


def update_learning_streak(user_id, activity_date=None):
    # Keep compatibility for existing callers while using the unified streak service.
    return update_streak(user_id)


def recalculate_course_progress(user_id, course_id):
    total_lessons = Video.query.filter_by(course_id=course_id).count()
    if total_lessons <= 0:
        progress_pct = 0.0
    else:
        completed_lessons = (
            LessonProgress.query
            .filter_by(user_id=user_id, course_id=course_id, completed=True)
            .count()
        )
        progress_pct = round((completed_lessons / total_lessons) * 100, 2)

    enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
    if enrollment:
        enrollment.progress = progress_pct
        enrollment.progress_percentage = progress_pct
        enrollment.completed = progress_pct >= 100
    return progress_pct


def mark_lesson_complete(user_id, course_id, lesson_id):
    progress = LessonProgress.query.filter_by(user_id=user_id, lesson_id=lesson_id).first()
    if not progress:
        progress = LessonProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            course_id=course_id,
            completed=True,
            completed_at=datetime.utcnow(),
        )
        db.session.add(progress)
    else:
        progress.course_id = course_id
        progress.completed = True
        progress.completed_at = datetime.utcnow()

    update_learning_streak(user_id)
    return recalculate_course_progress(user_id, course_id)


def refresh_progress_on_quiz_completion(user_id, course_id):
    """Keep progress cache synchronized after quiz completion events."""
    return recalculate_course_progress(user_id, course_id)


def refresh_progress_on_assignment_submission(user_id, course_id):
    """Keep progress cache synchronized after assignment submission events."""
    return recalculate_course_progress(user_id, course_id)
