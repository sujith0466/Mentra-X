from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app
from models import CodingChallenge, CodingSubmission, SkillProgress, db
from services.ai.assistant_service import mentor_assistant
from services.ai.coding import analyze_code_solution, create_submission, evaluate_submission, execute_python_code, update_skill_progress_for_challenge
from services.ai.learning_feed_service import generate_learning_feed
from tests.test_support import SQLiteFixtureMixin


class TestCodingPlatform(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()
        cls.ensure_enrollment(progress=35.0, completed=False)
        cls.challenge_title = f"Two Sum {cls.fixture_token}"
        with app.app_context():
            challenge = CodingChallenge(
                title=cls.challenge_title,
                description="Given an array of integers, return indices of the two numbers that add up to a target.",
                difficulty="Beginner",
                topic="Python Functions",
                starter_code="def two_sum(nums, target):\n    pass",
                expected_output="[0, 1]",
                test_cases_json=json.dumps([
                    {"input": "[2,7,11,15],9", "output": "[0,1]"},
                    {"input": "[3,2,4],6", "output": "[1,2]"}
                ]),
            )
            db.session.add(challenge)
            db.session.commit()
            cls.challenge_id = challenge.id

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            CodingSubmission.query.filter_by(challenge_id=cls.challenge_id).delete(synchronize_session=False)
            CodingChallenge.query.filter_by(id=cls.challenge_id).delete(synchronize_session=False)
            SkillProgress.query.filter_by(user_id=cls.fixture_ids["student_id"], skill_name="Python Functions").delete(synchronize_session=False)
            db.session.commit()
        cls.cleanup_fixture()

    def test_challenge_listing_route_renders(self):
        self.login_student(self.client)
        response = self.client.get("/student/coding/challenges")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.challenge_title.encode("utf-8"), response.data)

    def test_code_execution_and_feedback_services(self):
        execution = execute_python_code("print('mentra sandbox')")
        self.assertTrue(execution["success"])
        self.assertEqual(execution["output"], "mentra sandbox")

        feedback = analyze_code_solution("def solve(nums):\n    for i in nums:\n        for j in nums:\n            return i + j")
        self.assertIn("complexity_hint", feedback)
        self.assertIn("suggestion", feedback)

    def test_auto_grading_submission_storage_and_skill_progress(self):
        with app.app_context():
            challenge = CodingChallenge.query.get(self.challenge_id)
            code = (
                "def two_sum(nums, target):\n"
                "    seen = {}\n"
                "    for index, value in enumerate(nums):\n"
                "        if target - value in seen:\n"
                "            return [seen[target - value], index]\n"
                "        seen[value] = index\n"
            )
            evaluation = evaluate_submission(code, challenge)
            self.assertEqual(evaluation["passed_tests"], 2)
            self.assertEqual(evaluation["score"], 100.0)

            submission = create_submission(self.fixture_ids["student_id"], challenge, code, evaluation)
            self.assertIsNotNone(submission.id)

            skill_row = update_skill_progress_for_challenge(self.fixture_ids["student_id"], challenge, evaluation["score"])
            self.assertEqual(skill_row.skill_name, "Python Functions")
            self.assertEqual(skill_row.progress_percentage, 100.0)

            stored = CodingSubmission.query.get(submission.id)
            self.assertIsNotNone(stored)
            feed = generate_learning_feed(self.fixture_ids["student_id"])
            self.assertTrue(any("New coding challenge available" in item for item in feed))
            self.assertTrue(any("Python Functions skill improved" in item for item in feed))

    def test_submit_route_and_mentor_integration(self):
        self.login_student(self.client)
        code = (
            "def two_sum(nums, target):\n"
            "    lookup = {}\n"
            "    for index, value in enumerate(nums):\n"
            "        match = target - value\n"
            "        if match in lookup:\n"
            "            return [lookup[match], index]\n"
            "        lookup[value] = index\n"
        )
        response = self.client.post(
            f"/student/coding/submit/{self.challenge_id}",
            data={"code_submitted": code},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AI Feedback", response.data)

        with app.app_context():
            payload = mentor_assistant(self.fixture_ids["student_id"], "Give me coding practice")
            self.assertEqual(payload["intent"], "coding_practice")
            self.assertIn("/student/coding/challenges", payload["answer"])


if __name__ == "__main__":
    unittest.main()
