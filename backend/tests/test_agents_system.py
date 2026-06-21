from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import app
from backend.models import CommunityPost, db
from backend.services.ai.assistant_service import get_available_agents, mentor_assistant
from backend.services.ai.learning_feed_service import generate_learning_feed
from tests.test_support import SQLiteFixtureMixin


class TestAgentsSystem(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()
        cls.ensure_enrollment(progress=35.0, completed=False)

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixture()

    def test_intent_routing_and_response_shape(self):
        with app.app_context():
            cases = [
                ("Show my learning progress", "learning", "skill_progress"),
                ("Why am I getting IndexError?", "debug", "coding_help"),
                ("Help me improve my resume", "career", "resume_help"),
                ("Give me project ideas for AI", "project", "project_ideas"),
                ("Start mock interview", "interview", "interview_preparation"),
                ("Show community questions", "community", "community_help"),
                ("Where is the study planner?", "learning", "study_help"),
            ]

            for message, agent_name, intent in cases:
                payload = mentor_assistant(self.fixture_ids["student_id"], message, current_page="dashboard")
                self.assertEqual(payload["agent"], agent_name)
                self.assertEqual(payload["intent"], intent)
                self.assertIn("response", payload)
                self.assertIn("answer", payload)
                self.assertIn("suggestions", payload)
                self.assertIn("options", payload)

    def test_fallback_behavior_and_available_agents(self):
        with app.app_context():
            payload = mentor_assistant(self.fixture_ids["student_id"], "Can you help me?", current_page="dashboard")
            self.assertEqual(payload["agent"], "mentor")
            self.assertTrue(payload["answer"])

            agents = get_available_agents()
            labels = {item["label"] for item in agents}
            self.assertIn("Learning AI", labels)
            self.assertIn("Debug AI", labels)
            self.assertIn("Interview AI", labels)

    def test_learning_feed_and_dashboard_show_agent_features(self):
        with app.app_context():
            post = CommunityPost(
                user_id=self.fixture_ids["student_id"],
                title="Flask routing error while using blueprints",
                content="I am getting a build error in url_for and need help.",
            )
            db.session.add(post)
            db.session.commit()

            feed = generate_learning_feed(self.fixture_ids["student_id"])
            self.assertTrue(any(item.startswith("Learning AI suggests:") for item in feed))
            self.assertTrue(any(item.startswith("Interview AI recommends:") for item in feed))

        self.login_student(self.client)
        response = self.client.get("/student/dashboard")
        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("AI Assistants", page)
        self.assertIn("Learning AI", page)
        self.assertIn("Debug AI", page)


if __name__ == "__main__":
    unittest.main()
