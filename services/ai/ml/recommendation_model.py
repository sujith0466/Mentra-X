from __future__ import annotations

from typing import Dict, List

from models import Course, Enrollment

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except Exception:  # pragma: no cover
    TfidfVectorizer = None
    cosine_similarity = None


def _course_rows() -> List[Dict[str, object]]:
    courses = Course.query.filter((Course.status == "published") | (Course.status == None)).all()
    rows = []
    for course in courses:
        domain_name = course.domain.name if course.domain else "General"
        text_blob = " ".join(
            part.strip()
            for part in [course.title or "", domain_name, course.description or ""]
            if part and str(part).strip()
        )
        rows.append(
            {
                "id": course.id,
                "title": course.title,
                "domain": domain_name,
                "description": course.description or "",
                "text_blob": text_blob,
            }
        )
    return rows


def train_recommendation_model() -> Dict[str, object]:
    rows = _course_rows()
    if not rows:
        return {"rows": rows, "similarity": []}

    if TfidfVectorizer is not None and cosine_similarity is not None:
        texts = [row["text_blob"] for row in rows]
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(texts)
        similarity = cosine_similarity(tfidf_matrix)
        return {"rows": rows, "similarity": similarity}

    identity = []
    for index in range(len(rows)):
        row_scores = [0.0] * len(rows)
        row_scores[index] = 1.0
        identity.append(row_scores)
    return {"rows": rows, "similarity": identity}


def recommend_courses_ml(user_id: int) -> Dict[str, List[Dict[str, object]]]:
    model = train_recommendation_model()
    rows = model["rows"]
    similarity = model["similarity"]

    if not rows:
        return {"recommended_courses": [], "confidence_score": []}

    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    enrolled_ids = [row.course_id for row in enrollments if row.course_id]
    completed_ids = {
        row.course_id for row in enrollments
        if row.course_id and (row.completed or (row.progress_percentage or row.progress or 0) >= 100)
    }

    if not enrolled_ids:
        fallback = rows[:6]
        results = []
        confidences = []
        for row in fallback:
            results.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "domain": row["domain"],
                    "description": row["description"],
                    "reason": "Starter recommendation based on the most accessible published courses.",
                }
            )
            confidences.append(0.55)
        return {"recommended_courses": results, "confidence_score": confidences}

    id_to_index = {int(row["id"]): index for index, row in enumerate(rows)}
    candidate_scores: Dict[int, float] = {}

    for course_id in enrolled_ids:
        if course_id not in id_to_index:
            continue
        source_index = id_to_index[course_id]
        source_scores = similarity[source_index]
        for target_index, score in enumerate(source_scores):
            target_id = int(rows[target_index]["id"])
            if target_id in enrolled_ids:
                continue
            weighted_score = float(score)
            if course_id in completed_ids:
                weighted_score *= 1.15
            candidate_scores[target_id] = max(candidate_scores.get(target_id, 0.0), weighted_score)

    ranked_ids = sorted(candidate_scores.keys(), key=lambda item: candidate_scores[item], reverse=True)
    results: List[Dict[str, object]] = []
    confidences: List[float] = []

    for target_id in ranked_ids[:6]:
        course_row = next(row for row in rows if int(row["id"]) == target_id)
        confidence = round(min(max(candidate_scores[target_id], 0.0), 0.99), 2)
        results.append(
            {
                "id": int(course_row["id"]),
                "title": course_row["title"],
                "domain": course_row["domain"],
                "description": course_row["description"],
                "reason": f"Matched by course similarity in {course_row['domain']} learning paths.",
            }
        )
        confidences.append(confidence)

    return {"recommended_courses": results, "confidence_score": confidences}
