from __future__ import annotations

import re
from typing import Dict, List

from models import Syllabus, Video


def _split_text(text: str) -> List[str]:
    return [segment.strip() for segment in re.split(r"[.;:\n]+", text or "") if segment.strip()]


def _normalize_bullet(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", (text or "").strip())
    if not cleaned:
        return ""
    return cleaned[0].upper() + cleaned[1:]


def generate_notes(video_id: int) -> Dict[str, object]:
    video = Video.query.get_or_404(video_id)
    syllabus_topics = (
        Syllabus.query
        .filter_by(course_id=video.course_id)
        .order_by(Syllabus.order_number.asc(), Syllabus.id.asc())
        .limit(5)
        .all()
    )

    raw_points = _split_text(video.description or "")
    key_points = [_normalize_bullet(item) for item in raw_points[:4] if _normalize_bullet(item)]

    if not key_points:
        key_points = [
            f"Understand the main lesson goal in {video.title}.",
            "Review the example or explanation shown in the lesson.",
            "Connect this lesson to the wider course flow.",
        ]

    related_topics = [topic.topic_title for topic in syllabus_topics if topic.topic_title]
    summary = f"{video.title} focuses on the core lesson ideas and how they fit into the course progression."
    if related_topics:
        summary += f" It connects especially with topics such as {', '.join(related_topics[:3])}."

    revision_questions = [
        f"What is the main concept explained in {video.title}?",
        f"How would you apply the lesson from {video.title} in a small project or exercise?",
        "Which idea from this lesson would you revise again before taking a quiz?",
    ]
    if related_topics:
        revision_questions.append(f"How does this lesson relate to {related_topics[0]}?")

    return {
        "title": video.title,
        "key_points": key_points,
        "summary": summary,
        "revision_questions": revision_questions[:4],
    }
