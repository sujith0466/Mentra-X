from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import app
from backend.models import QuizAttempt, db
from backend.services.ai.career_service import generate_career_roadmap
from backend.services.ai.learning.notes_service import generate_notes
from backend.services.ai.learning.quiz_generator_service import generate_quiz_from_lesson
from backend.services.ai.learning.revision_service import get_revision_topics
from backend.services.ai.learning.study_planner_service import generate_adaptive_learning_path, generate_study_plan
from backend.services.ai.learning_feed_service import generate_learning_feed
from backend.services.ai.project_idea_service import generate_project_ideas
from backend.services.ai.recommendation_service import recommend_courses
from backend.services.ai.skills.skill_graph_service import build_skill_graph, get_skill_progress_snapshot
from tests.test_support import SQLiteFixtureMixin


class TestLearningAI(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()
        cls.ensure_enrollment(progress=20.0, completed=False)

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixture()

    def test_phase1_services_return_structured_data(self):
        with app.app_context():
            ideas = generate_project_ideas("AI")
            self.assertTrue(ideas)
            self.assertIn("title", ideas[0])
            roadmap = generate_career_roadmap("AI Engineer")
            self.assertIn("skills", roadmap)
            recommendations = recommend_courses(self.fixture_ids["student_id"])
            self.assertTrue(recommendations)
            self.assertIn("id", recommendations[0])

    def test_phase2_and_phase8_services_return_structured_data(self):
        with app.app_context():
            notes = generate_notes(self.fixture_ids["video_id"])
            self.assertIn("key_points", notes)
            questions = generate_quiz_from_lesson(self.fixture_ids["video_id"])
            self.assertTrue(questions)
            self.assertIn("question", questions[0])
            plan = generate_study_plan(self.fixture_ids["student_id"], self.fixture_ids["course_id"], 3)
            self.assertIn("days", plan)
            db.session.add(
                QuizAttempt(
                    quiz_id=self.fixture_ids["quiz_id"],
                    user_id=self.fixture_ids["student_id"],
                    attempt_number=1,
                    total_questions=1,
                    correct_answers=0,
                    score_percentage=30.0,
                    passed=False,
                )
            )
            db.session.commit()
            revision_topics = get_revision_topics(self.fixture_ids["student_id"])
            self.assertTrue(revision_topics)
            adaptive_path = generate_adaptive_learning_path(self.fixture_ids["student_id"])
            self.assertIn("recommended_lessons", adaptive_path)
            self.assertIn("revision_topics", adaptive_path)
            skill_graph = build_skill_graph(self.fixture_ids["student_id"])
            self.assertTrue(skill_graph)
            snapshot = get_skill_progress_snapshot(self.fixture_ids["student_id"])
            self.assertIsInstance(snapshot, list)
            feed = generate_learning_feed(self.fixture_ids["student_id"])
            self.assertTrue(feed)

    def test_ai_routes_render_for_logged_in_student(self):
        self.login_student(self.client)
        for path in [
            "/student/ai/project-ideas",
            "/student/ai/career-roadmap",
            "/student/ai/recommendations",
            "/student/ai/study-planner",
            f"/student/ai/notes/{self.fixture_ids['video_id']}",
            f"/student/ai/practice-quiz/{self.fixture_ids['video_id']}",
            "/student/ai/revision",
            "/student/skills",
        ]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, msg=path)


if __name__ == "__main__":
    unittest.main()
