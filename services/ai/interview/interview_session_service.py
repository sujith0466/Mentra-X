from __future__ import annotations

from datetime import datetime
from typing import Dict, List

import json

from models import (
    InterviewQuestion,
    InterviewResponse,
    InterviewSession,
    SkillProgress,
    UserResume,
    db,
)
from services.ai.interview.interview_feedback_service import analyze_interview_answer
from services.ai.interview.interview_question_service import generate_interview_questions


ROLE_SKILL_MAP = {
    "Backend Developer": ["Backend Architecture", "APIs", "Databases"],
    "Frontend Developer": ["Frontend Development", "UI Engineering", "Accessibility"],
    "AI Engineer": ["Machine Learning", "Model Evaluation", "Algorithms"],
    "Data Scientist": ["Data Analysis", "Statistics", "Machine Learning"],
    "Full Stack Developer": ["Full Stack Development", "Backend Architecture", "Frontend Development"],
}


def _upsert_skill_progress(user_id: int, skill_name: str, score: float) -> None:
    row = SkillProgress.query.filter_by(user_id=user_id, skill_name=skill_name).first()
    if not row:
        row = SkillProgress(user_id=user_id, skill_name=skill_name, progress_percentage=0.0)
        db.session.add(row)
    row.progress_percentage = min(100.0, round(max(float(row.progress_percentage or 0.0), float(score or 0.0)), 2))
    row.last_updated = datetime.utcnow()


def start_interview(user_id: int, role: str, difficulty: str) -> InterviewSession:
    session = InterviewSession(
        user_id=user_id,
        role=role,
        difficulty=difficulty,
        start_time=datetime.utcnow(),
        status="in_progress",
        score=0.0,
    )
    db.session.add(session)
    db.session.flush()

    resume_skills = []
    resume_row = UserResume.query.filter_by(user_id=user_id).first()
    if resume_row:
        resume_skills = json.loads(resume_row.skills_json or "[]")

    for payload in generate_interview_questions(role, difficulty, resume_skills=resume_skills):
        db.session.add(
            InterviewQuestion(
                session_id=session.id,
                question_text=payload["question_text"],
                question_type=payload["question_type"],
                expected_answer=payload.get("expected_answer", ""),
                difficulty=payload.get("difficulty", difficulty),
            )
        )

    db.session.commit()
    return session


def submit_interview_answers(session_id: int, answers_by_question: Dict[int, str]) -> Dict[str, object]:
    session = InterviewSession.query.get_or_404(session_id)
    questions = InterviewQuestion.query.filter_by(session_id=session.id).order_by(InterviewQuestion.id.asc()).all()
    response_rows: List[InterviewResponse] = []

    for question in questions:
        submitted_answer = (answers_by_question.get(question.id) or "").strip()
        analysis = analyze_interview_answer(
            question.question_text,
            submitted_answer,
            question.expected_answer or "",
        )
        response = InterviewResponse.query.filter_by(session_id=session.id, question_id=question.id).first()
        if not response:
            response = InterviewResponse(session_id=session.id, question_id=question.id)
            db.session.add(response)
        response.user_answer = submitted_answer
        response.ai_feedback = analysis["feedback"]
        response.score = float(analysis["score"])
        response_rows.append(response)

    db.session.commit()
    final_session = end_interview(session.id)
    return get_session_detail(final_session.id)


def end_interview(session_id: int) -> InterviewSession:
    session = InterviewSession.query.get_or_404(session_id)
    responses = InterviewResponse.query.filter_by(session_id=session.id).all()
    average_score = round(sum(float(item.score or 0.0) for item in responses) / len(responses), 2) if responses else 0.0
    session.score = average_score
    session.status = "completed"
    session.end_time = datetime.utcnow()

    for skill_name in ROLE_SKILL_MAP.get(session.role, []):
        _upsert_skill_progress(session.user_id, skill_name, average_score)

    if any(question.question_type == "coding" for question in session.questions):
        _upsert_skill_progress(session.user_id, "Algorithms", average_score)

    db.session.commit()
    return session


def get_session_detail(session_id: int) -> Dict[str, object]:
    session = InterviewSession.query.get_or_404(session_id)
    questions = InterviewQuestion.query.filter_by(session_id=session.id).order_by(InterviewQuestion.id.asc()).all()
    responses = {
        row.question_id: row for row in InterviewResponse.query.filter_by(session_id=session.id).all()
    }
    return {
        "session": session,
        "questions": questions,
        "responses": responses,
    }


def get_recent_interview_sessions(user_id: int) -> List[InterviewSession]:
    return (
        InterviewSession.query
        .filter_by(user_id=user_id)
        .order_by(InterviewSession.start_time.desc(), InterviewSession.id.desc())
        .limit(5)
        .all()
    )
