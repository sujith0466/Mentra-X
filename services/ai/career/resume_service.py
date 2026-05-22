from __future__ import annotations

from typing import Dict, List


CAREER_SKILL_MAP: Dict[str, List[str]] = {
    "AI Engineer": ["Python", "Machine Learning", "Neural Networks", "Data Processing", "Deep Learning"],
    "Data Scientist": ["Python", "Pandas", "Statistics", "Visualization", "Machine Learning"],
    "Full Stack Developer": ["HTML", "CSS", "JavaScript", "Flask", "SQL", "REST APIs"],
    "Backend Developer": ["Python", "Flask", "REST APIs", "SQL", "Authentication", "Docker"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Responsive Design"],
}

SKILL_KEYWORDS = {
    "Python": ["python"],
    "Machine Learning": ["machine learning", "ml"],
    "Neural Networks": ["neural network", "deep learning", "neural networks"],
    "Data Processing": ["data processing", "data cleaning", "etl"],
    "Deep Learning": ["deep learning"],
    "Pandas": ["pandas"],
    "Statistics": ["statistics", "probability", "hypothesis"],
    "Visualization": ["visualization", "matplotlib", "power bi", "dashboard"],
    "HTML": ["html"],
    "CSS": ["css"],
    "JavaScript": ["javascript", "js"],
    "Flask": ["flask"],
    "SQL": ["sql", "database", "mysql", "sqlite", "postgres"],
    "REST APIs": ["api", "rest", "rest api", "restful"],
    "Authentication": ["authentication", "auth", "login"],
    "React": ["react", "next.js", "nextjs"],
    "Responsive Design": ["responsive", "mobile first", "adaptive"],
    "Data Structures": ["data structures", "dsa", "algorithms", "algorithm"],
    "Docker": ["docker", "containers", "containerization", "kubernetes"],
}

EXPERIENCE_KEYWORDS = {
    "projects": ["project", "portfolio", "built", "developed", "created", "implemented"],
    "internship": ["intern", "internship", "trainee"],
    "teamwork": ["collaborated", "team", "worked with"],
}


def analyze_resume(text: str) -> Dict[str, object]:
    normalized = (text or "").lower()
    detected_skills = []
    for skill, keywords in SKILL_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            detected_skills.append(skill)

    experience_indicators = [
        label.title()
        for label, keywords in EXPERIENCE_KEYWORDS.items()
        if any(keyword in normalized for keyword in keywords)
    ]

    career_scores = []
    for career, required_skills in CAREER_SKILL_MAP.items():
        score = sum(1 for skill in required_skills if skill in detected_skills)
        if score > 0:
            career_scores.append((career, score))
    career_scores.sort(key=lambda item: item[1], reverse=True)

    career_matches = [item[0] for item in career_scores[:3]] or ["Full Stack Developer"]
    primary_career = career_matches[0]
    missing_skills = [skill for skill in CAREER_SKILL_MAP[primary_career] if skill not in detected_skills]

    suggestions = []
    if not detected_skills:
        suggestions.append("Add a clear skills section listing languages, frameworks, tools, and databases you actually used.")
    if not experience_indicators:
        suggestions.append("Add project or experience bullet points showing what you built and the impact of your work.")
    if missing_skills:
        suggestions.append(f"For the {primary_career} path, strengthen these skills: {', '.join(missing_skills[:4])}.")
    if "projects" not in [item.lower() for item in experience_indicators]:
        suggestions.append("Include 2-3 project bullets with technologies used, not just course names.")

    return {
        "detected_skills": detected_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "career_matches": career_matches,
        "experience_indicators": experience_indicators,
    }
