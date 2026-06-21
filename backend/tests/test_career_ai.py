from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import app
from backend.services.ai.career.portfolio_service import generate_portfolio
from backend.services.ai.career.resume_service import analyze_resume
from backend.services.ai.career.skill_gap_service import detect_skill_gap
from tests.test_support import SQLiteFixtureMixin


class TestCareerAI(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()
        cls.ensure_enrollment(progress=100.0, completed=True)

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixture()

    def test_resume_analyzer_skill_gap_and_portfolio_services(self):
        with app.app_context():
            analysis = analyze_resume("Python Flask SQL project experience and API development")
            self.assertIn("detected_skills", analysis)
            gap = detect_skill_gap(self.fixture_ids["student_id"], "Backend Developer")
            self.assertIn("skills_missing", gap)
            portfolio = generate_portfolio(self.fixture_ids["student_id"])
            self.assertIn("courses_completed", portfolio)
            self.assertIn("projects", portfolio)

    def test_career_routes_and_resume_upload(self):
        self.login_student(self.client)
        self.assertEqual(self.client.get("/student/career/skill-gap").status_code, 200)
        self.assertEqual(self.client.get("/student/career/portfolio").status_code, 200)
        text_file, filename = self.text_upload("Python Flask SQL REST APIs", "resume.txt")
        response = self.client.post(
            "/student/career/resume-analyzer",
            data={
                "resume_text": "",
                "resume_file": (text_file, filename),
            },
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
