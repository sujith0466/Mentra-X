from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app
from models import (
    CodingChallenge,
    InterviewQuestion,
    InterviewResponse,
    InterviewSession,
    SkillProgress,
    db,
)
from services.ai.assistant_service import mentor_assistant
from services.ai.interview import (
    analyze_interview_answer,
    generate_interview_questions,
    get_session_detail,
    start_interview,
    submit_interview_answers,
)
from services.ai.learning_feed_service import generate_learning_feed
from tests.test_support import SQLiteFixtureMixin


class TestInterviewSystem(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()
        with app.app_context():
            challenge = CodingChallenge(
                title=f"Interview Arrays {cls.fixture_token}",
                description="Return the max value from a list of integers.",
                difficulty="Intermediate",
                topic="Algorithms",
                starter_code="def find_max(nums):\n    pass",
                expected_output="9",
                test_cases_json=json.dumps([{"input": "[1,9,3]", "output": "9"}]),
            )
            db.session.add(challenge)
            db.session.commit()
            cls.challenge_id = challenge.id

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            InterviewResponse.query.delete(synchronize_session=False)
            InterviewQuestion.query.delete(synchronize_session=False)
            InterviewSession.query.filter_by(user_id=cls.fixture_ids["student_id"]).delete(synchronize_session=False)
            SkillProgress.query.filter_by(user_id=cls.fixture_ids["student_id"], skill_name="Algorithms").delete(synchronize_session=False)
            SkillProgress.query.filter_by(user_id=cls.fixture_ids["student_id"], skill_name="Backend Architecture").delete(synchronize_session=False)
            SkillProgress.query.filter_by(user_id=cls.fixture_ids["student_id"], skill_name="APIs").delete(synchronize_session=False)
            SkillProgress.query.filter_by(user_id=cls.fixture_ids["student_id"], skill_name="Databases").delete(synchronize_session=False)
            CodingChallenge.query.filter_by(id=cls.challenge_id).delete(synchronize_session=False)
            db.session.commit()
        cls.cleanup_fixture()

    def test_question_generation_and_feedback(self):
        with app.app_context():
            questions = generate_interview_questions("Backend Developer", "Intermediate")
            self.assertTrue(questions)
            self.assertTrue(any(item["question_type"] == "coding" for item in questions))

            analysis = analyze_interview_answer(
                "Explain REST API principles.",
                "REST APIs use resource-based endpoints, proper HTTP methods, and stateless requests.",
                "resource-based endpoints,statelessness,http methods,status codes",
            )
            self.assertIn("feedback", analysis)
            self.assertGreaterEqual(analysis["score"], 50)

    def test_session_creation_submission_and_skill_updates(self):
        with app.app_context():
            interview_session = start_interview(self.fixture_ids["student_id"], "Backend Developer", "Intermediate")
            self.assertIsNotNone(interview_session.id)
            detail = get_session_detail(interview_session.id)
            self.assertTrue(detail["questions"])

            answers = {}
            for question in detail["questions"]:
                if question.question_type == "coding":
                    answers[question.id] = "I would explain the algorithm, discuss time complexity, space complexity, and cover edge cases."
                elif "REST API" in question.question_text:
                    answers[question.id] = "REST uses resource-based endpoints, statelessness, HTTP methods, and clear status codes."
                elif "indexing" in question.question_text.lower():
                    answers[question.id] = "Indexing improves query performance and search speed, but write operations can become slower."
                else:
                    answers[question.id] = "I would explain the concept clearly, include the core points, and give an example."

            result = submit_interview_answers(interview_session.id, answers)
            self.assertEqual(result["session"].status, "completed")
            self.assertGreater(result["session"].score, 0)

            skill_row = SkillProgress.query.filter_by(
                user_id=self.fixture_ids["student_id"],
                skill_name="Backend Architecture",
            ).first()
            self.assertIsNotNone(skill_row)

            feed = generate_learning_feed(self.fixture_ids["student_id"])
            self.assertTrue(any("Mock interview completed for Backend Developer" in item for item in feed))
            self.assertTrue(any("interview score improved" in item for item in feed))

            mentor_payload = mentor_assistant(self.fixture_ids["student_id"], "Start mock interview")
            self.assertEqual(mentor_payload["intent"], "interview_preparation")
            self.assertIn("/student/interview/start", mentor_payload["answer"])

    def test_interview_routes_render_and_submit(self):
        self.login_student(self.client)
        self.assertEqual(self.client.get("/student/interview").status_code, 200)
        self.assertEqual(self.client.get("/student/interview/start").status_code, 200)

        start_response = self.client.post(
            "/student/interview/start",
            data={"role": "Backend Developer", "difficulty": "Intermediate"},
            follow_redirects=False,
        )
        self.assertIn(start_response.status_code, [302, 303])
        location = start_response.headers.get("Location", "")
        self.assertIn("/student/interview/session/", location)

        session_id = int(location.rstrip("/").split("/")[-1])
        session_response = self.client.get(location)
        self.assertEqual(session_response.status_code, 200)

        with app.app_context():
            questions = InterviewQuestion.query.filter_by(session_id=session_id).all()
            payload = {"session_id": session_id}
            for question in questions:
                payload[f"question_{question.id}"] = "Resource-based endpoints, statelessness, HTTP methods, and strong examples."

        submit_response = self.client.post("/student/interview/submit", data=payload, follow_redirects=True)
        self.assertEqual(submit_response.status_code, 200)
        self.assertIn(b"AI Feedback", submit_response.data)


if __name__ == "__main__":
    unittest.main()

