from __future__ import annotations

from collections import Counter
import re
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


def explain_code_snippet(code: str) -> Dict[str, object]:
    snippet = (code or "").strip()
    if not snippet:
        return {
            "purpose": "No code snippet provided.",
            "logic_flow": "Paste a snippet to receive a line-by-line explanation.",
            "functions_used": [],
            "architecture_summary": "N/A",
            "suggestions": ["Add a function or class so the explainer can infer structure."],
        }

    function_matches = re.findall(r"def\\s+([a-zA-Z_][\\w]*)\\s*\\(|function\\s+([a-zA-Z_][\\w]*)\\s*\\(", snippet)
    functions_used = [match[0] or match[1] for match in function_matches if match[0] or match[1]]

    purpose = "This snippet defines logic to process data and return results."
    if "class " in snippet:
        purpose = "This snippet defines a class-based component or model."
    if "def " in snippet and "return" in snippet:
        purpose = "This function processes inputs and returns a computed value."

    logic_flow_parts = []
    if re.search(r"for\\s+|while\\s+", snippet):
        logic_flow_parts.append("Iterates over data using loops.")
    if re.search(r"if\\s+|elif\\s+|else:", snippet):
        logic_flow_parts.append("Uses conditional branches for decision making.")
    if "try:" in snippet:
        logic_flow_parts.append("Wraps risky operations in error handling.")
    if "return" in snippet:
        logic_flow_parts.append("Returns a final value or response.")
    if not logic_flow_parts:
        logic_flow_parts.append("Runs sequentially from top to bottom.")

    suggestions = ["Consider adding input validation to guard against unexpected values."]
    if "print(" in snippet:
        suggestions.append("Replace print statements with logging when moving to production.")
    if not functions_used:
        suggestions.append("Wrap repeated logic into a reusable function for clarity.")

    return {
        "purpose": purpose,
        "logic_flow": " ".join(logic_flow_parts),
        "functions_used": functions_used,
        "architecture_summary": "Single-file utility snippet with focused logic.",
        "suggestions": suggestions,
    }
