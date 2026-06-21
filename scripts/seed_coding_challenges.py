from __future__ import annotations

import json

from app import app
from models import CodingChallenge, db


SEED_CHALLENGES = [
    {
        "title": "Print Welcome Message",
        "description": "Write a function that returns the text Welcome to Mentra.",
        "difficulty": "Beginner",
        "topic": "Python Basics",
        "starter_code": "def welcome_message():\n    pass",
        "expected_output": "Welcome to Mentra",
        "test_cases_json": [
            {"input": "", "output": "'Welcome to Mentra'"}
        ],
    },
    {
        "title": "Square a Number",
        "description": "Create a function that returns the square of a given integer.",
        "difficulty": "Beginner",
        "topic": "Functions",
        "starter_code": "def square_number(value):\n    pass",
        "expected_output": "25",
        "test_cases_json": [
            {"input": "5", "output": "25"},
            {"input": "-4", "output": "16"}
        ],
    },
    {
        "title": "Two Sum",
        "description": "Given an array of integers, return indices of the two numbers that add up to a target.",
        "difficulty": "Beginner",
        "topic": "Algorithms",
        "starter_code": "def two_sum(nums, target):\n    pass",
        "expected_output": "[0, 1]",
        "test_cases_json": [
            {"input": "[2,7,11,15],9", "output": "[0,1]"},
            {"input": "[3,2,4],6", "output": "[1,2]"}
        ],
    },
    {
        "title": "Reverse Queue",
        "description": "Return a reversed copy of the incoming list.",
        "difficulty": "Intermediate",
        "topic": "Data Structures",
        "starter_code": "def reverse_queue(items):\n    pass",
        "expected_output": "[3, 2, 1]",
        "test_cases_json": [
            {"input": "[1,2,3]", "output": "[3,2,1]"},
            {"input": "['a','b']", "output": "['b','a']"}
        ],
    },
    {
        "title": "Count Students By Course",
        "description": "Return an SQL query that counts students grouped by course_id from the enrollments table.",
        "difficulty": "Beginner",
        "topic": "SQL Queries",
        "starter_code": "SELECT course_id, COUNT(*) AS student_count\nFROM enrollments\nGROUP BY course_id;",
        "expected_output": "SELECT course_id, COUNT(*) AS student_count FROM enrollments GROUP BY course_id;",
        "test_cases_json": [
            {"input": "", "output": "'Use SQL editor review only'"}
        ],
    },
]


def seed_challenges() -> int:
    created = 0
    with app.app_context():
        for payload in SEED_CHALLENGES:
            existing = CodingChallenge.query.filter_by(title=payload["title"]).first()
            if existing:
                continue
            challenge = CodingChallenge(
                title=payload["title"],
                description=payload["description"],
                difficulty=payload["difficulty"],
                topic=payload["topic"],
                starter_code=payload["starter_code"],
                expected_output=payload["expected_output"],
                test_cases_json=json.dumps(payload["test_cases_json"]),
            )
            db.session.add(challenge)
            created += 1
        db.session.commit()
    return created


if __name__ == "__main__":
    inserted = seed_challenges()
    print(f"Seeded {inserted} coding challenges.")
