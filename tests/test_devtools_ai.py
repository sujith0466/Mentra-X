from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app
from services.ai.devtools.codebase_service import analyze_project_structure
from services.ai.devtools.coding_practice_service import generate_coding_problem
from services.ai.devtools.debug_service import explain_error
from tests.test_support import SQLiteFixtureMixin


class TestDeveloperAI(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixture()

    def test_devtool_services_return_structured_outputs(self):
        problem = generate_coding_problem("Python")
        self.assertIn("solution", problem)
        self.assertIn("difficulty", problem)
        debug_payload = explain_error("TypeError: unsupported operand type")
        self.assertIn("possible_fix", debug_payload)
        self.assertIn("error_type", debug_payload)
        structure = analyze_project_structure(["app.py", "models.py", "templates/base.html"])
        self.assertIn("architecture", structure)
        self.assertIn("project_type", structure)

    def test_devtool_routes_render(self):
        self.login_student(self.client)
        get_paths = [
            "/student/devtools/coding-practice",
            "/student/devtools/debug",
            "/student/devtools/codebase-explainer",
        ]
        for path in get_paths:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, msg=path)

        coding_response = self.client.post(
            "/student/devtools/coding-practice",
            data={"topic": "Python", "attempt": "def solve(tasks):\n    return len(tasks)", "action": "run"},
        )
        self.assertEqual(coding_response.status_code, 200)

        self.assertEqual(
            self.client.post("/student/devtools/debug", data={"error_text": "SyntaxError: invalid syntax"}).status_code,
            200,
        )
        project_file, filename = self.text_upload("app.py\nmodels.py\ntemplates/base.html", "project.txt")
        codebase_response = self.client.post(
            "/student/devtools/codebase-explainer",
            data={"files_text": "", "project_file": (project_file, filename)},
            content_type="multipart/form-data",
        )
        self.assertEqual(codebase_response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
