from __future__ import annotations

from typing import Dict, List

import json

from models import UserResume


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
        "skills": ["Python", "Flask", "SQL", "Authentication", "REST APIs", "Testing fundamentals"],
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


def generate_career_roadmap(role: str, user_id: int | None = None) -> Dict[str, object]:
    normalized = (role or "").strip()
    roadmap = CAREER_ROADMAPS.get(normalized) or CAREER_ROADMAPS["Full Stack Developer"]
    payload = {
        "role": normalized or "Full Stack Developer",
        "skills": roadmap["skills"],
        "recommended_courses": roadmap["recommended_courses"],
        "projects": roadmap["projects"],
        "timeline": roadmap["timeline"],
    }
    if user_id:
        resume_row = UserResume.query.filter_by(user_id=user_id).first()
        if resume_row:
            resume_skills = json.loads(resume_row.skills_json or "[]")
            missing_skills = [skill for skill in roadmap["skills"] if skill not in resume_skills]
            payload["resume_skills"] = resume_skills
            payload["missing_skills"] = missing_skills
    return payload
