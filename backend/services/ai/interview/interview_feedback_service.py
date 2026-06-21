from __future__ import annotations

from typing import Dict, List


def _extract_expected_points(expected_answer: str) -> List[str]:
    if not expected_answer:
        return []
    return [item.strip() for item in expected_answer.split(",") if item.strip()]


def analyze_interview_answer(question: str, answer: str, expected_answer: str = "") -> Dict[str, object]:
    answer_text = (answer or "").strip()
    expected_points = _extract_expected_points(expected_answer)
    lowered_answer = answer_text.lower()

    if not answer_text:
        return {
            "feedback": f"No answer provided for: {question}",
            "score": 0,
            "concept_completeness": "Low",
            "missing_points": expected_points[:3],
            "suggestions": ["Answer in complete sentences and cover the core concept directly."],
        }

    matched_points = []
    missing_points = []
    for point in expected_points:
        point_words = [word for word in point.lower().split() if len(word) > 2]
        if point_words and any(word in lowered_answer for word in point_words):
            matched_points.append(point)
        else:
            missing_points.append(point)

    if expected_points:
        completeness_ratio = len(matched_points) / len(expected_points)
        score = round(completeness_ratio * 100, 2)
    else:
        score = 75.0 if len(answer_text.split()) >= 12 else 55.0

    if score >= 80:
        completeness = "High"
    elif score >= 50:
        completeness = "Medium"
    else:
        completeness = "Low"

    feedback = "Your answer covered the question reasonably well."
    if matched_points:
        feedback = "You addressed " + ", ".join(matched_points[:3]) + "."
    if missing_points:
        feedback += " You missed " + ", ".join(missing_points[:3]) + "."

    suggestions = []
    if missing_points:
        suggestions.append("Add the missing core points explicitly in your answer.")
    if "example" not in lowered_answer:
        suggestions.append("Include a brief real-world example to strengthen your explanation.")
    if len(answer_text.split()) < 12:
        suggestions.append("Expand your answer with a clearer explanation of why the concept matters.")

    return {
        "feedback": feedback,
        "score": score,
        "concept_completeness": completeness,
        "missing_points": missing_points[:4],
        "suggestions": suggestions[:3],
    }

