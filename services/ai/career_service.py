from __future__ import annotations

from typing import Dict, List, Tuple

import json

from models import CodingSubmission, Enrollment, UserResume
from services.ai.career.resume_service import SKILL_KEYWORDS


CAREER_ROADMAPS: Dict[str, Dict[str, object]] = {
    "Full Stack Developer": {
        "skills": ["HTML/CSS", "JavaScript", "Flask or backend framework", "SQL", "REST APIs", "Deployment"],
        "recommended_courses": ["React JS", "Python Flask - Full Stack Development", "MERN Stack - Complete Web Development"],
        "projects": ["Portfolio platform", "Learning management dashboard", "E-commerce starter app"],
        "timeline": ["Month 1-2: frontend basics", "Month 3-4: backend and database", "Month 5-6: full-stack projects and deployment"],
    },
    "Data Scientist": {
        "skills": ["Python", "Pandas", "Statistics", "Visualization", "Machine Learning", "Storytelling with data"],
        "recommended_courses": ["Python for Data Science", "Machine Learning Fundamentals", "Data Analytics with Power BI"],
        "projects": ["Student performance analyzer", "Sales insight dashboard", "Prediction notebook portfolio"],
        "timeline": ["Month 1-2: Python and analysis", "Month 3-4: statistics and visualization", "Month 5-6: machine learning projects"],
    },
    "AI Engineer": {
        "skills": ["Python", "Math foundations", "Machine Learning", "Deep Learning", "Model evaluation", "Deployment basics"],
        "recommended_courses": ["Machine Learning Fundamentals", "Deep Learning - Neural Networks", "Natural Language Processing (NLP)"],
        "projects": ["Rule-based mentor bot", "Image classifier prototype", "Learning recommendation assistant"],
        "timeline": ["Month 1-2: ML basics", "Month 3-4: deep learning", "Month 5-6: AI projects and model deployment basics"],
    },
    "Backend Developer": {
        "skills": ["Python", "Flask", "SQL", "REST APIs", "Authentication", "Docker"],
        "recommended_courses": ["Python Flask - Full Stack Development", "AWS Cloud Computing Mastery", "Kubernetes & Docker - Container Mastery"],
        "projects": ["Authentication API", "Course management backend", "Deployment-ready LMS service"],
        "timeline": ["Month 1-2: Python and Flask", "Month 3-4: APIs and databases", "Month 5-6: auth, testing, deployment"],
    },
    "Frontend Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "React", "Responsive design", "Accessibility"],
        "recommended_courses": ["React JS - Modern Web Development", "Next.js - Advanced React Framework", "React Native - Cross-Platform Mobile Apps"],
        "projects": ["Responsive portfolio", "Course discovery UI", "Dashboard redesign challenge"],
        "timeline": ["Month 1-2: HTML/CSS/JS", "Month 3-4: React and component systems", "Month 5-6: advanced UI projects and performance"],
    },
}


def _skills_from_text(text: str) -> List[str]:
    normalized = (text or "").lower()
    detected = []
    for skill, keywords in SKILL_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            detected.append(skill)
    return detected


def _completed_course_data(user_id: int) -> Tuple[List[str], List[str]]:
    completed_titles: List[str] = []
    completed_skills: List[str] = []

    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    for enrollment in enrollments:
        if not enrollment.course:
            continue
        completed = enrollment.completed or (enrollment.progress_percentage or enrollment.progress or 0) >= 100
        if not completed:
            continue
        completed_titles.append(enrollment.course.title)
        course_text = f"{enrollment.course.title or ''} {enrollment.course.description or ''}"
        completed_skills.extend(_skills_from_text(course_text))

    return completed_titles, completed_skills


def _coding_performance(user_id: int) -> Dict[str, object]:
    submissions = CodingSubmission.query.filter_by(user_id=user_id).all()
    if not submissions:
        return {"average_score": None, "weak_topics": []}

    topic_totals: Dict[str, float] = {}
    topic_counts: Dict[str, int] = {}
    total_score = 0.0

    for submission in submissions:
        total_score += submission.score or 0.0
        topic = submission.challenge.topic if submission.challenge else None
        if not topic:
            continue
        topic_totals[topic] = topic_totals.get(topic, 0.0) + (submission.score or 0.0)
        topic_counts[topic] = topic_counts.get(topic, 0) + 1

    average_score = total_score / max(len(submissions), 1)
    topic_averages = [
        (topic, topic_totals[topic] / max(topic_counts.get(topic, 1), 1))
        for topic in topic_totals
    ]
    topic_averages.sort(key=lambda item: item[1])
    weak_topics = [topic for topic, score in topic_averages if score < 70][:3]

    return {
        "average_score": round(average_score, 2),
        "weak_topics": weak_topics,
    }


def _normalized_titles(items: List[str]) -> List[str]:
    return [item.strip().lower() for item in items if item and item.strip()]


def generate_career_roadmap(role: str, user_id: int | None = None) -> Dict[str, object]:
    normalized = (role or "").strip() or "Full Stack Developer"
    roadmap = CAREER_ROADMAPS.get(normalized) or CAREER_ROADMAPS["Full Stack Developer"]
    payload = {
        "role": normalized,
        "skills": roadmap["skills"],
        "recommended_courses": roadmap["recommended_courses"],
        "projects": roadmap["projects"],
        "timeline": roadmap["timeline"],
    }

    ordered_skills = list(roadmap["skills"])
    recommended_courses = list(roadmap["recommended_courses"])
    missing_skills: List[str] = []

    if user_id:
        resume_row = UserResume.query.filter_by(user_id=user_id).first()
        resume_skills = json.loads(resume_row.skills_json or "[]") if resume_row else []
        completed_titles, completed_skills = _completed_course_data(user_id)
        skill_evidence = set(resume_skills) | set(completed_skills)
        missing_skills = [skill for skill in roadmap["skills"] if skill not in skill_evidence]
        ordered_skills = missing_skills + [skill for skill in roadmap["skills"] if skill not in missing_skills]

        completed_normalized = set(_normalized_titles(completed_titles))
        recommended_courses = [
            course for course in roadmap["recommended_courses"]
            if course.strip().lower() not in completed_normalized
        ] or list(roadmap["recommended_courses"])

        coding_perf = _coding_performance(user_id)
        weak_topics = coding_perf.get("weak_topics", [])

        interview_items = [
            f"Mock interview for {normalized} roles",
            "Behavioral questions with STAR responses",
            "System design or architecture walkthroughs",
        ]
        for topic in weak_topics:
            interview_items.insert(0, f"Timed coding challenges in {topic}")
        if coding_perf.get("average_score") is not None and coding_perf["average_score"] < 70:
            interview_items.insert(0, "Increase coding accuracy to 80%+ with weekly practice")

        payload.update({
            "resume_skills": resume_skills,
            "completed_courses": completed_titles,
            "missing_skills": missing_skills,
            "recommended_courses": recommended_courses,
            "coding_performance": coding_perf,
        })

        split_index = max(2, len(ordered_skills) // 2)
        phase_one = ordered_skills[:split_index] or roadmap["skills"][:2]
        phase_two = ordered_skills[split_index:] or roadmap["skills"][split_index:]

        payload["phases"] = [
            {"title": "Phase 1 — Core Skills", "items": phase_one},
            {"title": "Phase 2 — Intermediate Skills", "items": phase_two},
            {"title": "Phase 3 — Projects", "items": roadmap["projects"]},
            {"title": "Phase 4 — Interview Preparation", "items": interview_items},
        ]
    else:
        split_index = max(2, len(ordered_skills) // 2)
        payload["phases"] = [
            {"title": "Phase 1 — Core Skills", "items": ordered_skills[:split_index]},
            {"title": "Phase 2 — Intermediate Skills", "items": ordered_skills[split_index:]},
            {"title": "Phase 3 — Projects", "items": roadmap["projects"]},
            {"title": "Phase 4 — Interview Preparation", "items": ["Mock interviews", "Behavioral prep", "Coding practice drills"]},
        ]

    return payload
