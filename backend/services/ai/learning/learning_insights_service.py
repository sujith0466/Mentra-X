from __future__ import annotations

from typing import Dict, List, Set

import json

from backend.models import (
    AssignmentSubmission,
    CodingChallenge,
    CodingSubmission,
    Course,
    Enrollment,
    LessonProgress,
    Quiz,
    QuizAttempt,
    UserResume,
)
from backend.services.ai.career.resume_service import CAREER_SKILL_MAP, SKILL_KEYWORDS
from backend.services.ai.career.skill_gap_service import detect_skill_gap
from backend.services.ai.recommendation_service import recommend_courses


def _skills_from_text(text: str) -> List[str]:
    normalized = (text or "").lower()
    detected = []
    for skill, keywords in SKILL_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            detected.append(skill)
    return detected


def _infer_primary_career(resume_skills: List[str]) -> str:
    if not resume_skills:
        return "Full Stack Developer"
    career_scores = []
    for career, required_skills in CAREER_SKILL_MAP.items():
        score = sum(1 for skill in required_skills if skill in resume_skills)
        if score > 0:
            career_scores.append((career, score))
    career_scores.sort(key=lambda item: item[1], reverse=True)
    return career_scores[0][0] if career_scores else "Full Stack Developer"


def get_learning_insights(user_id: int) -> Dict[str, List[str]]:
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    completed_courses = [
        row.course for row in enrollments
        if row.course and (row.completed or (row.progress_percentage or row.progress or 0) >= 100)
    ]
    enrolled_courses = [row.course for row in enrollments if row.course]

    resume_row = UserResume.query.filter_by(user_id=user_id).first()
    resume_skills = json.loads(resume_row.skills_json or "[]") if resume_row else []

    weak_topics: List[str] = []

    quiz_attempts = QuizAttempt.query.filter_by(user_id=user_id).all()
    quiz_scores: Dict[int, List[float]] = {}
    quiz_failures: Dict[int, int] = {}
    for attempt in quiz_attempts:
        quiz_scores.setdefault(attempt.quiz_id, []).append(float(attempt.score_percentage or 0))
        if attempt.passed is False:
            quiz_failures[attempt.quiz_id] = quiz_failures.get(attempt.quiz_id, 0) + 1

    for quiz_id, scores in quiz_scores.items():
        avg_score = sum(scores) / max(len(scores), 1)
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            continue
        if avg_score < 60 or quiz_failures.get(quiz_id, 0) >= 2:
            weak_topics.append(quiz.title)

    assignment_rows = AssignmentSubmission.query.filter_by(user_id=user_id).all()
    for submission in assignment_rows:
        if submission.marks_awarded is None or not submission.assignment:
            continue
        max_marks = float(submission.assignment.marks or 100.0)
        if max_marks <= 0:
            continue
        percentage = (float(submission.marks_awarded or 0.0) / max_marks) * 100.0
        if percentage < 60:
            weak_topics.append(submission.assignment.title)

    lesson_rows = LessonProgress.query.filter_by(user_id=user_id).all()
    lesson_totals: Dict[int, int] = {}
    lesson_completed: Dict[int, int] = {}
    for row in lesson_rows:
        lesson_totals[row.course_id] = lesson_totals.get(row.course_id, 0) + 1
        if row.completed:
            lesson_completed[row.course_id] = lesson_completed.get(row.course_id, 0) + 1
    for course_id, total in lesson_totals.items():
        ratio = (lesson_completed.get(course_id, 0) / total) if total else 0
        if ratio < 0.5:
            course = Course.query.get(course_id)
            if course:
                weak_topics.append(f"{course.title} lessons")

    coding_submissions = CodingSubmission.query.filter_by(user_id=user_id).all()
    challenge_scores: Dict[int, List[float]] = {}
    for submission in coding_submissions:
        challenge_scores.setdefault(submission.challenge_id, []).append(float(submission.score or 0))
    for challenge_id, scores in challenge_scores.items():
        avg_score = sum(scores) / max(len(scores), 1)
        if avg_score < 60:
            challenge = CodingChallenge.query.get(challenge_id)
            if challenge:
                weak_topics.append(challenge.title)

    if not weak_topics and enrolled_courses:
        for course in enrolled_courses[:3]:
            weak_topics.append(course.title)

    skill_pool: Set[str] = set(resume_skills)
    for course in enrolled_courses:
        if not course:
            continue
        course_text = f"{course.title or ''} {course.description or ''}"
        skill_pool.update(_skills_from_text(course_text))

    career_goal = _infer_primary_career(resume_skills)
    gap_report = detect_skill_gap(user_id, career_goal)
    missing_skills = gap_report.get("skills_missing", [])
    suggested_skills = list(dict.fromkeys(missing_skills + sorted(skill_pool - set(resume_skills))))[:6]

    recommended_courses_payload = recommend_courses(user_id)
    recommended_courses = [item["title"] for item in recommended_courses_payload[:5]]
    if not recommended_courses:
        recommended_courses = [course.title for course in completed_courses[:3]]

    return {
        "weak_topics": list(dict.fromkeys(weak_topics))[:5],
        "suggested_skills": suggested_skills,
        "recommended_courses": recommended_courses,
    }
