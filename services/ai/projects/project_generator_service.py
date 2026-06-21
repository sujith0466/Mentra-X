from __future__ import annotations

import json
from typing import Dict, Optional

import json

from models import Enrollment, ProjectIdea, UserResume, db
from services.ai.projects.project_blueprint_service import generate_project_blueprint


PROJECT_CATALOG = {
    "AI": {
        "title": "AI Resume Analyzer",
        "description": "Build an AI system that analyzes resumes and provides skill recommendations.",
        "tech_stack": ["Python", "Flask", "NLP", "SQLite"],
    },
    "Web Development": {
        "title": "Mentra Course Marketplace",
        "description": "Create a web platform for browsing courses, tracking progress, and recommending learning paths.",
        "tech_stack": ["Python", "Flask", "Jinja", "SQLite"],
    },
    "Machine Learning": {
        "title": "Model Performance Dashboard",
        "description": "Build a dashboard that compares model metrics and surfaces training insights for students.",
        "tech_stack": ["Python", "Pandas", "Scikit-learn", "SQLite"],
    },
    "Data Science": {
        "title": "Student Success Analyzer",
        "description": "Analyze student activity data and generate recommendations for better learning outcomes.",
        "tech_stack": ["Python", "Pandas", "Matplotlib", "SQLite"],
    },
    "Mobile Apps": {
        "title": "Micro Learning Companion",
        "description": "Build a mobile learning companion with streak tracking, quizzes, and push-style reminders.",
        "tech_stack": ["Flutter", "Dart", "REST API", "SQLite"],
    },
}


def _infer_domain_from_user(user_id: int) -> str:
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    for enrollment in enrollments:
        if enrollment.course and enrollment.course.domain:
            return enrollment.course.domain.name
    resume_row = UserResume.query.filter_by(user_id=user_id).first()
    if resume_row:
        try:
            skills = json.loads(resume_row.skills_json or "[]")
        except (TypeError, ValueError, json.JSONDecodeError):
            skills = []
        if any(skill in skills for skill in ["React", "JavaScript", "HTML", "CSS"]):
            return "Web Development"
        if any(skill in skills for skill in ["Machine Learning", "Deep Learning", "Neural Networks"]):
            return "AI"
        if any(skill in skills for skill in ["Pandas", "Statistics", "Visualization"]):
            return "Data Science"
    return "AI"


def generate_project(domain: str, difficulty: str, user_id: Optional[int] = None) -> ProjectIdea:
    selected_domain = domain if domain in PROJECT_CATALOG else ""
    if not selected_domain and user_id:
        selected_domain = _infer_domain_from_user(user_id)
    if not selected_domain:
        selected_domain = "AI"
    base = PROJECT_CATALOG[selected_domain]
    blueprint = generate_project_blueprint(base["title"], selected_domain, difficulty)

    project = ProjectIdea(
        title=base["title"],
        description=base["description"],
        domain=selected_domain,
        difficulty=difficulty,
        tech_stack=json.dumps(base["tech_stack"]),
        architecture=json.dumps(blueprint),
    )
    db.session.add(project)
    db.session.commit()
    return project
