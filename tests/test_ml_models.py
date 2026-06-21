from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app
from services.ai.ml import learning_difficulty_model, recommendation_model, skill_prediction_model


class TestMLModels(unittest.TestCase):
    def test_recommendation_model_fallback_path(self):
        rows = [
            {"id": 1, "title": "Course A", "domain": "AI", "description": "Intro AI", "text_blob": "ai intro"},
            {"id": 2, "title": "Course B", "domain": "AI", "description": "Advanced AI", "text_blob": "ai advanced"},
        ]
        fake_enrollment_model = SimpleNamespace(query=SimpleNamespace(filter_by=lambda **kwargs: SimpleNamespace(all=lambda: [])))
        with app.app_context(), \
             patch.object(recommendation_model, "_course_rows", return_value=rows), \
             patch.object(recommendation_model, "TfidfVectorizer", None), \
             patch.object(recommendation_model, "cosine_similarity", None), \
             patch.object(recommendation_model, "Enrollment", fake_enrollment_model):
            payload = recommendation_model.recommend_courses_ml(99)
        self.assertTrue(payload["recommended_courses"])
        self.assertEqual(len(payload["recommended_courses"]), 2)

    def test_recommendation_model_ml_path(self):
        rows = [
            {"id": 1, "title": "Course A", "domain": "AI", "description": "Intro AI", "text_blob": "ai intro"},
            {"id": 2, "title": "Course B", "domain": "AI", "description": "Advanced AI", "text_blob": "ai advanced"},
        ]

        class FakeVectorizer:
            def __init__(self, *args, **kwargs):
                pass
            def fit_transform(self, texts):
                return texts

        enrollments = [SimpleNamespace(course_id=1, completed=True, progress_percentage=100, progress=100)]
        fake_enrollment_model = SimpleNamespace(query=SimpleNamespace(filter_by=lambda **kwargs: SimpleNamespace(all=lambda: enrollments)))
        with app.app_context(), \
             patch.object(recommendation_model, "_course_rows", return_value=rows), \
             patch.object(recommendation_model, "TfidfVectorizer", FakeVectorizer), \
             patch.object(recommendation_model, "cosine_similarity", lambda matrix: [[1.0, 0.88], [0.88, 1.0]]), \
             patch.object(recommendation_model, "Enrollment", fake_enrollment_model):
            payload = recommendation_model.recommend_courses_ml(42)
        self.assertTrue(payload["recommended_courses"])
        self.assertGreater(payload["confidence_score"][0], 0)

    def test_skill_prediction_fallback_path(self):
        course = SimpleNamespace(domain=SimpleNamespace(name="Artificial Intelligence"))
        enrollments = [SimpleNamespace(course=course, completed=True, progress_percentage=100, progress=100)]
        attempts = [SimpleNamespace(quiz_id=1, score_percentage=40)]
        quiz_model = SimpleNamespace(query=SimpleNamespace(get=lambda quiz_id: SimpleNamespace(course=course)))
        enrollment_model = SimpleNamespace(query=SimpleNamespace(filter_by=lambda **kwargs: SimpleNamespace(all=lambda: enrollments)))
        attempt_model = SimpleNamespace(query=SimpleNamespace(filter_by=lambda **kwargs: SimpleNamespace(all=lambda: attempts)))
        with app.app_context(), \
             patch.object(skill_prediction_model, "np", None), \
             patch.object(skill_prediction_model, "pd", None), \
             patch.object(skill_prediction_model, "Enrollment", enrollment_model), \
             patch.object(skill_prediction_model, "QuizAttempt", attempt_model), \
             patch.object(skill_prediction_model, "Quiz", quiz_model), \
             patch.object(skill_prediction_model, "detect_skill_gap", return_value={"skills_missing": ["Deployment"], "recommended_projects": ["AI dashboard"]}):
            payload = skill_prediction_model.predict_next_skills(42)
        self.assertIn("skills_to_learn_next", payload)
        self.assertTrue(payload["skills_to_learn_next"])

    def test_learning_difficulty_fallback_path(self):
        enrollments = [SimpleNamespace(course=SimpleNamespace(title="QA Course"), completed=False, progress_percentage=20, progress=20)]
        lessons = [SimpleNamespace(course_id=1, completed=False), SimpleNamespace(course_id=1, completed=False)]
        attempts = [SimpleNamespace(quiz_id=1, score_percentage=45)]
        streak_model = SimpleNamespace(query=SimpleNamespace(filter_by=lambda **kwargs: SimpleNamespace(first=lambda: SimpleNamespace(current_streak=0))))
        enrollment_model = SimpleNamespace(query=SimpleNamespace(filter_by=lambda **kwargs: SimpleNamespace(all=lambda: enrollments)))
        lesson_model = SimpleNamespace(query=SimpleNamespace(filter_by=lambda **kwargs: SimpleNamespace(all=lambda: lessons)))
        attempt_model = SimpleNamespace(query=SimpleNamespace(filter_by=lambda **kwargs: SimpleNamespace(all=lambda: attempts)))
        course_model = SimpleNamespace(query=SimpleNamespace(get=lambda course_id: SimpleNamespace(title="QA Course")))
        quiz_model = SimpleNamespace(query=SimpleNamespace(get=lambda quiz_id: SimpleNamespace(title="QA Quiz")))
        video_chain = SimpleNamespace(all=lambda: [SimpleNamespace(title="QA Lesson")])
        video_model = SimpleNamespace(query=SimpleNamespace(join=lambda *args, **kwargs: SimpleNamespace(filter=lambda *a, **k: SimpleNamespace(order_by=lambda *oa, **ok: SimpleNamespace(limit=lambda n: video_chain)))))
        with app.app_context(), \
             patch.object(learning_difficulty_model, "pd", None), \
             patch.object(learning_difficulty_model, "Enrollment", enrollment_model), \
             patch.object(learning_difficulty_model, "LessonProgress", lesson_model), \
             patch.object(learning_difficulty_model, "QuizAttempt", attempt_model), \
             patch.object(learning_difficulty_model, "LearningStreak", streak_model), \
             patch.object(learning_difficulty_model, "Course", course_model), \
             patch.object(learning_difficulty_model, "Quiz", quiz_model), \
             patch.object(learning_difficulty_model, "Video", video_model):
            payload = learning_difficulty_model.detect_learning_difficulty(42)
        self.assertIn("weak_topics", payload)
        self.assertTrue(payload["recommended_revision"])


if __name__ == "__main__":
    unittest.main()
