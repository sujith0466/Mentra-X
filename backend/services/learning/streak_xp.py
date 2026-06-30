"""
Learning Streak + XP System (Feature 12 — Phase C)

Tracks daily learning streaks and calculates dynamic XP points
based on student actions (progress, challenges, quizzes).
"""

from datetime import datetime, timezone, date, timedelta
from backend.models import (
    db, LearningStreak, UserXP, LessonProgress, 
    Enrollment, CodingSubmission, QuizAttempt
)

def _serialize_streak(streak: LearningStreak) -> dict:
    return {
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
        "last_learning_date": streak.last_learning_date.isoformat() if streak.last_learning_date else None
    }


def get_streak(user_id: int) -> dict:
    """Return current streak data without mutating streak counters."""
    streak = LearningStreak.query.filter_by(user_id=user_id).first()
    if not streak:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "last_learning_date": None,
        }
    return _serialize_streak(streak)


def update_streak(user_id: int) -> dict:
    """
    Updates the learning streak assuming the user performed a meaningful action.
    Returns streak data.
    """
    activity_date = date.today()
    streak = LearningStreak.query.filter_by(user_id=user_id).first()
    
    if not streak:
        streak = LearningStreak(
            user_id=user_id,
            last_learning_date=activity_date,
            current_streak=1,
            longest_streak=1,
            updated_at=datetime.utcnow()
        )
        db.session.add(streak)
    else:
        last_date = streak.last_learning_date
        
        if last_date == activity_date:
            streak.updated_at = datetime.utcnow()
        elif last_date == activity_date - timedelta(days=1):
            streak.current_streak += 1
            if streak.current_streak > streak.longest_streak:
                streak.longest_streak = streak.current_streak
            streak.last_learning_date = activity_date
            streak.updated_at = datetime.utcnow()
        elif last_date and last_date < activity_date - timedelta(days=1):
            # Broken streak
            streak.current_streak = 1
            streak.last_learning_date = activity_date
            streak.updated_at = datetime.utcnow()

    db.session.commit()
    
    return _serialize_streak(streak)


def calculate_xp(user_id: int) -> dict:
    """
    Aggregates existing data to calculate historical XP. 
    Returns current XP and computed level.
    """
    # Base XP calculation logic:
    # +10 XP per lesson completed
    # +20 XP per course fully completed
    # +5 XP per passed coding challenge tests
    # +10 XP per passed quiz
    
    total_xp = 0
    
    # +10 XP per lesson completed
    lessons_completed = LessonProgress.query.filter_by(user_id=user_id, completed=True).count()
    total_xp += (lessons_completed * 10)
    
    # +20 XP per course fully completed
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    courses_completed = sum(1 for e in enrollments if e.completed or (e.progress_percentage or 0) >= 100)
    total_xp += (courses_completed * 20)
    
    # +5 XP per passed test in coding challenges
    submissions = CodingSubmission.query.filter_by(user_id=user_id).all()
    total_coding_xp = sum((s.passed_tests or 0) * 5 for s in submissions)
    total_xp += total_coding_xp
    
    # +10 XP per passed quiz
    quizzes_passed = QuizAttempt.query.filter_by(user_id=user_id, passed=True).count()
    total_xp += (quizzes_passed * 10)
    
    # Calculate level (1 level every 100 XP, starting at level 1)
    new_level = max(1, (total_xp // 100) + 1)
    
    # Update UserXP record if it exists, otherwise create it
    xp_record = UserXP.query.filter_by(user_id=user_id).first()
    if not xp_record:
        xp_record = UserXP(user_id=user_id, xp_points=total_xp, level=new_level)
        db.session.add(xp_record)
    else:
        xp_record.xp_points = total_xp
        xp_record.level = new_level
        
    db.session.commit()
    
    return {
        "xp_points": total_xp,
        "level": new_level,
        "breakdown": {
            "lessons": lessons_completed * 10,
            "courses": courses_completed * 20,
            "coding": total_coding_xp,
            "quizzes": quizzes_passed * 10
        }
    }
