from __future__ import annotations

from typing import Dict, List

import json

from models import Course, Enrollment, Quiz, QuizAttempt, UserResume
from services.ai.career.resume_service import CAREER_SKILL_MAP, SKILL_KEYWORDS
from services.ai.career_service import CAREER_ROADMAPS


def _skills_from_text(text: str) -> List[str]:
    normalized = (text or "").lower()
    detected = []
    for skill, keywords in SKILL_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            detected.append(skill)
    return detected


def _infer_user_skills(user_id: int) -> Dict[str, List[str]]:
    resume_skills = []
    course_skills_completed: List[str] = []
    course_skills_enrolled: List[str] = []
    activity_skills: List[str] = []

    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    completed_courses = [
        row.course for row in enrollments
        if row.course and (row.completed or (row.progress_percentage or row.progress or 0) >= 100)
    ]
    enrolled_courses = [
        row.course for row in enrollments
        if row.course and not (row.completed or (row.progress_percentage or row.progress or 0) >= 100)
    ]
    for course in completed_courses:
        course_text = f"{course.title or ''} {course.description or ''}"
        course_skills_completed.extend(_skills_from_text(course_text))
    for course in enrolled_courses:
        course_text = f"{course.title or ''} {course.description or ''}"
        course_skills_enrolled.extend(_skills_from_text(course_text))

    passed_attempts = (
        QuizAttempt.query
        .join(Quiz, QuizAttempt.quiz_id == Quiz.id)
        .filter(QuizAttempt.user_id == user_id, QuizAttempt.passed == True)
        .all()
    )
    if passed_attempts:
        activity_skills.append("Problem Solving")

    resume_row = UserResume.query.filter_by(user_id=user_id).first()
    if resume_row:
        resume_skills = json.loads(resume_row.skills_json or "[]")

    return {
        "resume_skills": sorted(set(resume_skills)),
        "course_skills_completed": sorted(set(course_skills_completed)),
        "course_skills_enrolled": sorted(set(course_skills_enrolled)),
        "activity_skills": sorted(set(activity_skills)),
    }


def detect_skill_gap(user_id: int, career_goal: str) -> Dict[str, object]:
    normalized_goal = (career_goal or "").strip() or "Full Stack Developer"
    required_skills = CAREER_SKILL_MAP.get(normalized_goal, CAREER_SKILL_MAP["Full Stack Developer"])
    skill_buckets = _infer_user_skills(user_id)
    resume_skills = set(skill_buckets.get("resume_skills", []))
    course_completed = set(skill_buckets.get("course_skills_completed", []))
    course_enrolled = set(skill_buckets.get("course_skills_enrolled", []))
    activity_skills = set(skill_buckets.get("activity_skills", []))
    user_skills = sorted(resume_skills | course_completed | course_enrolled | activity_skills)
    skills_missing = [skill for skill in required_skills if skill not in user_skills]
    suggested_skills = [
        skill for skill in required_skills
        if skill in (course_completed | course_enrolled | activity_skills) and skill not in resume_skills
    ]

    recommended_courses = []
    all_courses = Course.query.filter(Course.status == 'published').all()
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    completed_course_ids = {
        row.course_id for row in enrollments
        if row.completed or (row.progress_percentage or row.progress or 0) >= 100
    }
    enrolled_course_ids = {row.course_id for row in enrollments}
    lowered_missing = [skill.lower() for skill in skills_missing]
    for course in all_courses:
        if course.id in completed_course_ids or course.id in enrolled_course_ids:
            continue
        course_text = f"{course.title} {course.description or ''}".lower()
        if any(skill.lower() in course_text for skill in skills_missing) or any(token in course_text for token in lowered_missing):
            recommended_courses.append(course.title)
    if not recommended_courses:
        recommended_courses = list(CAREER_ROADMAPS.get(normalized_goal, CAREER_ROADMAPS['Full Stack Developer'])["recommended_courses"])

    recommended_projects = list(CAREER_ROADMAPS.get(normalized_goal, CAREER_ROADMAPS['Full Stack Developer'])["projects"])

    return {
        "career_goal": normalized_goal,
        "skills_you_have": user_skills,
        "skills_missing": skills_missing,
        "suggested_skills": suggested_skills,
        "recommended_courses": recommended_courses[:5],
        "recommended_projects": recommended_projects[:4],
    }
