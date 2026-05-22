from __future__ import annotations

from typing import Dict, List, Set

import json

from models import CodingChallenge, CodingSubmission, Enrollment, LearningStreak, StudentProject, User, UserResume
from services.ai.career.resume_service import SKILL_KEYWORDS
from services.ai.project_idea_service import generate_project_ideas


def _skills_from_text(text: str) -> List[str]:
    normalized = (text or "").lower()
    detected = []
    for skill, keywords in SKILL_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            detected.append(skill)
    return detected


def _extract_course_skills(course_titles: List[str]) -> List[str]:
    skills = set()
    for title in course_titles:
        skills.update(_skills_from_text(title))
    return sorted(skills)


def _best_coding_challenges(user_id: int) -> List[Dict[str, object]]:
    submissions = CodingSubmission.query.filter_by(user_id=user_id).all()
    best_by_challenge: Dict[int, CodingSubmission] = {}
    for submission in submissions:
        if submission.challenge_id is None:
            continue
        current = best_by_challenge.get(submission.challenge_id)
        if current is None or (submission.score or 0) > (current.score or 0):
            best_by_challenge[submission.challenge_id] = submission

    results: List[Dict[str, object]] = []
    for challenge_id, submission in best_by_challenge.items():
        challenge = CodingChallenge.query.get(challenge_id)
        if not challenge:
            continue
        results.append(
            {
                "title": challenge.title,
                "topic": challenge.topic,
                "score": float(submission.score or 0),
                "passed_tests": submission.passed_tests,
            }
        )
    results.sort(key=lambda item: item.get("score", 0), reverse=True)
    return results


def _dominant_domain(enrollments: List[Enrollment], resume_skills: List[str]) -> str:
    for row in enrollments:
        if row.course and row.course.domain:
            return row.course.domain.name
    if any(skill in resume_skills for skill in ["React", "JavaScript", "HTML", "CSS"]):
        return "Web Development"
    if any(skill in resume_skills for skill in ["Machine Learning", "Deep Learning", "Neural Networks"]):
        return "AI"
    if any(skill in resume_skills for skill in ["Pandas", "Statistics", "Visualization"]):
        return "Data Science"
    return "AI"


def generate_portfolio(user_id: int) -> Dict[str, object]:
    user = User.query.get_or_404(user_id)
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    completed_courses = [
        row.course.title for row in enrollments
        if row.course and (row.completed or (row.progress_percentage or row.progress or 0) >= 100)
    ]
    enrolled_courses = [row.course.title for row in enrollments if row.course and row.course.title]

    resume_row = UserResume.query.filter_by(user_id=user_id).first()
    resume_skills = []
    resume_projects = []
    if resume_row:
        resume_skills = json.loads(resume_row.skills_json or "[]")
        resume_projects = json.loads(resume_row.projects_json or "[]")

    completed_projects = [
        row.project_idea.title
        for row in StudentProject.query.filter_by(user_id=user_id).all()
        if row.project_idea and row.completed_at
    ]

    coding_challenges = _best_coding_challenges(user_id)
    solved_challenges = [item for item in coding_challenges if item.get("score", 0) >= 70]

    skills: Set[str] = set(resume_skills)
    skills.update(_extract_course_skills(enrolled_courses))
    skills.update(item.get("topic") for item in coding_challenges if item.get("topic"))

    dominant_domain = _dominant_domain(enrollments, resume_skills)
    suggested_projects = generate_project_ideas(dominant_domain, user_id=user_id)

    projects = []
    projects.extend(resume_projects)
    projects.extend(completed_projects)
    if not projects:
        projects = [project["title"] for project in suggested_projects[:3]]

    streak = LearningStreak.query.filter_by(user_id=user_id).first()
    achievements = []
    if completed_courses:
        achievements.append(f"Completed {len(completed_courses)} course(s) on Mentra")
    if solved_challenges:
        achievements.append(f"Solved {len(solved_challenges)} coding challenge(s)")
    if streak and streak.longest_streak:
        achievements.append(f"Longest learning streak: {streak.longest_streak} days")
    if resume_projects:
        achievements.append("Resume projects imported into portfolio")
    if completed_projects:
        achievements.append(f"Completed {len(completed_projects)} portfolio project(s)")
    if not achievements:
        achievements.append("Started building a learning portfolio on Mentra")

    profile_summary = "Mentra learner portfolio snapshot"
    if resume_row:
        profile_summary = "Resume + learning data portfolio snapshot"

    return {
        "name": user.name,
        "profile_summary": profile_summary,
        "skills": sorted({skill for skill in skills if skill}),
        "projects": projects,
        "courses_completed": completed_courses,
        "coding_challenges": coding_challenges[:6],
        "achievements": achievements,
    }
