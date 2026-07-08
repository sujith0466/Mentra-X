"""
Mentra X — Unit & Integration Tests for Phase 8 Milestone 3 (Remediation Engine)

Tests 4-step intervention plan generation, avoidance constraint creation,
customized remediation drills, study path injection, and closed-loop verification.
"""

import sys
import unittest
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import app
from backend.models import db, StudentTwinRecord, TwinKnowledgeStateRecord
from backend.services.adaptive.remediation_engine import RemediationEngine
from backend.services.twin.twin_builder import build_initial_twin
from backend.tests.test_support import SQLiteFixtureMixin


class TestRemediationEngine(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixture()

    def setUp(self):
        self.engine = RemediationEngine()

    def test_remediation_plan_generation_with_fixture(self):
        with app.app_context():
            user_id = self.fixture_ids["student_id"]
            twin = build_initial_twin(user_id, "JEE")
            self.assertIsNotNone(twin)

            # Add weak concept
            ks = TwinKnowledgeStateRecord.query.filter_by(twin_id=twin.id, concept_id="calculus_integration").first()
            if not ks:
                ks = TwinKnowledgeStateRecord(twin_id=twin.id, concept_id="calculus_integration", mastery_score=0.30, mistake_count=5)
                db.session.add(ks)
            else:
                ks.mastery_score = 0.30
                ks.mistake_count = 5
            db.session.commit()

            plan = self.engine.generate_remediation_plan(user_id, "calculus_integration")
            self.assertIsNotNone(plan)
            self.assertEqual(plan["user_id"], user_id)
            self.assertEqual(plan["concept_id"], "calculus_integration")
            self.assertEqual(len(plan["step_by_step_path"]), 4)
            self.assertEqual(plan["step_by_step_path"][0]["step_number"], 1)
            self.assertIn("avoidance_constraints", plan)
            self.assertIn("levels_to_avoid", plan["avoidance_constraints"])

    def test_custom_quiz_generation_with_fixture(self):
        with app.app_context():
            user_id = self.fixture_ids["student_id"]
            quiz = self.engine.generate_custom_quiz(user_id, "calculus_integration")
            self.assertIsNotNone(quiz)
            self.assertEqual(quiz["user_id"], user_id)
            self.assertEqual(quiz["concept_id"], "calculus_integration")
            self.assertGreaterEqual(len(quiz["questions"]), 1)

    def test_inject_remediation_into_path(self):
        with app.app_context():
            user_id = self.fixture_ids["student_id"]
            twin = build_initial_twin(user_id, "JEE")
            ks = TwinKnowledgeStateRecord.query.filter_by(twin_id=twin.id, concept_id="calculus_integration").first()
            if not ks:
                ks = TwinKnowledgeStateRecord(twin_id=twin.id, concept_id="calculus_integration", mastery_score=0.30, mistake_count=5)
                db.session.add(ks)
            else:
                ks.mastery_score = 0.30
            db.session.commit()

            mock_path = [
                {"node_id": "LESSON_1", "title": "Advanced Integration Techniques", "node_type": "LESSON"},
                {"node_id": "QUIZ_1", "title": "Integration Quiz", "node_type": "QUIZ"}
            ]

            injected = self.engine.inject_remediation_into_path(user_id, mock_path)
            self.assertGreater(len(injected), len(mock_path))
            self.assertEqual(injected[0]["node_type"], "REMEDIATION_DRILL")
            self.assertIn("⚠️ Required Intervention", injected[0]["title"])
            self.assertTrue(injected[0]["is_mandatory"])

    def test_verify_remediation_completion(self):
        with app.app_context():
            user_id = self.fixture_ids["student_id"]
            success = self.engine.verify_remediation_completion(user_id, "calculus_integration", passed=True, new_score=0.82)
            self.assertTrue(success)

            # Verify twin mastery updated
            twin = StudentTwinRecord.query.filter_by(user_id=user_id).first()
            ks = TwinKnowledgeStateRecord.query.filter_by(twin_id=twin.id, concept_id="calculus_integration").first()
            self.assertIsNotNone(ks)
            self.assertGreaterEqual(ks.mastery_score, 0.75)


if __name__ == "__main__":
    unittest.main()
