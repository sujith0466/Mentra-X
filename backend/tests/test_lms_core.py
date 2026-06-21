from __future__ import annotations

import sys
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import app
from backend.models import AssignmentSubmission, Enrollment, LessonProgress, QuizAttempt, db
from tests.test_support import SQLiteFixtureMixin


class TestLMSCore(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixture()

    def test_registration_login_logout_flow(self):
        unique_email = f"qa_register_{self.fixture_token}_{uuid.uuid4().hex[:4]}@example.com"
        register_response = self.client.post(
            "/auth/register",
            data={
                "name": "QA Register User",
                "email": unique_email,
                "password": "Password123",
                "confirm_password": "Password123",
            },
            follow_redirects=False,
        )
        self.assertEqual(register_response.status_code, 302)

        login_response = self.client.post(
            "/auth/login",
            data={"email": unique_email, "password": "Password123"},
            follow_redirects=False,
        )
        self.assertEqual(login_response.status_code, 302)
        self.assertIn("/student/dashboard", login_response.headers.get("Location", ""))

        logout_response = self.client.get("/auth/logout", follow_redirects=False)
        self.assertEqual(logout_response.status_code, 302)
        self.assertIn("/", logout_response.headers.get("Location", ""))

    def test_public_routes_return_success(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/courses").status_code, 200)
        self.assertEqual(self.client.get("/student/courses").status_code, 200)
        self.assertEqual(self.client.get("/auth/login").status_code, 200)
        self.assertEqual(self.client.get("/auth/register").status_code, 200)

    def test_protected_routes_redirect_without_login(self):
        self.clear_session(self.client)
        self.assertEqual(self.client.get("/student/dashboard", follow_redirects=False).status_code, 302)
        self.assertEqual(self.client.get("/student/my-courses", follow_redirects=False).status_code, 302)

    def test_dashboard_loads_for_logged_in_student(self):
        self.ensure_enrollment(progress=25.0, completed=False)
        self.login_student(self.client)
        response = self.client.get("/student/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AI Learning Insights", response.data)

    def test_course_enrollment_and_video_loading(self):
        self.login_student(self.client)
        enroll_response = self.client.post(f"/student/enroll/{self.fixture_ids['course_id']}", follow_redirects=False)
        self.assertIn(enroll_response.status_code, [302, 303])
        with app.app_context():
            enrollment = Enrollment.query.filter_by(
                user_id=self.fixture_ids["student_id"],
                course_id=self.fixture_ids["course_id"],
            ).first()
            self.assertIsNotNone(enrollment)
        video_response = self.client.get(f"/student/course/{self.fixture_ids['course_id']}")
        self.assertEqual(video_response.status_code, 200)

    def test_quiz_attempt_submission(self):
        self.ensure_enrollment(progress=10.0, completed=False)
        self.login_student(self.client)
        take_response = self.client.get(f"/student/quiz/{self.fixture_ids['quiz_id']}")
        self.assertEqual(take_response.status_code, 200)
        with app.app_context():
            attempt = QuizAttempt.query.filter_by(
                user_id=self.fixture_ids["student_id"],
                quiz_id=self.fixture_ids["quiz_id"],
                submitted_at=None,
            ).order_by(QuizAttempt.id.desc()).first()
            self.assertIsNotNone(attempt)
            submit_response = self.client.post(
                f"/student/quiz/{self.fixture_ids['quiz_id']}/submit",
                data={
                    "attempt_id": attempt.id,
                    f"question_{self.fixture_ids['question_id']}": "Python",
                },
                follow_redirects=False,
            )
            self.assertIn(submit_response.status_code, [302, 303])
            db.session.expire_all()
            submitted = QuizAttempt.query.get(attempt.id)
            self.assertIsNotNone(submitted.submitted_at)

    def test_assignment_submission_progress_and_certificate(self):
        self.ensure_enrollment(progress=0.0, completed=False)
        self.login_student(self.client)
        assignment_response = self.client.post(
            f"/student/assignment/{self.fixture_ids['assignment_id']}/submit",
            data={"answer_text": "Flask routes connect URLs to view functions."},
            follow_redirects=False,
        )
        self.assertIn(assignment_response.status_code, [302, 303])
        with app.app_context():
            submission = AssignmentSubmission.query.filter_by(
                user_id=self.fixture_ids["student_id"],
                assignment_id=self.fixture_ids["assignment_id"],
            ).first()
            self.assertIsNotNone(submission)

        progress_response = self.client.post(
            f"/student/course/{self.fixture_ids['course_id']}/lesson/{self.fixture_ids['video_id']}/complete",
            follow_redirects=False,
        )
        self.assertIn(progress_response.status_code, [302, 303])
        with app.app_context():
            progress_row = LessonProgress.query.filter_by(
                user_id=self.fixture_ids["student_id"],
                lesson_id=self.fixture_ids["video_id"],
                course_id=self.fixture_ids["course_id"],
            ).first()
            self.assertIsNotNone(progress_row)
            enrollment = Enrollment.query.filter_by(
                user_id=self.fixture_ids["student_id"],
                course_id=self.fixture_ids["course_id"],
            ).first()
            enrollment.progress = 100
            enrollment.progress_percentage = 100
            enrollment.completed = True
            db.session.commit()

        certificate_response = self.client.get(f"/student/certificate/{self.fixture_ids['course_id']}/download")
        self.assertEqual(certificate_response.status_code, 200)
        self.assertIn("application/pdf", certificate_response.mimetype)


if __name__ == "__main__":
    unittest.main()
