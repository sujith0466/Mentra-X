from __future__ import annotations

from collections import Counter
from typing import Dict, List

from models import Course, Enrollment
from services.ai.ml.recommendation_model import recommend_courses_ml


def _course_payload(course: Course, reason: str, confidence: float | None = None) -> Dict[str, object]:
    payload = {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "domain": course.domain.name if course.domain else "General",
        "instructor": course.instructor,
        "price": course.price,
        "reason": reason,
    }
    if confidence is not None:
        payload["confidence"] = confidence
    return payload


def _fallback_recommendations(user_id: int) -> List[Dict[str, object]]:
    enrollments = (
        Enrollment.query
        .filter_by(user_id=user_id)
        .join(Course, Enrollment.course_id == Course.id)
        .all()
    )

    enrolled_course_ids = {enrollment.course_id for enrollment in enrollments}
    completed_domain_ids = []
    active_domain_ids = []

    for enrollment in enrollments:
        if not enrollment.course:
            continue
        if enrollment.completed or (enrollment.progress_percentage or enrollment.progress or 0) >= 100:
            completed_domain_ids.append(enrollment.course.domain_id)
        else:
            active_domain_ids.append(enrollment.course.domain_id)

    priority_domains = []
    if active_domain_ids:
        priority_domains.extend(domain_id for domain_id, _ in Counter(active_domain_ids).most_common())
    if completed_domain_ids:
        priority_domains.extend(domain_id for domain_id, _ in Counter(completed_domain_ids).most_common())

    recommendations: List[Dict[str, object]] = []
    seen_course_ids = set()

    for domain_id in priority_domains:
        domain_query = Course.query.filter(
            Course.domain_id == domain_id,
            Course.status == "published",
        )
        if enrolled_course_ids:
            domain_query = domain_query.filter(~Course.id.in_(enrolled_course_ids))
        domain_courses = domain_query.order_by(Course.created_at.desc()).limit(4).all()
        for course in domain_courses:
            if course.id in seen_course_ids:
                continue
            seen_course_ids.add(course.id)
            reason = "Build deeper skill in your current learning domain."
            recommendations.append(_course_payload(course, reason, 0.68))

    if len(recommendations) < 6:
        fallback_query = Course.query.filter(Course.status == "published")
        if enrolled_course_ids:
            fallback_query = fallback_query.filter(~Course.id.in_(enrolled_course_ids))
        fallback_courses = fallback_query.order_by(Course.created_at.desc()).limit(12).all()
        for course in fallback_courses:
            if course.id in seen_course_ids:
                continue
            seen_course_ids.add(course.id)
            recommendations.append(_course_payload(course, "Popular next-step course from the public catalog.", 0.55))
            if len(recommendations) >= 6:
                break

    return recommendations


def recommend_courses(user_id: int) -> List[Dict[str, object]]:
    try:
        ml_payload = recommend_courses_ml(user_id)
        recommended_courses = ml_payload.get("recommended_courses", [])
        confidence_scores = ml_payload.get("confidence_score", [])
        if recommended_courses:
            results = []
            for index, item in enumerate(recommended_courses):
                course = Course.query.get(item["id"])
                if not course:
                    continue
                confidence = confidence_scores[index] if index < len(confidence_scores) else None
                reason = item.get("reason") or "Recommended by personalized learning similarity."
                if confidence is not None:
                    reason = f"{reason} Confidence: {int(confidence * 100)}%."
                results.append(_course_payload(course, reason, confidence))
            if results:
                return results
    except Exception as error:
        print(f"ML recommendation fallback triggered: {error}")

    return _fallback_recommendations(user_id)
