from __future__ import annotations

import json
from typing import Dict

from models import ProjectIdea, db
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


def generate_project(domain: str, difficulty: str) -> ProjectIdea:
    selected_domain = domain if domain in PROJECT_CATALOG else "AI"
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

