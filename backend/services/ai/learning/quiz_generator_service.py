from __future__ import annotations

import re
from typing import Dict, List

from backend.models import Syllabus, Video


def _extract_phrases(video: Video) -> List[str]:
    text = " ".join(
        [
            video.title or "",
            video.description or "",
            " ".join(topic.topic_title for topic in Syllabus.query.filter_by(course_id=video.course_id).order_by(Syllabus.order_number.asc()).limit(4).all()),
        ]
    )
    return [item.strip() for item in re.split(r"[.;:\n,]+", text) if item.strip()]


def _build_options(correct: str) -> List[str]:
    distractors = [
        "Ignore the main concept and skip practice",
        "Memorize labels without understanding the topic",
        "Avoid reviewing the lesson after watching",
        "Focus only on unrelated tools and examples",
    ]
    options = [correct]
    for item in distractors:
        if item != correct and len(options) < 4:
            options.append(item)
    return options[:4]


def generate_quiz_from_lesson(video_id: int) -> List[Dict[str, object]]:
    video = Video.query.get_or_404(video_id)
    phrases = _extract_phrases(video)
    seed_phrase = phrases[0] if phrases else video.title
    syllabus_titles = [
        topic.topic_title
        for topic in Syllabus.query.filter_by(course_id=video.course_id).order_by(Syllabus.order_number.asc()).limit(3).all()
    ]
    supporting_topic = syllabus_titles[0] if syllabus_titles else "the course topic"

    return [
        {
            "question": f"What is the primary focus of the lesson '{video.title}'?",
            "options": _build_options(f"Understand {seed_phrase.lower()} in a practical way"),
            "correct_answer": f"Understand {seed_phrase.lower()} in a practical way",
        },
        {
            "question": f"Which action best reinforces the concepts from {video.title}?",
            "options": _build_options("Review the lesson and apply it in a small exercise"),
            "correct_answer": "Review the lesson and apply it in a small exercise",
        },
        {
            "question": f"How does this lesson connect to {supporting_topic}?",
            "options": _build_options("It supports broader course understanding and later assessments"),
            "correct_answer": "It supports broader course understanding and later assessments",
        },
        {
            "question": "What should a student do after finishing this lesson?",
            "options": _build_options("Revise the key points and attempt practice questions"),
            "correct_answer": "Revise the key points and attempt practice questions",
        },
    ]
