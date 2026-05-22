from __future__ import annotations

import json
import os
from typing import Dict, List

from models import UserResume

PROFILE_DIR = os.path.join("uploads", "profiles")


def _ensure_profile_dir() -> None:
    os.makedirs(PROFILE_DIR, exist_ok=True)


def _profile_path(user_id: int) -> str:
    return os.path.join(PROFILE_DIR, f"user_{user_id}.json")


def load_profile(user_id: int) -> Dict[str, object]:
    """Load profile metadata without changing database schema."""
    _ensure_profile_dir()
    path = _profile_path(user_id)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as handle:
                payload = json.load(handle) or {}
            return {
                "bio": payload.get("bio", "") or "",
                "skills": payload.get("skills", []) or [],
                "learning_goals": payload.get("learning_goals", []) or [],
            }
        except (OSError, json.JSONDecodeError):
            pass

    resume_row = UserResume.query.filter_by(user_id=user_id).first()
    skills = []
    if resume_row:
        try:
            skills = json.loads(resume_row.skills_json or "[]")
        except json.JSONDecodeError:
            skills = []

    return {
        "bio": "",
        "skills": skills,
        "learning_goals": [],
    }


def save_profile(user_id: int, *, bio: str, skills: List[str], learning_goals: List[str]) -> None:
    _ensure_profile_dir()
    payload = {
        "bio": (bio or "").strip(),
        "skills": [item for item in skills if item],
        "learning_goals": [item for item in learning_goals if item],
    }
    with open(_profile_path(user_id), "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
