"""
Mentra X — Unit & Integration Tests for Milestone 6.5 (Adaptive Pacing & Review)
Tests cognitive fatigue triggers, Ebbinghaus spaced repetition review scheduling,
and tool/API bindings.
"""

import pytest
from backend.services.adaptive.pacing_engine import FatigueDetector, SpacedRepetitionScheduler
from backend.services.orchestration.tools.registry import ToolRegistry
from backend.services.orchestration.tools.pacing_tools import register_pacing_tools


class TestFatigueDetector:
    def setup_method(self):
        self.detector = FatigueDetector()

    def test_no_fatigue(self):
        res = self.detector.evaluate_fatigue(session_duration_mins=25.0, recent_errors=1, response_time_degradation_pct=5.0)
        assert res.is_fatigued is False
        assert res.fatigue_level == "NONE"
        assert res.recommended_action == "CONTINUE"

    def test_critical_fatigue(self):
        res = self.detector.evaluate_fatigue(session_duration_mins=130.0, recent_errors=6, response_time_degradation_pct=80.0)
        assert res.is_fatigued is True
        assert res.fatigue_level == "CRITICAL"
        assert res.recommended_action == "MANDATORY_BREAK"
        assert "burnout" in res.rationale


class TestSpacedRepetitionScheduler:
    def setup_method(self):
        self.scheduler = SpacedRepetitionScheduler()

    def test_ebbinghaus_stable_memory(self):
        # Recently learned with high mastery
        res = self.scheduler.calculate_review_schedule(concept="hash_tables", hours_since_last_review=5.0, initial_mastery=0.90)
        assert res.needs_immediate_review is False
        assert res.urgency == "LOW"
        assert res.current_retention > 0.80

    def test_ebbinghaus_decayed_memory(self):
        # Long time since review or low initial mastery
        res = self.scheduler.calculate_review_schedule(concept="hash_tables", hours_since_last_review=200.0, initial_mastery=0.50)
        assert res.needs_immediate_review is True
        assert res.urgency in ("HIGH", "OVERDUE")
        assert res.current_retention <= 0.70


class TestPacingToolsAndRoutes:
    def test_mastra_pacing_tools(self):
        registry = ToolRegistry()
        registry.clear()
        register_pacing_tools(registry)
        
        tools = registry.get_all_tools()
        assert "detectStudentFatigue" in tools
        assert "scheduleSpacedReview" in tools
        
        fatigue = registry.execute_tool("detectStudentFatigue", kwargs={"session_duration_mins": 90, "recent_errors": 4})
        assert fatigue["is_fatigued"] is True

    @pytest.fixture
    def client(self):
        from backend.app import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_fatigue_route(self, client):
        payload = {"session_duration_mins": 45, "recent_errors": 3}
        resp = client.post('/api/v1/adaptive/pace/fatigue', json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert data["fatigue"]["fatigue_level"] in ("MODERATE", "HIGH")

    def test_schedule_route(self, client):
        payload = {"concept": "recursion", "hours_since_last_review": 150, "initial_mastery": 0.60}
        resp = client.post('/api/v1/adaptive/pace/schedule', json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert "current_retention" in data["review_schedule"]
