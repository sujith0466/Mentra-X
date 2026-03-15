from __future__ import annotations

from typing import Dict, List

from models import AssignmentSubmission, Course, Enrollment, LearningStreak, LessonProgress, Quiz, QuizAttempt, Video

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None


def detect_learning_difficulty(user_id: int) -> Dict[str, List[str]]:
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    lesson_rows = LessonProgress.query.filter_by(user_id=user_id).all()
    quiz_attempts = QuizAttempt.query.filter_by(user_id=user_id).all()
    assignment_rows = AssignmentSubmission.query.filter_by(user_id=user_id).all()
    streak = LearningStreak.query.filter_by(user_id=user_id).first()

    weak_topics: List[str] = []
    recommended_revision: List[str] = []
    practice_quizzes: List[str] = []

    incomplete_courses = [
        row.course for row in enrollments
        if row.course and not (row.completed or (row.progress_percentage or row.progress or 0) >= 100)
    ]

    if pd is not None:
        lesson_frame = pd.DataFrame(
            [{"course_id": row.course_id, "completed": bool(row.completed)} for row in lesson_rows]
        )
        grouped = lesson_frame.groupby("course_id")["completed"].mean().to_dict() if not lesson_frame.empty else {}
    else:
        grouped = {}
        totals = {}
        completed_counts = {}
        for row in lesson_rows:
            totals[row.course_id] = totals.get(row.course_id, 0) + 1
            completed_counts[row.course_id] = completed_counts.get(row.course_id, 0) + (1 if row.completed else 0)
        for course_id, total in totals.items():
            grouped[course_id] = (completed_counts.get(course_id, 0) / total) if total else 0

    for course_id, completion_ratio in grouped.items():
        if float(completion_ratio) < 0.5:
            course = Course.query.get(course_id)
            if course:
                weak_topics.append(f"{course.title} lesson flow")
                recommended_revision.append(f"Revisit the early modules in {course.title} and complete one lesson at a time.")

    if pd is not None:
        score_frame = pd.DataFrame(
            [{"quiz_id": row.quiz_id, "score": float(row.score_percentage or 0)} for row in quiz_attempts]
        )
        low_scores = score_frame.groupby("quiz_id")["score"].mean().to_dict() if not score_frame.empty else {}
    else:
        totals = {}
        counts = {}
        for row in quiz_attempts:
            totals[row.quiz_id] = totals.get(row.quiz_id, 0.0) + float(row.score_percentage or 0)
            counts[row.quiz_id] = counts.get(row.quiz_id, 0) + 1
        low_scores = {quiz_id: (totals[quiz_id] / counts[quiz_id]) for quiz_id in totals}

    for quiz_id, avg_score in low_scores.items():
        if avg_score < 70:
            quiz = Quiz.query.get(quiz_id)
            if quiz and quiz.title:
                weak_topics.append(quiz.title)
                recommended_revision.append(f"Review the lesson notes for {quiz.title} and retake a practice quiz.")
                practice_quizzes.append(quiz.title)

    for submission in assignment_rows:
        if submission.marks_awarded is None or not submission.assignment:
            continue
        assignment_marks = float(submission.marks_awarded or 0.0)
        max_marks = float(submission.assignment.marks or 100.0)
        if max_marks <= 0:
            continue
        assignment_percentage = (assignment_marks / max_marks) * 100.0
        if assignment_percentage < 60:
            weak_topics.append(submission.assignment.title)
            recommended_revision.append(f"Rework the assignment {submission.assignment.title} and review the related module before trying again.")

    streak_value = streak.current_streak if streak else 0
    if streak_value < 2 and incomplete_courses:
        for course in incomplete_courses[:2]:
            weak_topics.append(f"Consistency in {course.title}")
            recommended_revision.append(f"Use a lighter daily target in {course.title} until your study streak stabilizes.")

    if not weak_topics and incomplete_courses:
        for course in incomplete_courses[:3]:
            weak_topics.append(course.title)
            recommended_revision.append(f"Stay steady with {course.title} and review one lesson before attempting graded work.")

    unique_weak_topics = list(dict.fromkeys(weak_topics))[:5]
    unique_revision = list(dict.fromkeys(recommended_revision))[:5]
    unique_quizzes = list(dict.fromkeys(practice_quizzes))[:5]

    if not unique_quizzes:
        fallback_videos = Video.query.join(Enrollment, Enrollment.course_id == Video.course_id).filter(Enrollment.user_id == user_id).order_by(Video.order_number.asc()).limit(3).all()
        unique_quizzes = [video.title for video in fallback_videos]

    return {
        "weak_topics": unique_weak_topics,
        "recommended_revision": unique_revision,
        "practice_quizzes": unique_quizzes,
    }
