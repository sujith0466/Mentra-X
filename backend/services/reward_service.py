from __future__ import annotations

from typing import List

from backend.models import ReferralTransaction


def get_referral_rewards(user_id: int) -> List[ReferralTransaction]:
    return (
        ReferralTransaction.query.filter_by(referrer_id=user_id)
        .order_by(ReferralTransaction.date.desc(), ReferralTransaction.id.desc())
        .all()
    )


def build_reward_history(referrals: List[ReferralTransaction]) -> List[dict]:
    history = []
    for ref in referrals:
        history.append({
            "name": getattr(ref.new_user, "name", "New User"),
            "email": getattr(ref.new_user, "email", ""),
            "date": ref.date,
            "reward": float(ref.reward_amount or 0.0),
        })
    return history
