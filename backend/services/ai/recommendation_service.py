from __future__ import annotations

from collections import Counter
from typing import Dict, List

import json

from backend.models import Course, Enrollment, UserResume
from backend.services.ai.career.resume_service import CAREER_SKILL_MAP
from backend.services.ai.career.skill_gap_service import detect_skill_gap
from backend.services.ai.ml.recommendation_model import recommend_courses_ml


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


def _infer_primary_career(resume_skills: List[str]) -> str:
    if not resume_skills:
        return "Full Stack Developer"
    career_scores = []
    for career, required_skills in CAREER_SKILL_MAP.items():
        score = sum(1 for skill in required_skills if skill in resume_skills)
        if score > 0:
            career_scores.append((career, score))
    career_scores.sort(key=lambda item: item[1], reverse=True)
    return career_scores[0][0] if career_scores else "Full Stack Developer"


def _gap_based_recommendations(user_id: int) -> List[Dict[str, object]]:
    resume_row = UserResume.query.filter_by(user_id=user_id).first()
    if not resume_row:
        return []
    resume_skills = json.loads(resume_row.skills_json or "[]")
    if not resume_skills:
        return []

    career_goal = _infer_primary_career(resume_skills)
    gap_report = detect_skill_gap(user_id, career_goal)
    missing_skills = gap_report.get("skills_missing", [])
    suggested_skills = gap_report.get("suggested_skills", [])

    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    completed_course_ids = {
        row.course_id for row in enrollments
        if row.completed or (row.progress_percentage or row.progress or 0) >= 100
    }
    enrolled_course_ids = {row.course_id for row in enrollments}

    courses = Course.query.filter(Course.status == "published").all()
    scored: List[tuple[int, Course, List[str], List[str]]] = []

    for course in courses:
        if course.id in completed_course_ids or course.id in enrolled_course_ids:
            continue
        course_text = f"{course.title or ''} {course.description or ''}".lower()
        matched_missing = [skill for skill in missing_skills if skill.lower() in course_text]
        matched_suggested = [skill for skill in suggested_skills if skill.lower() in course_text]
        score = (len(matched_missing) * 3) + len(matched_suggested)
        if score > 0:
            scored.append((score, course, matched_missing, matched_suggested))

    scored.sort(key=lambda item: (item[0], item[1].created_at), reverse=True)
    recommendations: List[Dict[str, object]] = []

    for score, course, matched_missing, matched_suggested in scored[:6]:
        if matched_missing:
            reason = f"Targets missing skills: {', '.join(matched_missing[:3])}."
        elif matched_suggested:
            reason = f"Supports skills you are building: {', '.join(matched_suggested[:3])}."
        else:
            reason = "Matches your current skill gap priorities."
        recommendations.append(_course_payload(course, reason, min(0.9, 0.55 + (score * 0.05))))

    return recommendations


def recommend_courses(user_id: int) -> List[Dict[str, object]]:
    gap_recommendations = _gap_based_recommendations(user_id)
    if gap_recommendations:
        return gap_recommendations

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
