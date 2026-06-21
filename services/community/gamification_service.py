from __future__ import annotations

from datetime import datetime
from typing import List

from models import UserBadge, UserXP, db


ACTION_XP = {
    "quiz_passed": 20,
    "coding_challenge_solved": 30,
    "project_completed": 100,
    "community_answer": 15,
    "community_upvote": 5,
}

LEVELS = [
    (1, 0),
    (2, 100),
    (3, 300),
    (4, 600),
]


def _level_for_xp(xp_points: int) -> int:
    level = 1
    for candidate_level, threshold in LEVELS:
        if xp_points >= threshold:
            level = candidate_level
    return level


def get_or_create_user_xp(user_id: int) -> UserXP:
    profile = UserXP.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = UserXP(user_id=user_id, xp_points=0, level=1)
        db.session.add(profile)
        db.session.commit()
    return profile


def _award_badge_if_missing(user_id: int, badge_name: str) -> None:
    existing = UserBadge.query.filter_by(user_id=user_id, badge_name=badge_name).first()
    if not existing:
        db.session.add(UserBadge(user_id=user_id, badge_name=badge_name, awarded_at=datetime.utcnow()))


def award_xp(user_id: int, action: str) -> UserXP:
    profile = get_or_create_user_xp(user_id)
    profile.xp_points += ACTION_XP.get(action, 0)
    profile.level = _level_for_xp(profile.xp_points)

    if profile.xp_points >= 30:
        _award_badge_if_missing(user_id, "Python Beginner")
    if profile.xp_points >= 100:
        _award_badge_if_missing(user_id, "AI Explorer")
    if profile.xp_points >= 200:
        _award_badge_if_missing(user_id, "Coding Master")
    if profile.xp_points >= 300:
        _award_badge_if_missing(user_id, "Interview Ready")

    db.session.commit()
    return profile


def get_user_badges(user_id: int) -> List[UserBadge]:
    return UserBadge.query.filter_by(user_id=user_id).order_by(UserBadge.awarded_at.desc(), UserBadge.id.desc()).all()

