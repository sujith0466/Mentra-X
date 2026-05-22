"""
AI Doubt Solver Service (Feature 10 - Phase C)

Provides fast, rule-based explanations for common technical doubts.
"""

from __future__ import annotations


def _topic_payload() -> dict:
    return {
        'loops': {
            'answer': 'Loops repeat code automatically until a condition is met. Use for-loops when iteration count is known and while-loops when it depends on a condition.',
            'example': 'for i in range(5):\n    print(i)'
        },
        'functions': {
            'answer': 'Functions are reusable blocks of code that accept inputs and return outputs. They help reduce duplication and improve readability.',
            'example': 'def add(a, b):\n    return a + b'
        },
        'arrays': {
            'answer': 'Arrays/lists store ordered values. You can access items by index, usually starting from 0.',
            'example': 'nums = [10, 20, 30]\nprint(nums[0])  # 10'
        },
        'oop': {
            'answer': 'Object-Oriented Programming (OOP) models logic using classes and objects. It supports encapsulation, inheritance, and polymorphism.',
            'example': 'class Student:\n    def __init__(self, name):\n        self.name = name'
        },
        'sql': {
            'answer': 'SQL is used to query relational databases. Common commands include SELECT, INSERT, UPDATE, and DELETE.',
            'example': 'SELECT name FROM users WHERE id = 1;'
        },
    }


def _detect_topic(question: str) -> str:
    lowered = (question or '').lower()

    if any(k in lowered for k in ['for loop', 'while loop', 'loop', 'loops', 'iterate', 'iteration']):
        return 'loops'
    if any(k in lowered for k in ['function', 'functions', 'method', 'parameter', 'return']):
        return 'functions'
    if any(k in lowered for k in ['array', 'arrays', 'list', 'lists', 'index', 'indices']):
        return 'arrays'
    if any(k in lowered for k in ['oop', 'object oriented', 'class', 'object', 'inheritance', 'polymorphism']):
        return 'oop'
    if any(k in lowered for k in ['sql', 'query', 'database', 'table', 'join', 'select']):
        return 'sql'
    return 'general'


def solve_doubt(question_text: str) -> dict:
    """
    Detect topic and return a structured explanation.

    Returns:
      {
        "topic": "loops|functions|arrays|oop|sql|general",
        "answer": "...",
        "example": "...",
        "explanation": "..."  # backward-compatible alias
      }
    """
    question = (question_text or '').strip()
    if not question:
        answer = 'Please ask a specific doubt so I can give a focused explanation.'
        return {
            'topic': 'general',
            'answer': answer,
            'example': 'Example: What is the difference between for-loop and while-loop?',
            'explanation': answer,
        }

    topics = _topic_payload()
    detected = _detect_topic(question)

    if detected in topics:
        payload = topics[detected]
        return {
            'topic': detected,
            'answer': payload['answer'],
            'example': payload['example'],
            'explanation': payload['answer'],
        }

    fallback = (
        'That is a good question. Break it into smaller parts: concept, syntax, and example. '
        'Then validate with a small code snippet or practice problem.'
    )
    return {
        'topic': 'general',
        'answer': fallback,
        'example': 'Try: Explain one example input and expected output for your doubt.',
        'explanation': fallback,
    }
