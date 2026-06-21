from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Dict, List

from models import AssignmentSubmission, Course, CourseModule, Enrollment, Quiz, QuizAttempt, SkillProgress, db
from services.ai.skills.skill_mapping import infer_skills_for_course


def _course_modules(course_id: int) -> List[CourseModule]:
    return CourseModule.query.filter_by(course_id=course_id).order_by(CourseModule.order_index.asc(), CourseModule.id.asc()).all()


def _course_skills(course: Course) -> List[str]:
    modules = _course_modules(course.id)
    return infer_skills_for_course(course.title, [module.title for module in modules])


def _normalize_percentage(value: float) -> float:
    return round(max(0.0, min(float(value or 0.0), 100.0)), 2)


def build_skill_graph(user_id: int | None = None) -> List[Dict[str, object]]:
    graph: Dict[str, Dict[str, object]] = {}
    courses = Course.query.filter((Course.status == "published") | (Course.status == None)).all()

    for course in courses:
        skills = _course_skills(course)
        modules = _course_modules(course.id)
        for skill in skills:
            entry = graph.setdefault(skill, {
                "skill_name": skill,
                "courses": [],
                "modules": [],
                "progress_percentage": 0.0,
            })
            if course.title not in entry["courses"]:
                entry["courses"].append(course.title)
            for module in modules:
                if module.title not in entry["modules"]:
                    entry["modules"].append(module.title)

    if user_id:
        update_skill_progress_for_user(user_id)
        progress_rows = SkillProgress.query.filter_by(user_id=user_id).all()
        progress_map = {row.skill_name: row.progress_percentage for row in progress_rows}
        for skill_name, percentage in progress_map.items():
            if skill_name not in graph:
                graph[skill_name] = {
                    "skill_name": skill_name,
                    "courses": [],
                    "modules": [],
                    "progress_percentage": _normalize_percentage(percentage),
                }
            else:
                graph[skill_name]["progress_percentage"] = _normalize_percentage(percentage)

    return sorted(graph.values(), key=lambda item: item["skill_name"])


def update_skill_progress_for_user(user_id: int) -> List[SkillProgress]:
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    quiz_attempts = QuizAttempt.query.filter_by(user_id=user_id).all()
    assignment_submissions = AssignmentSubmission.query.filter_by(user_id=user_id).all()

    quiz_scores_by_course: Dict[int, List[float]] = defaultdict(list)
    for attempt in quiz_attempts:
        quiz = Quiz.query.get(attempt.quiz_id)
        if quiz and quiz.course_id:
            quiz_scores_by_course[quiz.course_id].append(float(attempt.score_percentage or 0.0))

    assignment_scores_by_course: Dict[int, List[float]] = defaultdict(list)
    for submission in assignment_submissions:
        if submission.assignment and submission.assignment.course_id and submission.marks_awarded is not None:
            course = submission.assignment.course_id
            assignment_scores_by_course[course].append(float(submission.marks_awarded or 0.0))

    updated_rows: List[SkillProgress] = []
    for enrollment in enrollments:
        course = enrollment.course
        if not course:
            continue
        progress_value = float(enrollment.progress_percentage or enrollment.progress or 0.0)
        quiz_scores = quiz_scores_by_course.get(course.id, [])
        assignment_scores = assignment_scores_by_course.get(course.id, [])
        quiz_component = sum(quiz_scores) / len(quiz_scores) if quiz_scores else progress_value
        assignment_component = sum(assignment_scores) / len(assignment_scores) if assignment_scores else progress_value
        combined = _normalize_percentage((progress_value * 0.5) + (quiz_component * 0.3) + (assignment_component * 0.2))

        for skill_name in _course_skills(course):
            row = SkillProgress.query.filter_by(user_id=user_id, skill_name=skill_name).first()
            if not row:
                row = SkillProgress(user_id=user_id, skill_name=skill_name)
                db.session.add(row)
            row.progress_percentage = combined
            row.last_updated = datetime.utcnow()
            updated_rows.append(row)

    db.session.commit()
    return updated_rows


def get_skill_progress_snapshot(user_id: int) -> List[Dict[str, object]]:
    graph = build_skill_graph(user_id)
    return [
        {
            "skill_name": item["skill_name"],
            "progress_percentage": item.get("progress_percentage", 0.0),
            "courses": item.get("courses", []),
            "modules": item.get("modules", []),
        }
        for item in graph
    ]


def get_dashboard_skill_progress(user_id: int, limit: int = 8) -> List[Dict[str, object]]:
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    enrolled_course_titles = {
        enrollment.course.title
        for enrollment in enrollments
        if enrollment.course
    }
    snapshot = get_skill_progress_snapshot(user_id)
    filtered = []
    for item in snapshot:
        progress_value = float(item.get("progress_percentage", 0.0) or 0.0)
        belongs_to_enrolled = bool(enrolled_course_titles.intersection(item.get("courses", [])))
        if progress_value > 0 or belongs_to_enrolled:
            item["progress_percentage"] = _normalize_percentage(progress_value)
            filtered.append(item)
    filtered.sort(
        key=lambda item: (
            -float(item.get("progress_percentage", 0.0) or 0.0),
            item.get("skill_name", ""),
        )
    )
    return filtered[: max(1, min(limit, 10))]
