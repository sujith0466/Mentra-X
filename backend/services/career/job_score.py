import json
from collections import defaultdict
from typing import Dict, List

from backend.models import CodingSubmission, Enrollment, ProjectTask, StudentProject, UserResume


def _to_list(raw_value: str) -> List:
    if not raw_value:
        return []
    try:
        parsed = json.loads(raw_value)
        return parsed if isinstance(parsed, list) else []
    except (TypeError, ValueError, json.JSONDecodeError):
        return []


def _resume_component(user_id: int) -> int:
    row = UserResume.query.filter_by(user_id=user_id).first()
    if not row:
        return 0

    skills = _to_list(row.skills_json)
    experiences = _to_list(row.experience_json)

    # Presence + skill density + experience depth.
    score = 4
    score += min(12, len(skills) * 2)
    score += min(9, len(experiences) * 3)
    return max(0, min(25, int(score)))


def _course_component(user_id: int) -> int:
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    if not enrollments:
        return 0

    completed_count = 0
    progress_values: List[float] = []
    for enrollment in enrollments:
        progress = float(enrollment.progress_percentage or enrollment.progress or 0.0)
        progress_values.append(max(0.0, min(100.0, progress)))
        if enrollment.completed or progress >= 100.0:
            completed_count += 1

    avg_progress = sum(progress_values) / len(progress_values) if progress_values else 0.0
    score = min(15, completed_count * 5)
    score += min(10, int(round(avg_progress / 10.0)))
    return max(0, min(25, int(score)))


def _coding_component(user_id: int) -> int:
    submissions = CodingSubmission.query.filter_by(user_id=user_id).all()
    if not submissions:
        return 0

    total = len(submissions)
    successful = 0
    aggregate_score = 0.0

    for submission in submissions:
        submission_score = float(submission.score or 0.0)
        aggregate_score += max(0.0, min(100.0, submission_score))
        if submission_score >= 70.0 or int(submission.passed_tests or 0) > 0:
            successful += 1

    success_rate = successful / total if total else 0.0
    avg_submission_score = aggregate_score / total if total else 0.0

    score = min(8, total * 2)
    score += int(round(success_rate * 10))
    score += min(7, int(round((avg_submission_score / 100.0) * 7)))
    return max(0, min(25, int(score)))


def _project_component(user_id: int) -> int:
    projects = StudentProject.query.filter_by(user_id=user_id).all()
    if not projects:
        return 0

    total_projects = len(projects)
    avg_progress = sum(float(project.progress_percentage or 0.0) for project in projects) / total_projects
    completed_projects = sum(1 for project in projects if project.completed_at is not None)

    project_ids = [project.id for project in projects]
    task_rows = ProjectTask.query.filter(ProjectTask.project_id.in_(project_ids)).all() if project_ids else []
    task_stats: Dict[int, Dict[str, int]] = defaultdict(lambda: {"total": 0, "done": 0})
    for task in task_rows:
        stats = task_stats[task.project_id]
        stats["total"] += 1
        if task.completed:
            stats["done"] += 1

    quality_ready_projects = 0
    for project in projects:
        stats = task_stats.get(project.id)
        if not stats or stats["total"] == 0:
            if float(project.progress_percentage or 0.0) >= 70.0:
                quality_ready_projects += 1
            continue
        ratio = stats["done"] / stats["total"]
        if ratio >= 0.7:
            quality_ready_projects += 1

    completion_ratio = completed_projects / total_projects if total_projects else 0.0
    quality_ratio = quality_ready_projects / total_projects if total_projects else 0.0

    score = min(10, total_projects * 3)
    score += min(10, int(round(max(0.0, min(100.0, avg_progress)) / 10.0)))
    score += int(round(completion_ratio * 3))
    score += int(round(quality_ratio * 2))
    return max(0, min(25, int(score)))


def _build_suggestions(breakdown: Dict[str, int]) -> List[str]:
    suggestions: List[str] = []

    if breakdown.get("resume", 0) < 15:
        suggestions.append("Strengthen your resume with core skills and 2-3 project-focused experience entries.")
    if breakdown.get("courses", 0) < 15:
        suggestions.append("Complete more enrolled courses and push your average learning progress above 70%.")
    if breakdown.get("coding", 0) < 15:
        suggestions.append("Improve coding practice by solving at least 3 challenges this week.")
    if breakdown.get("projects", 0) < 15:
        suggestions.append("Complete 1 more project with clear milestones and a deployable outcome.")

    if not suggestions:
        suggestions.append("Great momentum. Keep refining your portfolio, coding consistency, and resume depth.")

    return suggestions[:4]


def calculate_score(user_id: int) -> Dict[str, object]:
    resume_score = _resume_component(user_id)
    course_score = _course_component(user_id)
    coding_score = _coding_component(user_id)
    project_score = _project_component(user_id)

    total_score = resume_score + course_score + coding_score + project_score
    total_score = max(0, min(100, int(total_score)))

    breakdown = {
        "resume": resume_score,
        "courses": course_score,
        "coding": coding_score,
        "projects": project_score,
    }

    return {
        "score": total_score,
        "breakdown": breakdown,
        "suggestions": _build_suggestions(breakdown),
    }
