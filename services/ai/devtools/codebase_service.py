from __future__ import annotations

from collections import Counter
from typing import Dict, Iterable, List


FLASK_HINTS = {"app.py", "models.py", "templates", "static", "routes", "auth_routes.py", "student_routes.py", "admin_routes.py"}
NODE_HINTS = {"package.json", "src", "public", "server.js"}
DATA_HINTS = {"notebook.ipynb", "requirements.txt", "data", "analysis.py"}


def analyze_project_structure(files: Iterable[str]) -> Dict[str, object]:
    normalized_files = [str(item).strip() for item in files if str(item).strip()]
    lowered = [item.lower() for item in normalized_files]
    names_only = {part.split('/')[-1].split('\\')[-1] for part in lowered}

    project_type = "General Application"
    architecture = "This project has a general software structure."
    description = "The uploaded file list suggests a basic application layout without a strongly identifiable framework."

    if names_only & {name.lower() for name in FLASK_HINTS}:
        project_type = "Flask Web Application"
        architecture = "This project follows a Flask-style monolithic web application architecture."
        description = "The file list shows a typical Flask setup with app configuration, models, templates, static assets, and route modules."
    elif names_only & {name.lower() for name in NODE_HINTS}:
        project_type = "JavaScript / Node Application"
        architecture = "This project appears to use a JavaScript full-stack or Node-based architecture."
        description = "The file list includes common frontend and backend JavaScript project markers."
    elif names_only & {name.lower() for name in DATA_HINTS}:
        project_type = "Data or Analysis Project"
        architecture = "This project looks like a data or analysis-oriented codebase."
        description = "The file list suggests notebooks, scripts, and dependency files used for data workflows."

    important_files = []
    for candidate in ["app.py", "models.py", "requirements.txt", "package.json", "README.md", "templates", "static"]:
        for item in normalized_files:
            if item.lower().endswith(candidate.lower()) or item.lower() == candidate.lower():
                important_files.append(item)
                break

    backend_components = [
        item for item in normalized_files
        if any(token in item.lower() for token in ["app.py", "models.py", "route", "service", "api", "requirements.txt"])
    ][:8]
    frontend_components = [
        item for item in normalized_files
        if any(token in item.lower() for token in ["template", "static", ".html", ".css", ".js", "public", "src"])
    ][:8]

    extension_counter = Counter()
    for item in normalized_files:
        if "." in item:
            extension_counter[item.rsplit(".", 1)[-1].lower()] += 1

    suggestions: List[str] = [
        "Add a README that explains setup, architecture, and feature flow if one is missing.",
        "Separate core business logic from route handlers to keep the codebase easier to maintain.",
    ]
    if extension_counter.get("py", 0) and not any("tests" in path.lower() for path in normalized_files):
        suggestions.append("Add a tests folder so major routes and services can be verified safely.")
    if any("templates" in path.lower() for path in normalized_files) and not any("static" in path.lower() for path in normalized_files):
        suggestions.append("Check whether static assets are organized clearly for CSS, JavaScript, and media files.")

    return {
        "project_type": project_type,
        "architecture": architecture,
        "architecture_summary": description,
        "description": description,
        "backend_components": backend_components,
        "frontend_components": frontend_components,
        "important_files": important_files,
        "suggestions": suggestions,
    }
