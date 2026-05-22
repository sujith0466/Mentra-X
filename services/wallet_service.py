from __future__ import annotations

from models import User


def get_wallet_balance(user_id: int) -> float:
    user = User.query.get(user_id)
    if not user:
        return 0.0
    return float(user.wallet_balance or 0.0)
