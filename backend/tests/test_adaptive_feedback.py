"""
Mentra X — Unit & Integration Tests for Milestone 6.4 (Real-Time Adaptive Feedback)
Tests progressive hint ladders, Socratic guiding feedback, and tool/API bindings.
"""

import pytest
from backend.services.adaptive.feedback_engine import ProgressiveHintEngine, SocraticFeedbackEngine
from backend.services.orchestration.tools.registry import ToolRegistry
from backend.services.orchestration.tools.feedback_tools import register_feedback_tools


class TestProgressiveHintEngine:
    def setup_method(self):
        self.engine = ProgressiveHintEngine()

    def test_hint_ladder_progression(self):
        h1 = self.engine.get_hint("stack_memory", 0)
        assert h1.hint_level == 1
        assert h1.hint_type == "CONCEPTUAL_NUDGE"
        assert h1.remaining_hints == 3
        assert "key property" in h1.hint_text

        h2 = self.engine.get_hint("stack_memory", 1)
        assert h2.hint_level == 2
        assert h2.hint_type == "STRUCTURAL_FRAMEWORK"
        assert h2.remaining_hints == 2

        h4 = self.engine.get_hint("stack_memory", 3)
        assert h4.hint_level == 4
        assert h4.hint_type == "WALKTHROUGH"
        assert h4.remaining_hints == 0


class TestSocraticFeedbackEngine:
    def setup_method(self):
        self.engine = SocraticFeedbackEngine()

    def test_socratic_on_error(self):
        res = self.engine.generate_socratic_feedback(
            concept="binary_search",
            student_answer="O(n)",
            expected_concept_rule="we divide the search space in half at each step",
            is_correct=False
        )
        assert res.is_correct is False
        assert "O(n)" in res.socratic_question
        assert "divide the search space in half" in res.socratic_question
        assert "tracing your answer step-by-step" in res.reflective_prompt

    def test_socratic_on_correct(self):
        res = self.engine.generate_socratic_feedback("binary_search", "O(log n)", is_correct=True)
        assert res.is_correct is True
        assert "Why do you think this solution works so efficiently" in res.socratic_question


class TestFeedbackToolsAndRoutes:
    def test_mastra_feedback_tools(self):
        registry = ToolRegistry()
        registry.clear()
        register_feedback_tools(registry)
        
        tools = registry.get_all_tools()
        assert "generateProgressiveHint" in tools
        assert "formulateSocraticQuestion" in tools
        
        hint = registry.execute_tool("generateProgressiveHint", kwargs={"concept": "recursion", "current_hint_index": 0})
        assert hint["hint_level"] == 1
        assert hint["hint_type"] == "CONCEPTUAL_NUDGE"

    @pytest.fixture
    def client(self):
        from backend.app import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_hint_route(self, client):
        payload = {"concept": "recursion", "current_hint_index": 2}
        resp = client.post('/api/v1/adaptive/hint', json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert data["hint"]["hint_level"] == 3

    def test_socratic_route(self, client):
        payload = {"concept": "sorting", "student_answer": "bubble sort is fastest", "is_correct": False}
        resp = client.post('/api/v1/adaptive/socratic', json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert data["socratic_feedback"]["is_correct"] is False
