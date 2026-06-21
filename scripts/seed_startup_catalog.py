from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app
from models import Assignment, Course, CourseModule, Domain, Quiz, Syllabus, Video, db
from scripts.seed_courses_phase7 import seed_catalog


def _normalize(value: str) -> str:
    return " ".join((value or "").strip().split()).lower()


def _looks_like_noise(value: str) -> bool:
    text = _normalize(value)
    if not text:
        return True
    prefixes = ("qa domain", "qa course", "test ", "temp ", "dummy ", "sample ")
    if text.startswith(prefixes):
        return True
    return False


def _delete_noise_rows() -> dict[str, int]:
    deleted = {
        "domains": 0,
        "courses": 0,
        "modules": 0,
        "syllabus": 0,
        "videos": 0,
        "quizzes": 0,
        "assignments": 0,
    }

    for row in CourseModule.query.all():
        if _looks_like_noise(row.title):
            db.session.delete(row)
            deleted["modules"] += 1

    for row in Syllabus.query.all():
        if _looks_like_noise(row.topic_title):
            db.session.delete(row)
            deleted["syllabus"] += 1

    for row in Video.query.all():
        if _looks_like_noise(row.title):
            db.session.delete(row)
            deleted["videos"] += 1

    for row in Quiz.query.all():
        if _looks_like_noise(row.title):
            db.session.delete(row)
            deleted["quizzes"] += 1

    for row in Assignment.query.all():
        if _looks_like_noise(row.title):
            db.session.delete(row)
            deleted["assignments"] += 1

    for row in Course.query.all():
        if _looks_like_noise(row.title):
            db.session.delete(row)
            deleted["courses"] += 1

    for row in Domain.query.all():
        if _looks_like_noise(row.name):
            db.session.delete(row)
            deleted["domains"] += 1

    db.session.flush()
    return deleted


def _dedupe_domains() -> int:
    removed = 0
    seen = {}
    for domain in Domain.query.order_by(Domain.id.asc()).all():
        key = _normalize(domain.name)
        if key not in seen:
            seen[key] = domain
            continue
        keeper = seen[key]
        for course in Course.query.filter_by(domain_id=domain.id).all():
            course.domain_id = keeper.id
        db.session.delete(domain)
        removed += 1
    db.session.flush()
    return removed


def _dedupe_by_course_scope(model_cls, title_attr: str, owner_attr: str = "course_id") -> int:
    removed = 0
    seen = {}
    rows = model_cls.query.order_by(model_cls.id.asc()).all()
    for row in rows:
        owner_id = getattr(row, owner_attr)
        key = (owner_id, _normalize(getattr(row, title_attr)))
        if key not in seen:
            seen[key] = row.id
            continue
        db.session.delete(row)
        removed += 1
    db.session.flush()
    return removed


def _dedupe_courses() -> int:
    removed = 0
    seen = {}
    rows = Course.query.order_by(Course.id.asc()).all()
    for row in rows:
        key = (row.domain_id, _normalize(row.title))
        if key not in seen:
            seen[key] = row.id
            continue
        db.session.delete(row)
        removed += 1
    db.session.flush()
    return removed


def cleanup_catalog_noise_and_duplicates() -> dict[str, int]:
    report = _delete_noise_rows()
    report["duplicate_domains_removed"] = _dedupe_domains()
    report["duplicate_courses_removed"] = _dedupe_courses()
    report["duplicate_modules_removed"] = _dedupe_by_course_scope(CourseModule, "title")
    report["duplicate_syllabus_removed"] = _dedupe_by_course_scope(Syllabus, "topic_title")
    report["duplicate_videos_removed"] = _dedupe_by_course_scope(Video, "title")
    report["duplicate_quizzes_removed"] = _dedupe_by_course_scope(Quiz, "title")
    report["duplicate_assignments_removed"] = _dedupe_by_course_scope(Assignment, "title")
    return report


def main() -> None:
    with app.app_context():
        cleanup_report = cleanup_catalog_noise_and_duplicates()
        seeded_report = seed_catalog()
        db.session.commit()

        print("Startup catalog refresh completed")
        print("Cleanup summary:")
        for key, value in cleanup_report.items():
            print(f"  - {key}: {value}")
        print("Seed summary:")
        for key, value in seeded_report.items():
            print(f"  - {key}: {value}")


if __name__ == "__main__":
    main()
