"""
Multi-Agent Orchestrator for Mentra AI Platform.

Central routing layer that detects user intent from natural language input
and dispatches to the appropriate specialized agent. All AI interactions
should flow through `route_to_agent()` for consistent behaviour, logging,
and future extensibility.
"""
from __future__ import annotations

from typing import Dict, Optional

from backend.services.ai.agents import (
    CareerAgent,
    CommunityAgent,
    DebugAgent,
    InterviewAgent,
    LearningAgent,
    MentorAgent,
    ProjectAgent,
)

# ---------------------------------------------------------------------------
# Intent keyword map — order matters (first match wins)
# ---------------------------------------------------------------------------
INTENT_KEYWORDS: Dict[str, list[str]] = {
    # Debug / coding errors
    "debug": [
        "error", "bug", "fix", "traceback", "typeerror", "valueerror",
        "syntaxerror", "indexerror", "keyerror", "exception", "debug",
        "stack trace", "runtime error", "crash",
    ],
    # Learning / courses
    "learning": [
        "learn", "course", "study plan", "study planner", "revision",
        "weak topic", "adaptive plan", "learning path", "skill progress",
        "what should i learn", "recommend course", "next course",
    ],
    # Career / resume / jobs
    "career": [
        "career", "job", "resume", "cv", "roadmap", "skill gap",
        "portfolio", "placement", "hire", "interview preparation",
        "mock interview", "salary",
    ],
    # Projects
    "project": [
        "project", "idea", "blueprint", "build", "what can i build",
        "project ideas", "capstone",
    ],
    # Community
    "community": [
        "community", "discussion", "forum", "question thread",
    ],
}

# Agent name → singleton instance
AGENTS: Dict[str, object] = {
    "mentor":    MentorAgent(),
    "learning":  LearningAgent(),
    "career":    CareerAgent(),
    "debug":     DebugAgent(),
    "project":   ProjectAgent(),
    "interview": InterviewAgent(),
    "community": CommunityAgent(),
}

AGENT_LABELS: Dict[str, str] = {
    "mentor":    "Mentor AI",
    "learning":  "Learning AI",
    "career":    "Career AI",
    "debug":     "Debug AI",
    "project":   "Project AI",
    "interview": "Interview AI",
    "community": "Community AI",
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def detect_intent(user_input: str) -> str:
    """Return an intent key based on keyword matching against *user_input*.

    Returns one of: ``debug``, ``learning``, ``career``, ``project``,
    ``community``, or ``mentor`` (the default fallback).
    """
    lowered = (user_input or "").lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in lowered for kw in keywords):
            return intent
    return "mentor"


def route_to_agent(
    user_input: str,
    *,
    user_id: Optional[int] = None,
    current_page: Optional[str] = None,
    domain: Optional[str] = None,
    course_name: Optional[str] = None,
) -> Dict[str, object]:
    """Detect intent, dispatch to the matching agent, and return a
    structured response dict.

    The returned dict always contains::

        {
            "agent": str,           # agent key
            "agent_label": str,     # human-readable label
            "intent": str,          # detected intent
            "response": str,        # answer text
            "suggestions": list,    # follow-up suggestions
            "data": dict,           # any structured payload
        }
    """
    intent = detect_intent(user_input)
    agent = AGENTS.get(intent, AGENTS["mentor"])

    contextual_guidance: Dict[str, object] = {}
    lowered_input = (user_input or "").lower()
    if user_id and any(keyword in lowered_input for keyword in ["improve", "weak", "next step", "how can i improve"]):
        try:
            from services.career.job_score import calculate_score
            from services.learning.path_generator import generate_learning_path
            from services.learning.weekly_report import generate_weekly_report

            score_data = calculate_score(user_id)
            learning_path = generate_learning_path(user_id)
            weekly_report = generate_weekly_report(user_id)

            contextual_guidance = {
                "job_score": score_data,
                "learning_path": {
                    "priority": learning_path.get("priority"),
                    "reason": learning_path.get("reason"),
                    "next_courses": learning_path.get("next_courses", []),
                    "next_action": learning_path.get("next_action"),
                },
                "weekly_report": {
                    "weak_topics": weekly_report.get("weak_topics", []),
                    "strong_topics": weekly_report.get("strong_topics", []),
                    "recommendations": weekly_report.get("recommendations", []),
                    "next_action": weekly_report.get("next_action"),
                },
            }
        except Exception as exc:
            print(f"[Orchestrator] contextual guidance unavailable: {exc}")

    # --- Fallback safety: if the selected agent crashes, fall back to mentor ---
    try:
        payload = agent.handle(
            user_id,
            user_input,
            intent=intent,
            current_page=current_page,
            domain=domain,
            course_name=course_name,
        )
    except Exception as exc:
        print(f"[Orchestrator] Agent '{intent}' failed: {exc}. Falling back to mentor.")
        try:
            payload = AGENTS["mentor"].handle(
                user_id,
                user_input,
                intent="general",
                current_page=current_page,
                domain=domain,
                course_name=course_name,
            )
        except Exception:
            # Ultimate fallback — never crash
            payload = {
                "agent": "mentor",
                "response": "I'm here to help! Could you rephrase your question?",
                "suggestions": ["Show my courses", "Open study planner", "Help me debug"],
                "data": {},
                "intent": "general",
            }

    agent_key = payload.get("agent", intent)

    # --- MongoDB logging for analytics & future AI training ---
    _log_orchestrator_event(user_id, user_input, intent, agent_key)

    # Normalise the payload shape
    payload_data = payload.get("data", {}) or {}
    if contextual_guidance:
        payload_data = {**payload_data, "contextual_guidance": contextual_guidance}
        if not payload.get("response"):
            payload["response"] = "Based on your performance, focus on your weakest topics and complete the next recommended course."
        if not payload.get("suggestions"):
            payload["suggestions"] = [
                contextual_guidance.get("learning_path", {}).get("next_action", "Open your learning path"),
                "Review weak topics from weekly report",
                "Practice coding to improve job-readiness score",
            ]

    next_action = contextual_guidance.get("learning_path", {}).get("next_action") if contextual_guidance else None
    priority = contextual_guidance.get("learning_path", {}).get("priority") if contextual_guidance else "medium"

    return {
        "agent":        agent_key,
        "agent_label":  AGENT_LABELS.get(agent_key, "Mentor AI"),
        "intent":       payload.get("intent", intent),
        "response":     payload.get("response", ""),
        "answer":       payload.get("response", ""),       # compat alias
        "suggestions":  payload.get("suggestions", []),
        "options":      payload.get("suggestions", []),    # compat alias
        "data":         payload_data,
        "next_action":  next_action,
        "priority":     priority or "medium",
    }


def get_available_agents() -> list[Dict[str, str]]:
    """Return metadata about all registered agents for UI display."""
    return [
        {
            "key": key,
            "label": AGENT_LABELS.get(key, key.title()),
            "description": _AGENT_DESCRIPTIONS.get(key, ""),
        }
        for key in ["mentor", "learning", "debug", "career", "project", "interview", "community"]
        if key in AGENTS
    ]


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

_AGENT_DESCRIPTIONS: Dict[str, str] = {
    "mentor":    "General learning guidance, concept explanations, and platform help.",
    "learning":  "Adaptive study plans, learning paths, skill graph progress, and course recommendations.",
    "debug":     "Error analysis, stack trace explanations, and debugging suggestions.",
    "career":    "Resume analysis, career roadmaps, portfolio growth, and skill gap detection.",
    "project":   "Project ideas, blueprints, and guided project building.",
    "interview": "Mock interviews, role-based preparation, and interview feedback.",
    "community": "Community Q&A suggestions, answer hints, and discussion thread help.",
}


def _log_orchestrator_event(
    user_id: Optional[int],
    user_input: str,
    intent: str,
    agent_key: str,
) -> None:
    """Log every orchestrator invocation to MongoDB for analytics.

    Silently swallows errors so logging never disrupts the user flow.
    """
    try:
        from services.mongo_service import safe_insert
        safe_insert("orchestrator_logs", {
            "user_id": user_id,
            "input": (user_input or "")[:500],   # cap length
            "intent": intent,
            "agent": agent_key,
        })
    except Exception:
        # Logging must never break the orchestrator
        pass
