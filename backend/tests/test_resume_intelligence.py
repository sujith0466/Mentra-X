from __future__ import annotations

import io
import sys
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import app
from backend.models import User, UserResume, db
from backend.services.ai.career.resume_parser_service import parse_resume
from tests.test_support import SQLiteFixtureMixin


class TestResumeIntelligence(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixture()

    def test_resume_parser_outputs_structure(self):
        parsed = parse_resume("Python Flask SQL project experience. B.Tech AI & Data Science.")
        self.assertIn("skills", parsed)
        self.assertIn("projects", parsed)
        self.assertIn("education", parsed)
        self.assertIn("experience", parsed)

    def test_dashboard_resume_sections(self):
        self.login_student(self.client)
        response = self.client.get("/student/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No resume uploaded yet", response.data)

        with app.app_context():
            resume_row = UserResume(
                user_id=self.fixture_ids["student_id"],
                resume_path="resumes/test_resume.docx",
                skills_json='["Python", "Flask", "SQL"]',
                projects_json='["AI Resume Analyzer"]',
                education_json='["B.Tech AI & Data Science"]',
                experience_json='["Internship - Web Development"]',
            )
            db.session.add(resume_row)
            db.session.commit()

        response = self.client.get("/student/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Resume Insights", response.data)
        self.assertIn(b"Python", response.data)

    def test_registration_with_optional_resume_upload(self):
        unique_email = f"qa_resume_{self.fixture_token}_{uuid.uuid4().hex[:4]}@example.com"
        fake_docx = io.BytesIO(b"Fake docx content")
        response = self.client.post(
            "/auth/register",
            data={
                "name": "QA Resume User",
                "email": unique_email,
                "password": "Password123",
                "confirm_password": "Password123",
                "resume": (fake_docx, "resume.docx"),
            },
            content_type="multipart/form-data",
            follow_redirects=False,
        )
        self.assertEqual(response.status_code, 302)
        with app.app_context():
            user = User.query.filter_by(email=unique_email).first()
            self.assertIsNotNone(user)
            resume_row = UserResume.query.filter_by(user_id=user.id).first()
            self.assertIsNotNone(resume_row)


if __name__ == "__main__":
    unittest.main()
