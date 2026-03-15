from datetime import datetime, date, timedelta
from models import db, LearningStreak, LessonProgress, Enrollment, Video


def update_learning_streak(user_id, activity_date=None):
    activity_date = activity_date or date.today()
    streak = LearningStreak.query.filter_by(user_id=user_id).first()
    if not streak:
        streak = LearningStreak(
            user_id=user_id,
            last_learning_date=activity_date,
            current_streak=1,
            longest_streak=1,
            updated_at=datetime.utcnow(),
        )
        db.session.add(streak)
        return streak

    last_date = streak.last_learning_date
    if last_date == activity_date:
        streak.updated_at = datetime.utcnow()
        return streak

    if last_date == activity_date - timedelta(days=1):
        streak.current_streak += 1
    else:
        streak.current_streak = 1

    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak
    streak.last_learning_date = activity_date
    streak.updated_at = datetime.utcnow()
    return streak


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
