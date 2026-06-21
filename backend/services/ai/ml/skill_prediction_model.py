from __future__ import annotations

from collections import Counter
from typing import Dict, List

from backend.models import Enrollment, Quiz, QuizAttempt
from backend.services.ai.career.resume_service import CAREER_SKILL_MAP
from backend.services.ai.career.skill_gap_service import detect_skill_gap

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None


DOMAIN_SKILLS = {
    "AI": ["Python", "Machine Learning", "Data Processing", "Model Evaluation"],
    "Artificial Intelligence": ["Python", "Machine Learning", "Neural Networks", "Data Processing"],
    "Web Development": ["HTML", "CSS", "JavaScript", "Flask", "SQL"],
    "Python": ["Python", "Automation", "Problem Solving", "APIs"],
    "Data Science": ["Python", "Pandas", "Statistics", "Visualization"],
    "Machine Learning": ["Python", "Machine Learning", "Feature Engineering", "Model Evaluation"],
    "Cybersecurity": ["Networking", "Linux", "Security Basics", "Risk Analysis"],
}


def _infer_career_goal(user_id: int) -> str:
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    domain_counter = Counter(
        row.course.domain.name
        for row in enrollments
        if row.course and row.course.domain and row.course.domain.name
    )
    top_domain = domain_counter.most_common(1)
    if not top_domain:
        return "Full Stack Developer"

    domain_name = top_domain[0][0].lower()
    if "ai" in domain_name or "machine" in domain_name:
        return "AI Engineer"
    if "data" in domain_name:
        return "Data Scientist"
    if "backend" in domain_name:
        return "Backend Developer"
    if "frontend" in domain_name or "web" in domain_name:
        return "Full Stack Developer"
    return "Full Stack Developer"


def predict_next_skills(user_id: int) -> Dict[str, List[str]]:
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    completed_courses = [
        row.course for row in enrollments
        if row.course and (row.completed or (row.progress_percentage or row.progress or 0) >= 100)
    ]
    domain_skills: List[str] = []
    for course in completed_courses:
        if course.domain and course.domain.name in DOMAIN_SKILLS:
            domain_skills.extend(DOMAIN_SKILLS[course.domain.name])

    quiz_attempts = QuizAttempt.query.filter_by(user_id=user_id).all()
    low_score_topics: List[str] = []
    for attempt in quiz_attempts:
        quiz = Quiz.query.get(attempt.quiz_id)
        if quiz and (attempt.score_percentage or 0) < 70:
            if quiz.course and quiz.course.domain:
                low_score_topics.extend(DOMAIN_SKILLS.get(quiz.course.domain.name, []))

    dominant_goal = _infer_career_goal(user_id)
    target_skills = CAREER_SKILL_MAP.get(dominant_goal, [])
    combined_skills = domain_skills + low_score_topics
    if pd is not None:
        learned_skills = list(dict.fromkeys(pd.Series(combined_skills).dropna().tolist()))
    else:
        learned_skills = list(dict.fromkeys(skill for skill in combined_skills if skill))
    gap_payload = detect_skill_gap(user_id, dominant_goal)

    missing = [skill for skill in target_skills if skill not in learned_skills]
    if not missing:
        missing = gap_payload.get("skills_missing", [])[:4]

    recommended_projects = gap_payload.get("recommended_projects", [])
    if not recommended_projects:
        recommended_projects = [f"Build a mini project using {skill}" for skill in missing[:3]]

    if np is not None and missing:
        confidence_weights = np.linspace(0.9, 0.6, num=len(missing)).round(2).tolist()
    else:
        confidence_weights = [round(0.9 - (index * 0.1), 2) for index in range(len(missing))]
    skills_to_learn_next = [f"{skill} ({confidence_weights[index]})" for index, skill in enumerate(missing[:5])]

    return {
        "skills_to_learn_next": skills_to_learn_next,
        "recommended_projects": recommended_projects[:4],
    }
