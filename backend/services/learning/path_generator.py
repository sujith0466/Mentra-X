"""
Smart Learning Path 2.0 — Service (Feature 6 — Phase B)

Generates a personalised learning path for a student based on:
  • completed / in-progress courses
  • skill gaps (SkillProgress table)
  • overall progress percentage

All logic is local — NO paid APIs.
"""

from __future__ import annotations

from sqlalchemy.orm import joinedload
from backend.models import (
    db, Enrollment, Course, SkillProgress,
    CodingSubmission, QuizAttempt,
)
from backend.services.career.job_score import calculate_score
from backend.services.ai.career.skill_gap_service import detect_skill_gap


# ---------------------------------------------------------------------------
# Internal topic → prerequisite / next-step mapping
# ---------------------------------------------------------------------------
_LEARNING_GRAPH: dict[str, list[str]] = {
    # Web development track
    "HTML": ["CSS", "JavaScript"],
    "CSS": ["JavaScript", "Bootstrap"],
    "JavaScript": ["React", "Node.js", "TypeScript"],
    "React": ["Next.js", "Redux", "React Native"],
    "Node.js": ["Express", "MongoDB", "REST APIs"],
    "Next.js": ["Full Stack Projects"],

    # Python / Data Science track
    "Python": ["Flask", "Django", "Pandas", "NumPy"],
    "Flask": ["REST APIs", "Flask Full-Stack"],
    "Django": ["REST APIs", "Django REST Framework"],
    "Pandas": ["Data Visualization", "Machine Learning"],
    "NumPy": ["Machine Learning", "Deep Learning"],
    "Machine Learning": ["Deep Learning", "NLP", "Computer Vision"],
    "Deep Learning": ["NLP", "Computer Vision", "Generative AI"],

    # Mobile
    "Flutter": ["Dart Advanced", "Firebase", "Flutter State Management"],
    "React Native": ["Mobile Navigation", "Native Modules"],

    # DevOps
    "Docker": ["Kubernetes", "CI/CD"],
    "AWS": ["Cloud Architecture", "Terraform"],

    # Security
    "Ethical Hacking": ["Network Security", "Penetration Testing"],
}

_DIFFICULTY_ORDER = ["easy", "medium", "hard"]


def _avg_progress(enrollments: list[Enrollment]) -> float:
    """Average progress across all enrollments (0–100)."""
    if not enrollments:
        return 0.0
    total = sum(
        (e.progress_percentage if e.progress_percentage is not None else (e.progress or 0.0))
        for e in enrollments
    )
    return round(total / len(enrollments), 2)


def _infer_difficulty(avg: float) -> str:
    """Map average course progress to a difficulty recommendation."""
    if avg < 30:
        return "easy"
    if avg < 70:
        return "medium"
    return "hard"


def _estimate_weeks(num_courses: int, difficulty: str) -> str:
    """Rough estimate for how long the suggested path will take."""
    base = 2 if difficulty == "easy" else (3 if difficulty == "medium" else 4)
    weeks = max(1, num_courses * base)
    if weeks == 1:
        return "1 week"
    return f"{weeks} weeks"


def _skills_from_enrollments(enrollments: list[Enrollment]) -> set[str]:
    """Extract skill keywords from enrolled course titles."""
    skills: set[str] = set()
    for e in enrollments:
        if e.course:
            title = (e.course.title or "").lower()
            for keyword in _LEARNING_GRAPH.keys():
                if keyword.lower() in title:
                    skills.add(keyword)
    return skills


def generate_learning_path(user_id: int) -> dict:
    """
    Build a smart learning path for the given student.

    Returns
    -------
    dict
        {
            "next_courses": [{"title": ..., "reason": ...}, ...],
            "difficulty": "easy" | "medium" | "hard",
            "estimated_time": "X weeks",
            "completed_courses": int,
            "average_progress": float,
            "known_skills": [str, ...],
        }
    """
    enrollments = (
        Enrollment.query
        .options(joinedload(Enrollment.course))
        .filter_by(user_id=user_id)
        .all()
    )
    completed = [e for e in enrollments if e.completed or (e.progress_percentage or 0) >= 100]
    avg = _avg_progress(enrollments)
    difficulty = _infer_difficulty(avg)
    known_skills = _skills_from_enrollments(enrollments)
    weak_areas: list[str] = []
    score_data = calculate_score(user_id)
    score_breakdown = score_data.get("breakdown", {})

    # Gather skill-gap info from SkillProgress
    skill_rows = SkillProgress.query.filter_by(user_id=user_id).all()
    for row in skill_rows:
        if row.progress_percentage and row.progress_percentage >= 40:
            known_skills.add(row.skill_name)
        elif row.progress_percentage is not None and row.progress_percentage < 40:
            weak_areas.append(row.skill_name)

    # Build next-course suggestions from the learning graph
    next_course_set: dict[str, str] = {}  # title → reason

    for skill in known_skills:
        next_topics = _LEARNING_GRAPH.get(skill, [])
        for nt in next_topics:
            if nt not in known_skills and nt not in next_course_set:
                next_course_set[nt] = f"Recommended after mastering {skill}"

    # Boost weak-area recovery suggestions first.
    for weak in weak_areas[:3]:
        if weak in _LEARNING_GRAPH:
            for candidate in _LEARNING_GRAPH[weak]:
                if candidate not in known_skills and candidate not in next_course_set:
                    next_course_set[candidate] = f"Priority reinforcement for weak area: {weak}"

    coding_component = int(score_breakdown.get("coding", 0) or 0)
    project_component = int(score_breakdown.get("projects", 0) or 0)
    if coding_component < 15:
        for topic in ("Python", "JavaScript", "Problem Solving", "Data Structures"):
            if topic not in known_skills and topic not in next_course_set:
                next_course_set[topic] = "Prioritized due to low coding score."
    if project_component < 15:
        for topic in ("Full Stack Projects", "REST APIs", "React", "Flask Full-Stack"):
            if topic not in known_skills and topic not in next_course_set:
                next_course_set[topic] = "Prioritized due to low project readiness score."

    # If the graph produced nothing, suggest beginner entries
    if not next_course_set:
        if not enrollments:
            next_course_set = {
                "Python": "Great first language for beginners",
                "HTML": "Start your web development journey",
                "Flutter": "Build cross-platform mobile apps",
            }
        else:
            # Suggest courses the student hasn't started yet
            enrolled_ids = {e.course_id for e in enrollments}
            course_query = Course.query.filter(Course.status == 'published')
            if enrolled_ids:
                course_query = course_query.filter(~Course.id.in_(enrolled_ids))
            unenrolled = (
                course_query
                .order_by(Course.created_at.desc())
                .limit(5)
                .all()
            )
            for course in unenrolled:
                next_course_set[course.title] = "Popular course you haven't started yet"

    # Cap at 6 suggestions
    suggestions = [
        {"title": title, "reason": reason}
        for title, reason in list(next_course_set.items())[:6]
    ]

    gap_payload = detect_skill_gap(user_id, "Full Stack Developer")
    missing_skills = gap_payload.get("skills_missing", [])[:6]
    gap_courses = gap_payload.get("recommended_courses", [])[:5]
    for course_title in gap_courses:
        if all(item["title"] != course_title for item in suggestions):
            suggestions.append({
                "title": course_title,
                "reason": "Recommended from your current skill gap analysis.",
            })
        if len(suggestions) >= 6:
            break

    # Priority reasoning based on performance signals.
    priority = "low"
    reason = "Steady progress detected. Continue with the next suggested topics."
    coding_scores = [
        float(score or 0.0)
        for (score,) in db.session.query(CodingSubmission.score).filter_by(user_id=user_id).all()
    ]
    quiz_scores = [
        float(score_pct or 0.0)
        for (score_pct,) in db.session.query(QuizAttempt.score_percentage).filter_by(user_id=user_id).all()
    ]

    avg_coding = round(sum(coding_scores) / len(coding_scores), 1) if coding_scores else None
    avg_quiz = round(sum(quiz_scores) / len(quiz_scores), 1) if quiz_scores else None

    if weak_areas or (avg_coding is not None and avg_coding < 50) or (avg_quiz is not None and avg_quiz < 50):
        priority = "high"
        if avg_coding is not None and avg_coding < 50:
            reason = "Low coding performance detected. Prioritize fundamentals and guided practice."
        elif avg_quiz is not None and avg_quiz < 50:
            reason = "Low quiz performance detected. Focus on revision-oriented next courses."
        elif weak_areas:
            reason = f"Weak skill areas detected: {', '.join(weak_areas[:3])}."
    elif avg < 60:
        priority = "medium"
        reason = "Moderate progress detected. Maintain consistency and complete in-progress modules."
    elif coding_component < 15 or project_component < 15:
        priority = "medium"
        reason = "Career readiness score indicates coding or project improvement opportunities."

    next_action = (
        f"Complete '{suggestions[0]['title']}' next."
        if suggestions else
        "Complete one in-progress course module today."
    )

    return {
        "next_courses": suggestions,
        "difficulty": difficulty,
        "estimated_time": _estimate_weeks(len(suggestions), difficulty),
        "completed_courses": len(completed),
        "average_progress": avg,
        "known_skills": sorted(known_skills),
        "priority": priority,
        "reason": reason,
        "weak_areas": weak_areas[:5],
        "based_on_score": score_breakdown,
        "missing_skills": missing_skills,
        "recommended_courses": gap_courses,
        "next_action": next_action,
    }
