from __future__ import annotations

from typing import Dict, List

import json

from models import Course, Enrollment, Quiz, QuizAttempt, UserResume
from services.ai.career.resume_service import CAREER_SKILL_MAP
from services.ai.career_service import CAREER_ROADMAPS


def _infer_user_skills(user_id: int) -> List[str]:
    skills = set()

    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    completed_courses = [row.course for row in enrollments if row.course and (row.completed or (row.progress_percentage or row.progress or 0) >= 100)]
    for course in completed_courses:
        title = (course.title or "").lower()
        if "python" in title:
            skills.add("Python")
        if "react" in title or "next.js" in title or "nextjs" in title:
            skills.update(["JavaScript", "React"])
        if "flask" in title or "mern" in title:
            skills.update(["Flask", "JavaScript"])
        if "machine learning" in title:
            skills.add("Machine Learning")
        if "deep learning" in title:
            skills.update(["Deep Learning", "Neural Networks"])
        if "nlp" in title:
            skills.add("Data Processing")
        if "data" in title or "analytics" in title or "power bi" in title:
            skills.update(["Pandas", "Visualization", "Statistics"])
        if "aws" in title or "docker" in title or "kubernetes" in title:
            skills.add("APIs")
        if "security" in title or "hacking" in title:
            skills.add("Authentication")

    passed_attempts = (
        QuizAttempt.query
        .join(Quiz, QuizAttempt.quiz_id == Quiz.id)
        .filter(QuizAttempt.user_id == user_id, QuizAttempt.passed == True)
        .all()
    )
    if passed_attempts:
        skills.add("Problem Solving")

    resume_row = UserResume.query.filter_by(user_id=user_id).first()
    if resume_row:
        resume_skills = json.loads(resume_row.skills_json or "[]")
        skills.update(resume_skills)

    return sorted(skills)


def detect_skill_gap(user_id: int, career_goal: str) -> Dict[str, object]:
    normalized_goal = (career_goal or "").strip() or "Full Stack Developer"
    required_skills = CAREER_SKILL_MAP.get(normalized_goal, CAREER_SKILL_MAP["Full Stack Developer"])
    user_skills = _infer_user_skills(user_id)
    skills_missing = [skill for skill in required_skills if skill not in user_skills]

    recommended_courses = []
    all_courses = Course.query.filter(Course.status == 'published').all()
    lowered_missing = [skill.lower() for skill in skills_missing]
    for course in all_courses:
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
        "recommended_courses": recommended_courses[:5],
        "recommended_projects": recommended_projects[:4],
    }
