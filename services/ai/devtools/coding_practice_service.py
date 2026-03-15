from __future__ import annotations

from typing import Dict, List


PRACTICE_LIBRARY: Dict[str, Dict[str, object]] = {
    "Python": {
        "title": "Task Tracker Summary",
        "difficulty": "Easy",
        "tags": ["Python", "Dictionaries", "Counting"],
        "description": "Write a Python function that receives a list of completed study tasks and returns how many unique tasks were completed along with the most frequent task.",
        "input_example": "['variables', 'loops', 'loops', 'functions', 'loops']",
        "expected_output": "Unique tasks: 3, Most frequent: loops",
        "hints": [
            "Use a dictionary or collections.Counter to count task frequency.",
            "Track the number of unique tasks separately from the highest frequency.",
            "Return a clean summary string after processing the list.",
        ],
        "solution": "Use a frequency dictionary to count each task, compute len(counts) for unique tasks, then select the key with the maximum count and format the result.",
    },
    "Flask": {
        "title": "Course Progress Endpoint",
        "difficulty": "Medium",
        "tags": ["Flask", "Routes", "JSON API"],
        "description": "Design a Flask route that receives a course ID and returns the student's progress percentage in JSON format.",
        "input_example": "GET /api/course-progress/12",
        "expected_output": '{"course_id": 12, "progress": 78}',
        "hints": [
            "Use a route parameter for the course ID.",
            "Query the enrollment record for the logged-in user.",
            "Return jsonify with a simple payload instead of rendering HTML.",
        ],
        "solution": "Create a route like /api/course-progress/<int:course_id>, fetch the current user's enrollment for that course, and return jsonify with course_id and progress_percentage.",
    },
    "SQL": {
        "title": "Top Performing Courses",
        "difficulty": "Medium",
        "tags": ["SQL", "Aggregation", "Analytics"],
        "description": "Write a SQL query that returns the top 3 courses with the highest average quiz score.",
        "input_example": "Tables: courses, quizzes, quiz_attempts",
        "expected_output": "A result set with course title and average score ordered descending.",
        "hints": [
            "Join courses to quizzes, then quizzes to quiz_attempts.",
            "Use AVG(score_percentage) and GROUP BY course title.",
            "Apply ORDER BY average score DESC with LIMIT 3.",
        ],
        "solution": "Select course title and AVG(quiz_attempts.score_percentage), join related tables, group by course, order by average descending, and limit the result to 3 rows.",
    },
    "Algorithms": {
        "title": "Daily Revision Prioritizer",
        "difficulty": "Hard",
        "tags": ["Algorithms", "Sorting", "Scoring"],
        "description": "Create an algorithm that orders revision topics by urgency using quiz score, last access date, and completion status.",
        "input_example": "[(lesson='Loops', score=45, days_since=8, completed=False)]",
        "expected_output": "Lessons sorted from highest to lowest revision priority.",
        "hints": [
            "Define a scoring formula that rewards lower quiz scores and older access dates.",
            "Incomplete lessons should receive a strong penalty boost.",
            "Sort topics by the computed urgency score.",
        ],
        "solution": "Compute an urgency score per topic, for example (100 - score) + days_since + 20 if incomplete, then sort descending by urgency.",
    },
    "Data Structures": {
        "title": "Recent Errors Queue",
        "difficulty": "Easy",
        "tags": ["Data Structures", "Queue", "Deque"],
        "description": "Model a queue that stores the last 5 debugging errors a student submitted and removes the oldest when a new one arrives.",
        "input_example": "enqueue('TypeError'), enqueue('SyntaxError')",
        "expected_output": "A queue containing at most 5 errors in insertion order.",
        "hints": [
            "A deque with maxlen can solve this neatly in Python.",
            "Queue behavior means first-in-first-out.",
            "Focus on insert and display operations.",
        ],
        "solution": "Use collections.deque(maxlen=5) so new errors are appended and the oldest item is discarded automatically when the queue exceeds capacity.",
    },
}

SUPPORTED_TOPICS: List[str] = list(PRACTICE_LIBRARY.keys())


def generate_coding_problem(topic: str) -> Dict[str, object]:
    normalized_topic = (topic or "").strip()
    if normalized_topic not in PRACTICE_LIBRARY:
        normalized_topic = "Python"

    problem = dict(PRACTICE_LIBRARY[normalized_topic])
    problem["topic"] = normalized_topic
    problem["language"] = "SQL" if normalized_topic == "SQL" else "Python"
    return problem
