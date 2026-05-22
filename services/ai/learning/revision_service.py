from __future__ import annotations

from datetime import date, timedelta
from typing import Dict, List

from models import (
    AssignmentSubmission,
    CodingChallenge,
    CodingSubmission,
    Course,
    Enrollment,
    LearningStreak,
    LessonProgress,
    Quiz,
    QuizAttempt,
    Video,
)
from services.ai.ml.learning_difficulty_model import detect_learning_difficulty


def get_revision_topics(user_id: int) -> List[Dict[str, object]]:
    suggestions: List[Dict[str, object]] = []
    today = date.today()
    streak = LearningStreak.query.filter_by(user_id=user_id).first()
    streak_inactive = not streak or not streak.last_learning_date or streak.last_learning_date <= today - timedelta(days=2)

    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    enrolled_courses = [row.course for row in enrollments if row.course]
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
            reason = "Rewatch this lesson and attempt a practice quiz to reinforce the concept."
            if streak_inactive:
                reason = "Rewatch this lesson and attempt a practice quiz to rebuild momentum."
            suggestions.append({"course": course.title, "lesson": next_incomplete.title, "reason": reason})

        failed_attempts = (
            QuizAttempt.query
            .join(Quiz, QuizAttempt.quiz_id == Quiz.id)
            .filter(QuizAttempt.user_id == user_id, Quiz.course_id == course.id, QuizAttempt.passed == False)
            .order_by(QuizAttempt.submitted_at.desc(), QuizAttempt.id.desc())
            .all()
        )
        if failed_attempts:
            attempt = failed_attempts[0]
            lesson_name = attempt.quiz.title if attempt.quiz else course.title
            if attempt.quiz and attempt.quiz.module_id:
                related_lesson = (
                    Video.query
                    .filter_by(course_id=course.id, module_id=attempt.quiz.module_id)
                    .order_by(Video.order_number.asc(), Video.id.asc())
                    .first()
                )
                if related_lesson:
                    lesson_name = related_lesson.title
            reason = "Recent quiz performance was below target. Rewatch the lesson and attempt a practice quiz."
            if len(failed_attempts) >= 2:
                reason = "Repeated quiz misses detected. Rewatch the lesson, then retry the quiz."
            suggestions.append(
                {
                    "course": course.title,
                    "lesson": lesson_name,
                    "reason": reason,
                }
            )

    quiz_attempts = QuizAttempt.query.filter_by(user_id=user_id).all()
    quiz_scores: Dict[int, List[float]] = {}
    for attempt in quiz_attempts:
        quiz_scores.setdefault(attempt.quiz_id, []).append(float(attempt.score_percentage or 0))
    for quiz_id, scores in quiz_scores.items():
        avg_score = sum(scores) / max(len(scores), 1)
        if avg_score < 60:
            quiz = Quiz.query.get(quiz_id)
            if quiz:
                suggestions.append(
                    {
                        "course": Course.query.get(quiz.course_id).title if quiz.course_id else "Quiz Focus",
                        "lesson": quiz.title,
                        "reason": f"Average quiz score {int(avg_score)}%. Rewatch lessons and attempt a practice quiz.",
                    }
                )

    assignment_rows = AssignmentSubmission.query.filter_by(user_id=user_id).all()
    for submission in assignment_rows:
        if submission.marks_awarded is None or not submission.assignment:
            continue
        max_marks = float(submission.assignment.marks or 100.0)
        if max_marks <= 0:
            continue
        percentage = (float(submission.marks_awarded or 0.0) / max_marks) * 100.0
        if percentage < 60:
            suggestions.append(
                {
                    "course": Course.query.get(submission.assignment.course_id).title if submission.assignment.course_id else "Assignment Focus",
                    "lesson": submission.assignment.title,
                    "reason": f"Assignment score {int(percentage)}%. Revisit the lesson and resubmit the assignment.",
                }
            )

    coding_submissions = CodingSubmission.query.filter_by(user_id=user_id).all()
    challenge_scores: Dict[int, List[float]] = {}
    for submission in coding_submissions:
        challenge_scores.setdefault(submission.challenge_id, []).append(float(submission.score or 0))
    for challenge_id, scores in challenge_scores.items():
        avg_score = sum(scores) / max(len(scores), 1)
        if avg_score < 60:
            challenge = CodingChallenge.query.get(challenge_id)
            if challenge:
                suggestions.append(
                    {
                        "course": "Coding Practice",
                        "lesson": challenge.title,
                        "reason": f"Average coding score {int(avg_score)}%. Re-attempt this challenge for stronger fundamentals.",
                    }
                )

    try:
        difficulty_payload = detect_learning_difficulty(user_id)
    except Exception:
        difficulty_payload = {}
    for topic in difficulty_payload.get("weak_topics", [])[:3]:
        suggestions.append(
            {
                "course": "Focus Area",
                "lesson": topic,
                "reason": "Weak topic detected. Rewatch lessons and attempt a practice quiz.",
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
    if unique:
        return unique[:10]

    recent_progress = (
        LessonProgress.query
        .filter_by(user_id=user_id)
        .order_by(LessonProgress.created_at.desc())
        .limit(3)
        .all()
    )
    fallback = []
    for row in recent_progress:
        video = Video.query.get(row.lesson_id)
        if video:
            fallback.append(
                {
                    "course": Course.query.get(video.course_id).title if video.course_id else "Recent Lesson",
                    "lesson": video.title,
                    "reason": "Recent lesson detected. Rewatch to strengthen recall.",
                }
            )
    if fallback:
        return fallback

    for course in enrolled_courses[:3]:
        if not course:
            continue
        fallback.append(
            {
                "course": course.title,
                "lesson": "Recent lesson review",
                "reason": "Revisit the last lesson you opened and attempt a quick practice quiz.",
            }
        )
    return fallback
