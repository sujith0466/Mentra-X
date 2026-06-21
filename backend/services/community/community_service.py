from __future__ import annotations

from typing import Dict, List

from backend.models import CommunityAnswer, CommunityPost, db
from backend.services.community.gamification_service import award_xp


def get_recent_posts() -> List[CommunityPost]:
    return CommunityPost.query.order_by(CommunityPost.created_at.desc(), CommunityPost.id.desc()).limit(10).all()


def create_post(user_id: int, title: str, content: str) -> CommunityPost:
    post = CommunityPost(user_id=user_id, title=title.strip(), content=content.strip())
    db.session.add(post)
    db.session.commit()
    return post


def create_answer(post_id: int, user_id: int, answer_text: str) -> CommunityAnswer:
    answer = CommunityAnswer(post_id=post_id, user_id=user_id, answer_text=answer_text.strip(), votes=0)
    db.session.add(answer)
    db.session.commit()
    award_xp(user_id, "community_answer")
    return answer


def upvote_answer(answer_id: int) -> CommunityAnswer:
    answer = CommunityAnswer.query.get_or_404(answer_id)
    answer.votes += 1
    db.session.commit()
    award_xp(answer.user_id, "community_upvote")
    return answer


def get_post_detail(post_id: int) -> Dict[str, object]:
    post = CommunityPost.query.get_or_404(post_id)
    answers = CommunityAnswer.query.filter_by(post_id=post.id).order_by(CommunityAnswer.votes.desc(), CommunityAnswer.created_at.asc()).all()
    return {
        "post": post,
        "answers": answers,
    }
