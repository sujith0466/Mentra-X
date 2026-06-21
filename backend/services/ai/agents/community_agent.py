from __future__ import annotations

from typing import Optional

from backend.models import CommunityAnswer, CommunityPost
from backend.services.ai.agents.base_agent import BaseAgent


class CommunityAgent(BaseAgent):
    agent_name = "community"

    def handle(self, user_id: Optional[int], message: str, **kwargs):
        lowered = (message or "").lower()
        posts = CommunityPost.query.order_by(CommunityPost.created_at.desc(), CommunityPost.id.desc()).limit(3).all()
        related_posts = [
            {"id": post.id, "title": post.title}
            for post in posts
            if any(token in post.title.lower() or token in post.content.lower() for token in lowered.split()[:5])
        ] or [{"id": post.id, "title": post.title} for post in posts[:2]]

        suggestion = "The Mentra community is available at /community. You can browse questions, post your own, answer peers, and earn XP as you contribute."
        possible_answer = ""
        if "flask" in lowered and "routing" in lowered:
            possible_answer = "Check that your Flask route decorator matches the URL, the endpoint name exists in url_for, and your blueprint prefix is included."
            suggestion += " For Flask routing issues, verify the route path, blueprint name, and dynamic parameters."
        elif "error" in lowered or "bug" in lowered:
            possible_answer = "Share the exact traceback, expected behavior, and the smallest code snippet that reproduces the issue so the community can help faster."

        top_answer = CommunityAnswer.query.order_by(CommunityAnswer.votes.desc(), CommunityAnswer.created_at.asc()).first()
        data = {
            "hub_link": "/community",
            "post_link": "/community/post",
            "related_posts": related_posts,
            "suggested_answer": possible_answer,
        }
        if top_answer:
            data["top_answer_preview"] = top_answer.answer_text[:180]
        return self.build_response(
            suggestion,
            suggestions=["Show community questions", "Ask a community question", "How do I earn XP?"],
            data=data,
            intent=kwargs.get("intent", "community_help"),
        )
