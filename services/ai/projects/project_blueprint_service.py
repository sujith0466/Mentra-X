from __future__ import annotations

from typing import Dict, List


def generate_project_blueprint(title: str, domain: str, difficulty: str) -> Dict[str, List[str] | str]:
    folder_structure = [
        "backend/",
        "backend/models/",
        "backend/routes/",
        "backend/services/",
        "frontend/",
        "README.md",
    ]
    api_endpoints = [
        "GET /api/projects",
        "POST /api/projects",
        "GET /api/projects/<id>",
        "POST /api/projects/<id>/tasks",
    ]
    database_schema = [
        "users",
        "project_ideas",
        "student_projects",
        "project_tasks",
    ]
    development_roadmap = [
        f"Define {title} scope and user stories",
        "Set up project environment",
        "Create database models and task plan",
        "Implement backend endpoints",
        "Build the frontend experience",
        "Test the project end to end",
    ]
    return {
        "summary": f"{difficulty} {domain} project blueprint for {title}",
        "folder_structure": folder_structure,
        "api_endpoints": api_endpoints,
        "database_schema": database_schema,
        "development_roadmap": development_roadmap,
    }

