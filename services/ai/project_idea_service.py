from __future__ import annotations

from typing import Dict, List


PROJECT_IDEAS: Dict[str, List[Dict[str, object]]] = {
    "AI": [
        {
            "title": "AI Study Planner",
            "description": "Build a planner that suggests daily learning tasks based on weak topics and completed lessons.",
            "features": ["Daily task suggestions", "Weak-topic focus", "Progress summary", "Streak reminders"],
            "tech_stack": ["Python", "Flask", "Jinja", "SQLite"],
        },
        {
            "title": "Rule-Based AI Mentor",
            "description": "Create a mentor assistant that answers student questions using keyword and domain matching.",
            "features": ["Context-aware replies", "Domain knowledge mapping", "Suggested follow-up questions"],
            "tech_stack": ["Python", "Flask", "Rule engine", "HTML/CSS"],
        },
    ],
    "Web Development": [
        {
            "title": "Mentor Portfolio Hub",
            "description": "Create a portfolio site where students can showcase projects, skills, and contact links.",
            "features": ["Project gallery", "Skill tags", "Resume section", "Responsive design"],
            "tech_stack": ["Flask", "HTML", "CSS", "JavaScript"],
        },
        {
            "title": "Course Tracker Dashboard",
            "description": "Build a dashboard that visualizes enrolled courses, progress, and upcoming assessments.",
            "features": ["Progress charts", "Course cards", "Reminder panel", "Certificate list"],
            "tech_stack": ["Flask", "Jinja", "SQLite", "Chart-ready UI"],
        },
    ],
    "Python": [
        {
            "title": "CLI Task Coach",
            "description": "Create a command-line app that tracks study tasks, reminders, and progress logs.",
            "features": ["Task manager", "Deadline reminders", "Progress export"],
            "tech_stack": ["Python", "argparse", "JSON or SQLite"],
        },
        {
            "title": "Automation Notes Organizer",
            "description": "Build a tool that groups notes by topic and generates study summaries.",
            "features": ["Topic grouping", "Summary generation", "Search by keyword"],
            "tech_stack": ["Python", "Flask or CLI", "SQLite"],
        },
    ],
    "Data Science": [
        {
            "title": "Student Performance Analyzer",
            "description": "Analyze quiz and assignment trends to identify weak and strong areas for a learner.",
            "features": ["Trend summaries", "Weak-skill detection", "Visual metrics"],
            "tech_stack": ["Python", "Pandas", "Flask", "SQLite"],
        },
        {
            "title": "Course Insight Dashboard",
            "description": "Build a dashboard that explores enrollments, completion rates, and domain popularity.",
            "features": ["Enrollment analysis", "Completion insights", "Domain comparisons"],
            "tech_stack": ["Python", "Pandas", "Matplotlib-ready backend", "Flask"],
        },
    ],
    "Machine Learning": [
        {
            "title": "Model Comparison Studio",
            "description": "Compare simple ML models on the same dataset and explain accuracy differences.",
            "features": ["Dataset upload", "Model metrics", "Result explanation"],
            "tech_stack": ["Python", "scikit-learn", "Flask"],
        },
        {
            "title": "Skill Gap Predictor",
            "description": "Use rule-based inputs or basic scoring to estimate which learning topics a student should revisit.",
            "features": ["Topic scoring", "Recommendation summary", "Improvement plan"],
            "tech_stack": ["Python", "Flask", "SQLite"],
        },
    ],
    "Cybersecurity": [
        {
            "title": "Security Checklist Assistant",
            "description": "Create a learning app that walks users through security checks for a sample web project.",
            "features": ["Checklist workflow", "Risk labels", "Best practice notes"],
            "tech_stack": ["Flask", "Python", "HTML/CSS"],
        },
        {
            "title": "Incident Log Trainer",
            "description": "Build a training dashboard where users review sample incidents and choose a response action.",
            "features": ["Scenario cards", "Decision feedback", "Difficulty levels"],
            "tech_stack": ["Python", "Flask", "SQLite"],
        },
    ],
}


ALIASES = {
    "artificial intelligence": "AI",
    "web": "Web Development",
    "python programming": "Python",
    "data science": "Data Science",
    "machine learning": "Machine Learning",
    "cyber security": "Cybersecurity",
    "cybersecurity": "Cybersecurity",
}


def normalize_domain(domain: str) -> str:
    cleaned = (domain or "").strip()
    if not cleaned:
        return "AI"
    return ALIASES.get(cleaned.lower(), cleaned)


def generate_project_ideas(domain: str) -> List[Dict[str, object]]:
    normalized = normalize_domain(domain)
    ideas = PROJECT_IDEAS.get(normalized)
    if ideas:
        return ideas
    return PROJECT_IDEAS["AI"]

