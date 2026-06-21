from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app
from services.ai import assistant_service
from services.ai.mentor_service import mentor_service
from tests.test_support import SQLiteFixtureMixin


class TestChatbotAssistant(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()
        cls.ensure_enrollment(progress=25.0, completed=False)

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixture()

    def test_intent_detection_keywords(self):
        self.assertEqual(assistant_service._detect_intent("Can you make a study plan for me?"), "study_help")
        self.assertEqual(assistant_service._detect_intent("I need career advice"), "career_advice")
        self.assertEqual(assistant_service._detect_intent("How do I fix this Python error?"), "coding_help")
        self.assertEqual(assistant_service._detect_intent("Recommend my next course"), "course_recommendation")
        self.assertEqual(assistant_service._detect_intent("Please improve my resume"), "resume_help")
        self.assertEqual(assistant_service._detect_intent("Give me project ideas"), "project_ideas")
        self.assertEqual(assistant_service._detect_intent("Show my learning progress"), "skill_progress")
        self.assertEqual(assistant_service._detect_intent("What skills should I learn next?"), "learning_path")

    def test_assistant_routes_queries_to_services(self):
        with app.app_context():
            payload = assistant_service.mentor_assistant(self.fixture_ids["student_id"], "Need a study plan")
            self.assertEqual(payload["intent"], "study_help")
            self.assertEqual(payload["agent"], "learning")
            self.assertIn("answer", payload)
            self.assertIn("response", payload)

        with app.app_context():
            payload = assistant_service.mentor_assistant(self.fixture_ids["student_id"], "Recommend my next course")
            self.assertEqual(payload["intent"], "course_recommendation")
            self.assertEqual(payload["agent"], "learning")

        with app.app_context():
            payload = assistant_service.mentor_assistant(self.fixture_ids["student_id"], "career roadmap for AI Engineer")
            self.assertEqual(payload["intent"], "career_advice")
            self.assertEqual(payload["agent"], "career")

        with app.app_context():
            payload = assistant_service.mentor_assistant(self.fixture_ids["student_id"], "debug this TypeError")
            self.assertEqual(payload["intent"], "coding_help")
            self.assertEqual(payload["agent"], "debug")

        with app.app_context():
            payload = assistant_service.mentor_assistant(self.fixture_ids["student_id"], "Improve my resume")
            self.assertEqual(payload["intent"], "resume_help")
            self.assertEqual(payload["agent"], "career")

        with app.app_context():
            payload = assistant_service.mentor_assistant(self.fixture_ids["student_id"], "project ideas for AI")
            self.assertEqual(payload["intent"], "project_ideas")
            self.assertEqual(payload["agent"], "project")

        with app.app_context():
            payload = assistant_service.mentor_assistant(self.fixture_ids["student_id"], "Show my learning progress")
            self.assertEqual(payload["intent"], "skill_progress")
            self.assertEqual(payload["agent"], "learning")

        with app.app_context():
            payload = assistant_service.mentor_assistant(self.fixture_ids["student_id"], "What skills should I learn next?")
            self.assertEqual(payload["intent"], "learning_path")
            self.assertEqual(payload["agent"], "learning")

    def test_available_agents_and_routing_helpers(self):
        agents = assistant_service.get_available_agents()
        self.assertGreaterEqual(len(agents), 6)
        self.assertEqual(assistant_service._detect_agent_name("Show my learning progress"), "learning")
        self.assertEqual(assistant_service._detect_agent_name("Why am I getting IndexError?"), "debug")
        self.assertEqual(assistant_service._detect_agent_name("Start mock interview"), "interview")

    def test_chatbot_endpoints_remain_functional(self):
        self.login_student(self.client)
        public_response = self.client.post(
            "/api/chatbot",
            json={"message": "Recommend my next course", "current_page": "dashboard"},
        )
        self.assertEqual(public_response.status_code, 200)
        self.assertTrue(public_response.get_json()["response"])

        widget_response = self.client.post(
            "/api/chatbot/ask",
            json={"question": "How do I practice coding?", "context": {"page": "dashboard"}},
        )
        self.assertEqual(widget_response.status_code, 200)
        self.assertIn("answer", widget_response.get_json())
        self.assertIn("agent", widget_response.get_json())

    def test_mentor_service_still_returns_structured_response(self):
        payload = mentor_service.get_structured_response("How do I build a portfolio?", current_page="dashboard")
        self.assertIn("answer", payload)
        self.assertIn("options", payload)


if __name__ == "__main__":
    unittest.main()
