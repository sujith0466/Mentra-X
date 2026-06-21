from __future__ import annotations

from typing import Dict, List, Optional

from backend.models import CodingChallenge, CodingSubmission, InterviewSession, ProjectIdea, SkillProgress, StudentProject
from backend.services.ai.agents.interview_agent import InterviewAgent
from backend.services.ai.agents.learning_agent import LearningAgent
from backend.services.ai.learning.study_planner_service import generate_adaptive_learning_path
from backend.services.ai.ml.learning_difficulty_model import detect_learning_difficulty
from backend.services.ai.ml.skill_prediction_model import predict_next_skills
from backend.services.ai.project_idea_service import generate_project_ideas
from backend.services.ai.recommendation_service import recommend_courses
from backend.services.ai.skills.skill_graph_service import get_skill_progress_snapshot


def _format_feed_item(label: str, title: str, detail: Optional[str] = None) -> str:
    if detail:
        return f"{label}: {title} - {detail}"
    return f"{label}: {title}"


def _build_feed_item(
    category: str,
    title: str,
    description: Optional[str] = None,
    action_label: Optional[str] = None,
    action_url: Optional[str] = None,
    tag: Optional[str] = None,
    legacy_label: Optional[str] = None,
) -> Dict[str, str]:
    description = description or ""
    action_label = action_label or "View Details"
    action_url = action_url or ""
    tag = tag or category
    label = legacy_label or category
    return {
        "category": category,
        "title": title,
        "description": description,
        "action_label": action_label,
        "action_url": action_url,
        "tag": tag,
        "text": _format_feed_item(label, title, description),
    }


def _summarize_first_sentence(text: str) -> str:
    cleaned = (text or "").strip()
    if not cleaned:
        return ""
    if "." in cleaned:
        return cleaned.split(".", 1)[0].strip() + "."
    return cleaned


def generate_learning_feed(
    user_id: int,
    *,
    difficulty_payload: Optional[dict] = None,
    skill_snapshot: Optional[list] = None,
    skill_prediction: Optional[dict] = None,
    return_structured: bool = False,
) -> List[Dict[str, str]] | List[str]:
    feed_items: List[Dict[str, str]] = []

    learning_agent_payload = LearningAgent().handle(user_id, 'Show my learning progress', intent='skill_progress')
    learning_summary = learning_agent_payload.get('response', '')
    if learning_summary:
        feed_items.append(
            _build_feed_item(
                "Learning Suggestion",
                _summarize_first_sentence(learning_summary),
                "Review the next learning focus generated from your progress.",
                "Start Revision",
                "/student/ai/revision",
                "AI Coach",
                "Learning AI suggests",
            )
        )

    interview_agent_payload = InterviewAgent().handle(user_id, 'Prepare me for backend interview', intent='interview_preparation')
    interview_summary = interview_agent_payload.get('response', '')
    if interview_summary:
        feed_items.append(
            _build_feed_item(
                "Interview Preparation Tip",
                _summarize_first_sentence(interview_summary),
                "Practice targeted questions to raise your interview readiness.",
                "Start Prep",
                "/student/interview",
                "Interview",
                "Interview AI recommends",
            )
        )

    latest_challenge = CodingChallenge.query.order_by(CodingChallenge.created_at.desc(), CodingChallenge.id.desc()).first()
    if latest_challenge:
        feed_items.append(
            _build_feed_item(
                "Learning Suggestion",
                latest_challenge.title,
                "Solve the newest coding challenge to boost your problem-solving score.",
                "Open Challenge",
                "/student/coding/challenges",
                "Coding",
                "New coding challenge available",
            )
        )

    latest_interview = InterviewSession.query.filter_by(user_id=user_id, status='completed').order_by(
        InterviewSession.end_time.desc(),
        InterviewSession.id.desc(),
    ).first()
    if latest_interview:
        feed_items.append(
            _build_feed_item(
                "Interview Preparation Tip",
                f"Mock interview completed for {latest_interview.role}",
                f"Interview score improved to {int(latest_interview.score)}%.",
                "Review Feedback",
                "/student/interview",
                "Interview",
                "Interview Update",
            )
        )
        feed_items.append(
            _build_feed_item(
                "Interview Preparation Tip",
                f"interview score improved to {int(latest_interview.score)}%",
                "Review interview notes and address weak areas.",
                "Review Feedback",
                "/student/interview",
                "Interview",
                "Interview Update",
            )
        )

    latest_project_idea = ProjectIdea.query.order_by(ProjectIdea.created_at.desc(), ProjectIdea.id.desc()).first()
    if latest_project_idea:
        feed_items.append(
            _build_feed_item(
                "Project Recommendation",
                latest_project_idea.title,
                "Build this project to strengthen your portfolio.",
                "View Idea",
                "/student/ai/project-ideas",
                "Projects",
                "Project Idea",
            )
        )

    latest_student_project = StudentProject.query.filter_by(user_id=user_id).order_by(
        StudentProject.started_at.desc(),
        StudentProject.id.desc(),
    ).first()
    if latest_student_project and latest_student_project.project_idea:
        if latest_student_project.completed_at:
            feed_items.append(
                _build_feed_item(
                    "Project Recommendation",
                    latest_student_project.project_idea.title,
                    "Great work. Publish your progress and start the next build.",
                    "View Projects",
                    "/student/projects",
                    "Projects",
                    "Project completed",
                )
            )
        elif latest_student_project.progress_percentage > 0:
            feed_items.append(
                _build_feed_item(
                    "Project Recommendation",
                    latest_student_project.project_idea.title,
                    f"{int(latest_student_project.progress_percentage)}% complete. Keep shipping updates.",
                    "Continue Project",
                    "/student/projects",
                    "Projects",
                    "Project progress updated",
                )
            )

    recommendations = recommend_courses(user_id)[:2]
    for item in recommendations:
        feed_items.append(
            _build_feed_item(
                "Learning Suggestion",
                item["title"],
                "Recommended course based on your current learning signals.",
                "View Course",
                "/student/ai/recommendations",
                "Courses",
                "Recommended Course",
            )
        )

    difficulty = difficulty_payload if difficulty_payload is not None else detect_learning_difficulty(user_id)
    for topic in difficulty.get('weak_topics', [])[:2]:
        feed_items.append(
            _build_feed_item(
                "Skill Gap Alert",
                topic,
                "Weak topic detected from quiz and assignment performance.",
                "Start Revision",
                "/student/ai/revision",
                "Skill Gap",
                "Skill Focus",
            )
        )

    adaptive_path = generate_adaptive_learning_path(user_id)
    for quiz_title in adaptive_path.get('recommended_quizzes', [])[:2]:
        feed_items.append(
            _build_feed_item(
                "Learning Suggestion",
                quiz_title,
                "Practice quiz recommended from your adaptive plan.",
                "Practice Quiz",
                "/student/ai/study-planner",
                "Practice",
                "Practice Quiz",
            )
        )

    snapshot_rows = skill_snapshot if skill_snapshot is not None else get_skill_progress_snapshot(user_id)
    snapshot_rows = [row for row in snapshot_rows if row.get('progress_percentage', 0) < 100][:2]
    for item in snapshot_rows:
        feed_items.append(
            _build_feed_item(
                "Skill Progress Update",
                item["skill_name"],
                f"{int(item['progress_percentage'])}% progress so far.",
                "View Skills",
                "/student/skills",
                "Progress",
                "Skill Progress Update",
            )
        )

    latest_submission = CodingSubmission.query.filter_by(user_id=user_id).order_by(
        CodingSubmission.submitted_at.desc(),
        CodingSubmission.id.desc(),
    ).first()
    if latest_submission and latest_submission.challenge:
        skill_row = SkillProgress.query.filter_by(
            user_id=user_id,
            skill_name=latest_submission.challenge.topic,
        ).first()
        if skill_row:
            topic_label = f"{latest_submission.challenge.topic} skill improved"
            feed_items.append(
                _build_feed_item(
                    "Skill Progress Update",
                    topic_label,
                    f"{int(skill_row.progress_percentage)}% mastery recorded.",
                    "View Challenges",
                    "/student/coding/challenges",
                    "Coding",
                    "Skill Progress Update",
                )
            )

    prediction_payload = skill_prediction if skill_prediction is not None else predict_next_skills(user_id)
    suggested_skills = prediction_payload.get('skills_to_learn_next', [])
    domain = 'AI'
    if suggested_skills and 'JavaScript' in suggested_skills[0]:
        domain = 'Web Development'
    ideas = generate_project_ideas(domain, user_id=user_id)
    if ideas:
        feed_items.append(
            _build_feed_item(
                "Project Recommendation",
                ideas[0]["title"],
                "New project idea based on your next-skill predictions.",
                "Open Project Ideas",
                "/student/ai/project-ideas",
                "Projects",
                "Project Idea",
            )
        )

    feed_items = feed_items[:10]
    if return_structured:
        return feed_items
    return [item["text"] for item in feed_items]
