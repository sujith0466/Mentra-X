from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import app
from backend.models import ProjectIdea, ProjectTask, SkillProgress, StudentProject, db
from backend.services.ai.assistant_service import mentor_assistant
from backend.services.ai.career.portfolio_service import generate_portfolio
from backend.services.ai.learning_feed_service import generate_learning_feed
from backend.services.ai.projects import generate_project, get_student_project_detail, start_student_project, update_student_project_progress
from tests.test_support import SQLiteFixtureMixin


class TestProjectsSystem(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            student_projects = StudentProject.query.filter_by(user_id=cls.fixture_ids["student_id"]).all()
            project_ids = [row.id for row in student_projects]
            if project_ids:
                ProjectTask.query.filter(ProjectTask.project_id.in_(project_ids)).delete(synchronize_session=False)
            StudentProject.query.filter_by(user_id=cls.fixture_ids["student_id"]).delete(synchronize_session=False)
            ProjectIdea.query.filter(ProjectIdea.title.in_(["AI Resume Analyzer", "Mentra Course Marketplace"])).delete(synchronize_session=False)
            SkillProgress.query.filter_by(user_id=cls.fixture_ids["student_id"], skill_name="Project Delivery").delete(synchronize_session=False)
            SkillProgress.query.filter_by(user_id=cls.fixture_ids["student_id"], skill_name="AI").delete(synchronize_session=False)
            db.session.commit()
        cls.cleanup_fixture()

    def test_project_generation_and_progress_services(self):
        with app.app_context():
            project = generate_project("AI", "Intermediate")
            self.assertEqual(project.domain, "AI")
            self.assertTrue(project.get_tech_stack_list())

            student_project = start_student_project(self.fixture_ids["student_id"], project.id)
            self.assertIsNotNone(student_project.id)

            detail = get_student_project_detail(student_project.id)
            self.assertTrue(detail["tasks"])

            completed_ids = [task.id for task in detail["tasks"]]
            updated = update_student_project_progress(student_project.id, completed_ids)
            self.assertEqual(updated.progress_percentage, 100.0)
            self.assertIsNotNone(updated.completed_at)

            portfolio = generate_portfolio(self.fixture_ids["student_id"])
            self.assertIn(project.title, portfolio["projects"])

            feed = generate_learning_feed(self.fixture_ids["student_id"])
            self.assertTrue(any("Project completed" in item for item in feed))

            mentor_payload = mentor_assistant(self.fixture_ids["student_id"], "Give me project ideas")
            self.assertEqual(mentor_payload["intent"], "project_ideas")
            self.assertIn("/student/projects", mentor_payload["answer"])

    def test_project_routes_render(self):
        self.login_student(self.client)
        self.assertEqual(self.client.get("/student/projects").status_code, 200)
        generate_response = self.client.post(
            "/student/projects/generate",
            data={"domain": "Web Development", "difficulty": "Beginner"},
            follow_redirects=True,
        )
        self.assertEqual(generate_response.status_code, 200)
        self.assertIn(b"Mentra Course Marketplace", generate_response.data)

        with app.app_context():
            project = ProjectIdea.query.filter_by(title="Mentra Course Marketplace").order_by(ProjectIdea.id.desc()).first()
            self.assertIsNotNone(project)

        detail_response = self.client.get(f"/student/projects/{project.id}")
        self.assertEqual(detail_response.status_code, 200)

        start_response = self.client.post(f"/student/projects/start/{project.id}", follow_redirects=False)
        self.assertIn(start_response.status_code, [302, 303])


if __name__ == "__main__":
    unittest.main()

