from __future__ import annotations

from typing import Dict, List

from models import Enrollment, LearningStreak, StudentProject, User
from services.ai.project_idea_service import generate_project_ideas


def _extract_skills_from_courses(course_titles: List[str]) -> List[str]:
    skills = set()
    for title in course_titles:
        lowered = title.lower()
        if "python" in lowered:
            skills.add("Python")
        if "react" in lowered or "next" in lowered:
            skills.update(["JavaScript", "React"])
        if "flask" in lowered or "mern" in lowered:
            skills.update(["Flask", "JavaScript"])
        if "data" in lowered or "analytics" in lowered:
            skills.update(["Data Analysis", "Visualization"])
        if "machine learning" in lowered:
            skills.add("Machine Learning")
        if "deep learning" in lowered or "nlp" in lowered:
            skills.update(["Deep Learning", "NLP"])
        if "security" in lowered or "hacking" in lowered:
            skills.add("Cybersecurity")
        if "aws" in lowered or "docker" in lowered or "kubernetes" in lowered:
            skills.add("Cloud Basics")
    return sorted(skills)


def generate_portfolio(user_id: int) -> Dict[str, object]:
    user = User.query.get_or_404(user_id)
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    completed_courses = [row.course.title for row in enrollments if row.course and (row.completed or (row.progress_percentage or row.progress or 0) >= 100)]
    completed_projects = [
        row.project_idea.title
        for row in StudentProject.query.filter_by(user_id=user_id).all()
        if row.project_idea and row.completed_at
    ]

    dominant_domain = None
    for row in enrollments:
        if row.course and row.course.domain:
            dominant_domain = row.course.domain.name
            break
    dominant_domain = dominant_domain or "AI"

    project_payloads = generate_project_ideas(dominant_domain)
    project_titles = completed_projects or [project["title"] for project in project_payloads[:3]]
    streak = LearningStreak.query.filter_by(user_id=user_id).first()
    achievements = []
    if completed_courses:
        achievements.append(f"Completed {len(completed_courses)} course(s) on Mentra")
    if streak and streak.longest_streak:
        achievements.append(f"Longest learning streak: {streak.longest_streak} days")
    if completed_projects:
        achievements.append(f"Completed {len(completed_projects)} portfolio project(s)")
    if not achievements:
        achievements.append("Started building a learning portfolio on Mentra")

    return {
        "name": user.name,
        "skills": _extract_skills_from_courses(completed_courses),
        "projects": project_titles,
        "courses_completed": completed_courses,
        "achievements": achievements,
    }
