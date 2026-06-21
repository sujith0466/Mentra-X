"""
Weekly AI Report - Service  (Feature 7 - Phase B)

Generates a summary of a student's last-7-days activity.
All logic is local and lightweight.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import joinedload
from models import (
    db, User, Enrollment, CodingSubmission, QuizAttempt,
    LessonProgress, SkillProgress, LearningStreak,
)
from services.learning.path_generator import generate_learning_path
from services.ai.career.skill_gap_service import detect_skill_gap


def _past_week() -> datetime:
    return datetime.utcnow() - timedelta(days=7)


def _course_progress_summary(user_id: int) -> list[dict]:
    enrollments = (
        Enrollment.query
        .options(joinedload(Enrollment.course))
        .filter_by(user_id=user_id)
        .all()
    )
    rows = []
    for e in enrollments:
        if not e.course:
            continue
        progress = e.progress_percentage if e.progress_percentage is not None else (e.progress or 0.0)
        rows.append({
            'course': e.course.title,
            'progress_pct': round(progress, 1),
            'completed': bool(e.completed or progress >= 100),
        })
    return rows


def _coding_activity(user_id: int) -> dict:
    cutoff = _past_week()
    submissions = (
        CodingSubmission.query
        .filter(CodingSubmission.user_id == user_id, CodingSubmission.submitted_at >= cutoff)
        .all()
    )
    total = len(submissions)
    passed = sum(1 for s in submissions if (s.score or 0) > 0)
    avg_score = round(sum(s.score or 0 for s in submissions) / total, 1) if total else 0.0
    return {
        'challenges_attempted': total,
        'challenges_passed': passed,
        'average_score': avg_score,
    }


def _quiz_activity(user_id: int) -> dict:
    cutoff = _past_week()
    attempts = (
        QuizAttempt.query
        .filter(QuizAttempt.user_id == user_id, QuizAttempt.start_time >= cutoff)
        .all()
    )
    total = len(attempts)
    passed = sum(1 for a in attempts if a.passed)
    avg_score = round(sum(a.score_percentage for a in attempts) / total, 1) if total else 0.0
    return {
        'quizzes_attempted': total,
        'quizzes_passed': passed,
        'average_score_pct': avg_score,
    }


def _lessons_completed_week(user_id: int) -> int:
    cutoff = _past_week()
    return (
        LessonProgress.query
        .filter(
            LessonProgress.user_id == user_id,
            LessonProgress.completed == True,
            LessonProgress.completed_at >= cutoff,
        )
        .count()
    )


def _split_skill_topics(rows: List[SkillProgress]) -> tuple[list[str], list[str]]:
    valid_rows = [row for row in rows if row.progress_percentage is not None]
    weakest = sorted(valid_rows, key=lambda row: float(row.progress_percentage or 0.0))
    strongest = sorted(valid_rows, key=lambda row: float(row.progress_percentage or 0.0), reverse=True)
    weak_topics = [
        f"{row.skill_name} ({round(row.progress_percentage, 1)}%)"
        for row in weakest[:5]
        if row.progress_percentage < 50
    ]
    strong_topics = [
        f"{row.skill_name} ({round(row.progress_percentage, 1)}%)"
        for row in strongest[:5]
        if row.progress_percentage >= 70
    ]
    return weak_topics, strong_topics


def _generate_recommendations(
    course_progress: list[dict],
    coding: dict,
    weak_topics: list[str],
    strong_topics: list[str],
    lessons_count: int,
) -> list[str]:
    recs: list[str] = []

    in_progress = [c for c in course_progress if not c['completed'] and c['progress_pct'] > 0]
    not_started = [c for c in course_progress if c['progress_pct'] == 0]

    if in_progress:
        closest = max(in_progress, key=lambda c: c['progress_pct'])
        recs.append(
            f"You're {round(100 - closest['progress_pct'])}% away from finishing '{closest['course']}'. Complete it this week."
        )
    if not_started:
        recs.append(f"You have not started '{not_started[0]['course']}'. Begin with a 30-minute session.")

    if coding['challenges_attempted'] == 0:
        recs.append('No coding challenges this week. Solve at least 2 practice tasks.')
    elif coding['average_score'] < 50:
        recs.append('Coding score is below 50%. Revisit hints and retry previous problems.')

    if weak_topics:
        recs.append(f"Focus revision on: {', '.join(weak_topics[:3])}.")
    if strong_topics:
        recs.append(f"Build advanced work around your strengths: {', '.join(strong_topics[:2])}.")

    if lessons_count == 0:
        recs.append('No lessons completed this week. Set a minimum target of 3 lessons.')
    elif lessons_count < 3:
        recs.append(f'You completed {lessons_count} lesson(s). Aim for 5 next week.')

    if not recs:
        recs.append('Great consistency this week. Move to one higher-difficulty topic next.')

    return recs[:6]


def _build_summary_text(
    user_name: str,
    courses: list[dict],
    coding: dict,
    quiz: dict,
    lessons_count: int,
    streak_days: int,
    weak_topics: list[str],
    strong_topics: list[str],
) -> str:
    parts = [f"Here's your weekly learning summary, {user_name}!"]

    enrolled = len(courses)
    completed = sum(1 for c in courses if c['completed'])
    parts.append(f'You are enrolled in {enrolled} course(s) with {completed} completed.')

    parts.append(f'Lessons completed this week: {lessons_count}.')
    parts.append(
        f"Coding: {coding['challenges_attempted']} attempted, {coding['challenges_passed']} passed (avg {coding['average_score']}%)."
    )
    parts.append(
        f"Quizzes: {quiz['quizzes_attempted']} attempted, {quiz['quizzes_passed']} passed (avg {quiz['average_score_pct']}%)."
    )

    if streak_days:
        parts.append(f'Current learning streak: {streak_days} day(s).')
    if strong_topics:
        parts.append(f"Strong topics: {', '.join(strong_topics[:2])}.")
    if weak_topics:
        parts.append(f"Needs attention: {', '.join(weak_topics[:2])}.")

    return ' '.join(parts)


def generate_weekly_report(user_id: int) -> dict:
    """Build a weekly AI report with strong/weak topic insights."""
    user = db.session.get(User, user_id)
    user_name = user.name if user else 'Student'

    courses = _course_progress_summary(user_id)
    coding = _coding_activity(user_id)
    quiz = _quiz_activity(user_id)
    lessons_count = _lessons_completed_week(user_id)
    skill_rows = SkillProgress.query.filter_by(user_id=user_id).all()
    weak_topics, strong_topics = _split_skill_topics(skill_rows)

    streak_record = LearningStreak.query.filter_by(user_id=user_id).first()
    streak_days = streak_record.current_streak if streak_record else 0

    summary = _build_summary_text(
        user_name, courses, coding, quiz, lessons_count, streak_days, weak_topics, strong_topics
    )
    recommendations = _generate_recommendations(courses, coding, weak_topics, strong_topics, lessons_count)
    learning_path = generate_learning_path(user_id)
    gap_payload = detect_skill_gap(user_id, "Full Stack Developer")
    missing_skills = gap_payload.get("skills_missing", [])[:6]
    recommended_courses = gap_payload.get("recommended_courses", [])[:5]

    priority = "high" if weak_topics or coding.get("average_score", 0) < 50 else "medium"
    next_action = (
        learning_path.get("next_action")
        or (f"Start '{learning_path.get('next_courses', [{}])[0].get('title')}'." if learning_path.get("next_courses") else "Complete one lesson today.")
    )

    return {
        'summary': summary,
        'course_progress': courses,
        'coding_activity': coding,
        'quiz_activity': quiz,
        'lessons_completed': lessons_count,
        'weak_topics': weak_topics,
        'strong_topics': strong_topics,
        'recommendations': recommendations,
        'next_steps': learning_path.get('next_courses', []),
        'missing_skills': missing_skills,
        'recommended_courses': recommended_courses,
        'next_action': next_action,
        'priority': priority,
        'streak_days': streak_days,
        'generated_at': datetime.utcnow().isoformat() + 'Z',
    }
