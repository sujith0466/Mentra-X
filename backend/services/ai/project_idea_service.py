from __future__ import annotations

from typing import Dict, List, Optional, Set

import json

from backend.models import Enrollment, UserResume
from backend.services.ai.career.resume_service import SKILL_KEYWORDS


PROJECT_IDEAS: Dict[str, List[Dict[str, object]]] = {
    "AI": [
        {
            "title": "AI Study Planner",
            "description": "Build a planner that suggests daily learning tasks based on weak topics and completed lessons.",
            "features": ["Daily task suggestions", "Weak-topic focus", "Progress summary", "Streak reminders"],
            "tech_stack": ["Python", "Flask", "Jinja", "SQLite"],
            "difficulty": "Intermediate",
        },
        {
            "title": "Rule-Based AI Mentor",
            "description": "Create a mentor assistant that answers student questions using keyword and domain matching.",
            "features": ["Context-aware replies", "Domain knowledge mapping", "Suggested follow-up questions"],
            "tech_stack": ["Python", "Flask", "Rule engine", "HTML/CSS"],
            "difficulty": "Beginner",
        },
    ],
    "Web Development": [
        {
            "title": "Mentor Portfolio Hub",
            "description": "Create a portfolio site where students can showcase projects, skills, and contact links.",
            "features": ["Project gallery", "Skill tags", "Resume section", "Responsive design"],
            "tech_stack": ["Flask", "HTML", "CSS", "JavaScript"],
            "difficulty": "Intermediate",
        },
        {
            "title": "Course Tracker Dashboard",
            "description": "Build a dashboard that visualizes enrolled courses, progress, and upcoming assessments.",
            "features": ["Progress charts", "Course cards", "Reminder panel", "Certificate list"],
            "tech_stack": ["Flask", "Jinja", "SQLite", "Chart-ready UI"],
            "difficulty": "Beginner",
        },
    ],
    "Python": [
        {
            "title": "CLI Task Coach",
            "description": "Create a command-line app that tracks study tasks, reminders, and progress logs.",
            "features": ["Task manager", "Deadline reminders", "Progress export"],
            "tech_stack": ["Python", "argparse", "JSON or SQLite"],
            "difficulty": "Beginner",
        },
        {
            "title": "Automation Notes Organizer",
            "description": "Build a tool that groups notes by topic and generates study summaries.",
            "features": ["Topic grouping", "Summary generation", "Search by keyword"],
            "tech_stack": ["Python", "Flask or CLI", "SQLite"],
            "difficulty": "Intermediate",
        },
    ],
    "Data Science": [
        {
            "title": "Student Performance Analyzer",
            "description": "Analyze quiz and assignment trends to identify weak and strong areas for a learner.",
            "features": ["Trend summaries", "Weak-skill detection", "Visual metrics"],
            "tech_stack": ["Python", "Pandas", "Flask", "SQLite"],
            "difficulty": "Intermediate",
        },
        {
            "title": "Course Insight Dashboard",
            "description": "Build a dashboard that explores enrollments, completion rates, and domain popularity.",
            "features": ["Enrollment analysis", "Completion insights", "Domain comparisons"],
            "tech_stack": ["Python", "Pandas", "Matplotlib-ready backend", "Flask"],
            "difficulty": "Intermediate",
        },
    ],
    "Machine Learning": [
        {
            "title": "Model Comparison Studio",
            "description": "Compare simple ML models on the same dataset and explain accuracy differences.",
            "features": ["Dataset upload", "Model metrics", "Result explanation"],
            "tech_stack": ["Python", "scikit-learn", "Flask"],
            "difficulty": "Advanced",
        },
        {
            "title": "Skill Gap Predictor",
            "description": "Use rule-based inputs or basic scoring to estimate which learning topics a student should revisit.",
            "features": ["Topic scoring", "Recommendation summary", "Improvement plan"],
            "tech_stack": ["Python", "Flask", "SQLite"],
            "difficulty": "Intermediate",
        },
    ],
    "Cybersecurity": [
        {
            "title": "Security Checklist Assistant",
            "description": "Create a learning app that walks users through security checks for a sample web project.",
            "features": ["Checklist workflow", "Risk labels", "Best practice notes"],
            "tech_stack": ["Flask", "Python", "HTML/CSS"],
            "difficulty": "Beginner",
        },
        {
            "title": "Incident Log Trainer",
            "description": "Build a training dashboard where users review sample incidents and choose a response action.",
            "features": ["Scenario cards", "Decision feedback", "Difficulty levels"],
            "tech_stack": ["Python", "Flask", "SQLite"],
            "difficulty": "Intermediate",
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


def _skills_from_text(text: str) -> List[str]:
    normalized = (text or "").lower()
    detected = []
    for skill, keywords in SKILL_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            detected.append(skill)
    return detected


def _extract_user_skills(user_id: int) -> Set[str]:
    skills: Set[str] = set()
    resume_row = UserResume.query.filter_by(user_id=user_id).first()
    if resume_row:
        try:
            skills.update(json.loads(resume_row.skills_json or "[]"))
        except (TypeError, ValueError, json.JSONDecodeError):
            pass
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    for enrollment in enrollments:
        if not enrollment.course:
            continue
        course_text = f"{enrollment.course.title or ''} {enrollment.course.description or ''}"
        skills.update(_skills_from_text(course_text))
    return skills


def _personalized_ideas(skills: Set[str], domain: str) -> List[Dict[str, object]]:
    personalized: List[Dict[str, object]] = []
    if {"Python", "Flask", "SQL"}.issubset(skills):
        personalized.extend(
            [
                {
                    "title": "AI Study Planner",
                    "description": "Create a personalized study planner that adapts to weak topics and quiz results.",
                    "features": ["Adaptive schedule", "Weak-topic focus", "Progress analytics"],
                    "tech_stack": ["Python", "Flask", "SQL", "Jinja"],
                    "difficulty": "Intermediate",
                },
                {
                    "title": "Task Automation Tool",
                    "description": "Build an automation tool that converts study checklists into scheduled tasks.",
                    "features": ["Task scheduling", "Reminder engine", "Completion tracking"],
                    "tech_stack": ["Python", "Flask", "SQLite", "Celery or cron"],
                    "difficulty": "Intermediate",
                },
                {
                    "title": "Learning Analytics Dashboard",
                    "description": "Deliver dashboards that visualize course progress, quiz performance, and skill gaps.",
                    "features": ["Performance charts", "Skill gap insights", "Weekly reports"],
                    "tech_stack": ["Python", "Flask", "SQL", "Charts"],
                    "difficulty": "Intermediate",
                },
            ]
        )

    if {"JavaScript", "React"}.intersection(skills):
        personalized.append(
            {
                "title": "Progress Tracker Web App",
                "description": "Build a responsive tracker for courses, quizzes, and certifications.",
                "features": ["Progress cards", "Completion stats", "Streak widget"],
                "tech_stack": ["React", "JavaScript", "API integration"],
                "difficulty": "Intermediate",
            }
        )

    if {"Machine Learning", "Pandas", "Statistics"}.intersection(skills):
        personalized.append(
            {
                "title": "Skill Gap Predictor",
                "description": "Analyze learning signals to recommend the next best topics and courses.",
                "features": ["Weak-topic scoring", "Skill recommendations", "Course matches"],
                "tech_stack": ["Python", "Pandas", "Flask", "SQLite"],
                "difficulty": "Advanced" if "Machine Learning" in skills else "Intermediate",
            }
        )

    if not personalized and domain in PROJECT_IDEAS:
        personalized.extend(PROJECT_IDEAS[domain][:2])

    return personalized


def generate_project_ideas(domain: str, user_id: Optional[int] = None) -> List[Dict[str, object]]:
    normalized = normalize_domain(domain)
    if user_id:
        skills = _extract_user_skills(user_id)
        personalized = _personalized_ideas(skills, normalized)
        if personalized:
            seen = set()
            merged = []
            for idea in personalized + (PROJECT_IDEAS.get(normalized) or PROJECT_IDEAS["AI"]):
                title = idea.get("title")
                if not title or title in seen:
                    continue
                seen.add(title)
                if "difficulty" not in idea:
                    idea["difficulty"] = "Intermediate"
                merged.append(idea)
            return merged

    ideas = PROJECT_IDEAS.get(normalized)
    if ideas:
        return ideas
    return PROJECT_IDEAS["AI"]
