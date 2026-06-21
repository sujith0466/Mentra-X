from __future__ import annotations

from typing import Dict, Optional

import json

from backend.models import UserResume
from backend.services.ai.agents import (
    CareerAgent,
    CommunityAgent,
    DebugAgent,
    InterviewAgent,
    LearningAgent,
    MentorAgent,
    ProjectAgent,
)
from backend.services.ai.coding import get_coding_challenges
from backend.services.ai.ml.learning_difficulty_model import detect_learning_difficulty
from backend.services.ai.ml.recommendation_model import recommend_courses_ml
from backend.services.ai.ml.skill_prediction_model import predict_next_skills
from backend.services.ai.career.resume_service import CAREER_SKILL_MAP


INTENT_KEYWORDS = {
    "study_help": ["study plan", "study planner", "adaptive plan", "revision", "weak topic"],
    "interview_preparation": ["prepare me for backend interview", "prepare me for interview", "start mock interview", "mock interview", "interview preparation", "backend interview", "frontend interview", "ai engineer interview", "data scientist interview"],
    "career_advice": ["career", "roadmap", "skill gap", "portfolio"],
    "coding_practice": ["give me coding practice", "show python challenges", "coding challenge", "coding challenges", "practice coding", "python challenge"],
    "coding_help": ["debug", "error", "traceback", "python error", "exception", "bug"],
    "course_recommendation": ["recommend course", "recommended course", "what should i learn next", "next course"],
    "resume_help": ["resume", "cv"],
    "project_ideas": ["project idea", "project ideas", "what can i build", "build project", "blueprint"],
    "community_help": ["show community questions", "community questions", "community help", "open community", "community answers", "discussion"],
    "skill_progress": ["skill progress", "show my learning progress", "show my skills", "knowledge map"],
    "learning_path": ["learning path", "what skills should i learn next", "adaptive learning path", "study path"],
    "platform_help": ["course navigation", "where is", "how do i use", "platform help", "dashboard help"],
}

INTENT_TO_AGENT = {
    "study_help": "learning",
    "learning_path": "learning",
    "skill_progress": "learning",
    "course_recommendation": "learning",
    "coding_help": "debug",
    "career_advice": "career",
    "resume_help": "career",
    "project_ideas": "project",
    "interview_preparation": "interview",
    "community_help": "community",
    "coding_practice": "mentor",
    "platform_help": "mentor",
    "general": "mentor",
}

AGENT_LABELS = {
    "learning": "Learning AI",
    "debug": "Debug AI",
    "career": "Career AI",
    "project": "Project AI",
    "interview": "Interview AI",
    "community": "Community AI",
    "mentor": "Mentor AI",
}

AGENTS = {
    "learning": LearningAgent(),
    "debug": DebugAgent(),
    "career": CareerAgent(),
    "project": ProjectAgent(),
    "interview": InterviewAgent(),
    "community": CommunityAgent(),
    "mentor": MentorAgent(),
}


def _detect_intent(message: str) -> str:
    lowered = (message or "").lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return intent
    return "general"


def _detect_agent_name(message: str) -> str:
    return INTENT_TO_AGENT.get(_detect_intent(message), "mentor")


def get_available_agents() -> list[Dict[str, str]]:
    return [
        {
            "key": "learning",
            "label": AGENT_LABELS["learning"],
            "description": "Study plans, learning paths, skill graph progress, and feed recommendations.",
            "example_question": "Show my learning progress",
            "link": "/student/ai/study-planner",
        },
        {
            "key": "debug",
            "label": AGENT_LABELS["debug"],
            "description": "Coding errors, stack traces, exception explanations, and debugging hints.",
            "example_question": "Why am I getting IndexError?",
            "link": "/student/devtools/debug",
        },
        {
            "key": "career",
            "label": AGENT_LABELS["career"],
            "description": "Resume analysis, career roadmaps, portfolio growth, and skill gaps.",
            "example_question": "Help me improve my resume",
            "link": "/student/career/resume-analyzer",
        },
        {
            "key": "project",
            "label": AGENT_LABELS["project"],
            "description": "Project ideas, blueprints, and project progress guidance.",
            "example_question": "Give me project ideas for AI",
            "link": "/student/projects",
        },
        {
            "key": "interview",
            "label": AGENT_LABELS["interview"],
            "description": "Mock interviews, role-based preparation, and interview feedback.",
            "example_question": "Start mock interview",
            "link": "/student/interview",
        },
        {
            "key": "community",
            "label": AGENT_LABELS["community"],
            "description": "Community question suggestions, answer ideas, and related discussion threads.",
            "example_question": "Show community questions",
            "link": "/community",
        },
    ]


def _append_suggestions_block(answer: str, suggestions: list[str]) -> str:
    if not suggestions:
        return answer
    return answer + "\n\nNext Actions\n" + "\n".join(f"- {item}" for item in suggestions[:3])


def _summarize_first_sentence(text: str) -> str:
    cleaned = (text or "").strip()
    if not cleaned:
        return ""
    if "." in cleaned:
        return cleaned.split(".", 1)[0].strip() + "."
    return cleaned


def _ensure_structured_answer(intent: str, answer: str, suggestions: list[str], data: Dict[str, object]) -> str:
    lines = [line for line in (answer or "").splitlines() if line.strip()]
    if len(lines) > 2:
        return answer
    summary = _summarize_first_sentence(answer) or "Here is a focused next step tailored to you."
    focus = "Skill Growth"
    if intent in {"coding_help", "coding_practice"}:
        focus = "Coding Practice"
    elif intent in {"interview_preparation"}:
        focus = "Interview Readiness"
    elif intent in {"career_advice", "resume_help"}:
        focus = "Career Growth"
    elif intent in {"project_ideas"}:
        focus = "Project Building"
    elif intent in {"learning_path", "study_help", "skill_progress"}:
        focus = "Learning Path"

    structured_lines = [
        "Recommended Practice",
        f"Focus: {focus}",
        f"Summary: {summary}",
    ]
    if suggestions:
        structured_lines.append(f"Next Action: {suggestions[0]}")
    if data.get("recommendation") and isinstance(data["recommendation"], dict):
        courses = data["recommendation"].get("recommended_courses") or []
        if courses:
            structured_lines.append(f"Suggested Course: {courses[0].get('title', 'Recommended course')}")
    return "\n".join(structured_lines)


def _resume_insights_for_user(user_id: Optional[int]) -> Optional[Dict[str, list]]:
    if not user_id:
        return None
    row = UserResume.query.filter_by(user_id=user_id).first()
    if not row:
        return None
    skills = json.loads(row.skills_json or "[]")
    career_scores = []
    for career, required_skills in CAREER_SKILL_MAP.items():
        score = sum(1 for skill in required_skills if skill in skills)
        if score > 0:
            career_scores.append((career, score))
    career_scores.sort(key=lambda item: item[1], reverse=True)
    primary_career = career_scores[0][0] if career_scores else "Full Stack Developer"
    missing = [skill for skill in CAREER_SKILL_MAP[primary_career] if skill not in skills]
    return {
        "detected_skills": skills,
        "recommended_skills": missing,
        "primary_career": primary_career,
    }


def _mentor_special_cases(user_id: Optional[int], message: str, intent: str) -> Optional[Dict[str, object]]:
    if intent == "coding_practice":
        challenges = get_coding_challenges()
        featured = challenges[0] if challenges else None
        answer_lines = [
            "Recommended Practice",
            "",
            f"Topic: {featured.topic if featured else 'Python Practice'}",
            f"Challenge: {featured.title if featured else 'Starter Challenge'}",
            f"Skills Improved: {featured.topic if featured else 'Problem Solving'}, Test-Driven Thinking",
            f"Difficulty: {featured.difficulty if featured else 'Beginner'}",
            "",
            "Open /student/coding/challenges to start practicing inside Mentra.",
        ]
        return {
            "agent": "mentor",
            "response": "\n".join(answer_lines),
            "suggestions": ["Show Python challenges", "Open coding challenge results", "How do I improve my solution?"],
            "data": {
                "challenge_links": [f"/student/coding/challenge/{item.id}" for item in challenges[:5]],
                "hub_link": "/student/coding/challenges",
            },
            "intent": intent,
        }

    return None


def _format_enhanced_answer(intent: str, payload: Dict[str, object], answer: str, suggestions: list[str]) -> str:
    data = payload.get("data") or {}
    if intent == "course_recommendation":
        course_lines = [item.get("title", "") for item in data.get("recommended_courses", [])[:3] if item.get("title")]
        if course_lines:
            answer = "Recommended Next Step\n\nCourses\n" + "\n".join(f"- {item}" for item in course_lines)
    elif intent == "project_ideas":
        idea_lines = [item.get("title", "") for item in data.get("ideas", [])[:3] if item.get("title")]
        if idea_lines:
            answer = "Suggested Project Ideas\n\nProjects\n" + "\n".join(f"- {item}" for item in idea_lines)
            answer += "\n\nOpen /student/projects to track and build your ideas."
    elif intent == "interview_preparation":
        answer = "Interview Preparation Plan\n\n" + answer
    return _append_suggestions_block(answer, suggestions)


def mentor_assistant(
    user_id: Optional[int],
    message: str,
    *,
    current_page: Optional[str] = None,
    domain: Optional[str] = None,
    course_name: Optional[str] = None,
) -> Dict[str, object]:
    intent = _detect_intent(message)
    agent_name = INTENT_TO_AGENT.get(intent, "mentor")

    special_case = _mentor_special_cases(user_id, message, intent)
    if special_case:
        payload = special_case
    else:
        agent = AGENTS.get(agent_name, AGENTS["mentor"])
        payload = agent.handle(
            user_id,
            message,
            intent=intent,
            current_page=current_page,
            domain=domain,
            course_name=course_name,
        )

    answer = str(payload.get("response", ""))
    suggestions = list(payload.get("suggestions") or [])
    data = payload.get("data") or {}

    if user_id and agent_name == "mentor":
        skill_prediction = predict_next_skills(user_id) or {}
        difficulty = detect_learning_difficulty(user_id) or {}
        recommendation = recommend_courses_ml(user_id) or {}
        if skill_prediction.get("skills_to_learn_next"):
            answer += "\n\nSuggested Skills\n" + "\n".join(f"- {item}" for item in skill_prediction.get("skills_to_learn_next", [])[:3])
        if difficulty.get("weak_topics"):
            answer += "\n\nPractice Focus\n" + "\n".join(f"- {item}" for item in difficulty["weak_topics"][:2])
        if recommendation.get("recommended_courses"):
            answer += "\n\nRecommended Course\n- " + recommendation["recommended_courses"][0]["title"]
        data = {
            **data,
            "skill_prediction": skill_prediction,
            "difficulty": difficulty,
            "recommendation": recommendation,
        }

    answer = _format_enhanced_answer(intent, {**payload, "data": data}, answer, suggestions)
    answer = _ensure_structured_answer(intent, answer, suggestions, data)

    resume_insights = _resume_insights_for_user(user_id)
    if resume_insights:
        needs_resume = intent in {"resume_help", "career_advice"} or (
            "missing" in (message or "").lower() and "skill" in (message or "").lower()
        )
        if needs_resume:
            detected = resume_insights.get("detected_skills", [])[:6]
            recommended = resume_insights.get("recommended_skills", [])[:6]
            answer += "\n\nResume Insights"
            if detected:
                answer += "\nDetected Skills\n" + "\n".join(f"- {item}" for item in detected)
            if recommended:
                answer += "\nRecommended Skills\n" + "\n".join(f"- {item}" for item in recommended)
            data = {**data, "resume_insights": resume_insights}

    result = {
        "agent": payload.get("agent", agent_name),
        "response": answer,
        "suggestions": suggestions,
        "intent": payload.get("intent", intent),
        "data": data,
        "answer": answer,
        "options": suggestions,
    }
    result["agent_label"] = AGENT_LABELS.get(result["agent"], "Mentor AI")
    return result
