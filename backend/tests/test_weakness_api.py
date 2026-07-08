"""
Mentra X — Unit & Integration Tests for Phase 8 Milestone 4 (API & Tool Integration)

Tests Flask API endpoints for weakness profile retrieval, pre-test vulnerability scans,
misconception reports, remediation plans, closed-loop verification, and Mastra tool execution.
"""

import sys
import unittest
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import app
from backend.models import db, Quiz
from backend.services.twin.twin_builder import build_initial_twin
from backend.services.orchestration.tools.registry import ToolRegistry
from backend.services.orchestration.tools.tutor_tools import register_tutor_tools
from backend.tests.test_support import SQLiteFixtureMixin


class TestWeaknessAPI(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixture()

    def test_get_profile_endpoint(self):
        with app.app_context():
            user_id = self.fixture_ids["student_id"]
            build_initial_twin(user_id, "JEE")
            
        res = self.client.get(f"/api/weakness/profile/{user_id}")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["status"], "success")
        self.assertIn("profile", data)
        self.assertIn("user_id", data["profile"])

    def test_vulnerability_scan_endpoint(self):
        with app.app_context():
            user_id = self.fixture_ids["student_id"]
            quiz = Quiz.query.filter_by(title="API Integration Test Quiz", course_id=1).first()
            if not quiz:
                quiz = Quiz(title="API Integration Test Quiz", course_id=1)
                db.session.add(quiz)
                db.session.commit()
            quiz_id = quiz.id

        res = self.client.get(f"/api/weakness/vulnerabilities/{user_id}/{quiz_id}")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["status"], "success")
        self.assertIn("vulnerability_scan", data)

    def test_misconceptions_endpoint(self):
        with app.app_context():
            user_id = self.fixture_ids["student_id"]

        res = self.client.get(f"/api/weakness/misconceptions/{user_id}")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["status"], "success")
        self.assertIn("misconception_reports", data)

    def test_remediation_endpoints(self):
        with app.app_context():
            user_id = self.fixture_ids["student_id"]

        # Get Plan
        res = self.client.get(f"/api/weakness/remediation/{user_id}/calculus_integration")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["status"], "success")
        self.assertIn("remediation_plan", data)

        # Generate Quiz
        res_quiz = self.client.post(f"/api/weakness/remediation/quiz/{user_id}/calculus_integration")
        self.assertEqual(res_quiz.status_code, 200)
        data_quiz = json.loads(res_quiz.data)
        self.assertEqual(data_quiz["status"], "success")
        self.assertIn("custom_quiz", data_quiz)

        # Verify Remediation
        verify_payload = {"user_id": user_id, "concept_id": "calculus_integration", "passed": True, "new_score": 0.85}
        res_ver = self.client.post("/api/weakness/remediation/verify", data=json.dumps(verify_payload), content_type="application/json")
        self.assertEqual(res_ver.status_code, 200)
        data_ver = json.loads(res_ver.data)
        self.assertEqual(data_ver["status"], "success")
        self.assertTrue(data_ver["verified"])

    def test_mastra_weakness_tool(self):
        with app.app_context():
            user_id = self.fixture_ids["student_id"]
            registry = ToolRegistry()
            registry.clear()
            register_tutor_tools(registry)
            
            tools = registry.get_all_tools()
            self.assertIn("diagnoseWeaknessProfile", tools)
            
            res = registry.execute_tool("diagnoseWeaknessProfile", kwargs={"user_id": user_id})
            self.assertIsNotNone(res)
            self.assertEqual(res.get("user_id"), user_id)


if __name__ == "__main__":
    unittest.main()
