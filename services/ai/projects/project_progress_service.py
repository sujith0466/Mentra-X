from __future__ import annotations

import json
from datetime import datetime
from typing import Dict, List

from models import ProjectIdea, ProjectTask, SkillProgress, StudentProject, db
from services.community.gamification_service import award_xp


DEFAULT_TASKS = [
    ("Setup project environment", "Initialize the repository, dependencies, and configuration."),
    ("Create database models", "Design the schema and create the initial models."),
    ("Implement backend API", "Build the core routes and service logic."),
    ("Build frontend interface", "Create the user-facing screens and interactions."),
    ("Test application", "Validate the project with manual and automated tests."),
]


def generate_project_tasks(student_project_id: int) -> List[ProjectTask]:
    tasks = []
    for index, (title, description) in enumerate(DEFAULT_TASKS, start=1):
        task = ProjectTask(
            project_id=student_project_id,
            task_title=title,
            task_description=description,
            task_order=index,
            completed=False,
        )
        db.session.add(task)
        tasks.append(task)
    db.session.commit()
    return tasks


def start_student_project(user_id: int, project_id: int) -> StudentProject:
    student_project = StudentProject.query.filter_by(user_id=user_id, project_id=project_id).first()
    if student_project:
        return student_project

    student_project = StudentProject(
        user_id=user_id,
        project_id=project_id,
        progress_percentage=0.0,
        started_at=datetime.utcnow(),
    )
    db.session.add(student_project)
    db.session.flush()
    generate_project_tasks(student_project.id)
    db.session.commit()
    return student_project


def update_student_project_progress(student_project_id: int, completed_task_ids: List[int]) -> StudentProject:
    student_project = StudentProject.query.get_or_404(student_project_id)
    task_id_set = {int(value) for value in completed_task_ids}
    tasks = ProjectTask.query.filter_by(project_id=student_project.id).order_by(ProjectTask.task_order.asc()).all()
    for task in tasks:
        task.completed = task.id in task_id_set

    total_tasks = len(tasks)
    completed_count = sum(1 for task in tasks if task.completed)
    student_project.progress_percentage = round((completed_count / total_tasks) * 100, 2) if total_tasks else 0.0

    if student_project.progress_percentage >= 100 and student_project.completed_at is None:
        student_project.completed_at = datetime.utcnow()
        award_xp(student_project.user_id, "project_completed")
        for skill_name in ["Project Delivery", student_project.project_idea.domain]:
            row = SkillProgress.query.filter_by(user_id=student_project.user_id, skill_name=skill_name).first()
            if not row:
                row = SkillProgress(user_id=student_project.user_id, skill_name=skill_name, progress_percentage=0.0)
                db.session.add(row)
            row.progress_percentage = min(100.0, max(float(row.progress_percentage or 0.0), 100.0))
            row.last_updated = datetime.utcnow()

    db.session.commit()
    return student_project


def get_student_project_detail(student_project_id: int) -> Dict[str, object]:
    student_project = StudentProject.query.get_or_404(student_project_id)
    project = student_project.project_idea
    architecture = {}
    try:
        architecture = json.loads(project.architecture or "{}")
    except (TypeError, ValueError, json.JSONDecodeError):
        architecture = {}

    tasks = ProjectTask.query.filter_by(project_id=student_project.id).order_by(ProjectTask.task_order.asc()).all()
    return {
        "student_project": student_project,
        "project": project,
        "tasks": tasks,
        "blueprint": architecture,
    }


def get_recent_student_projects(user_id: int) -> List[StudentProject]:
    return (
        StudentProject.query
        .filter_by(user_id=user_id)
        .order_by(StudentProject.started_at.desc(), StudentProject.id.desc())
        .limit(6)
        .all()
    )

