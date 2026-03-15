from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TESTS_DIR = ROOT / "tests"

MODULES = [
    "test_lms_core.py",
    "test_learning_ai.py",
    "test_career_ai.py",
    "test_devtools_ai.py",
    "test_ml_models.py",
    "test_chatbot_assistant.py",
    "test_agents_system.py",
    "test_projects_system.py",
    "test_community_system.py",
    "test_coding_platform.py",
    "test_interview_system.py",
    "test_resume_intelligence.py",
]


def main() -> int:
    loader = unittest.TestLoader()
    suite = loader.discover(str(TESTS_DIR), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    print("Mentra AI Student Platform test run")
    print("Modules scheduled:")
    for module in MODULES:
        print(f"- {module}")
    print("")
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
