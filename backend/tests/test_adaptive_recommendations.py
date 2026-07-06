"""
Mentra X — Unit & Integration Tests for Milestone 6.6 (Unified Recommendation Engine)
Tests multi-service aggregation, priority ranking rules, and < 200ms latency compliance.
"""

import pytest
import time
from backend.services.adaptive.recommendation_engine import UnifiedRecommendationEngine
from backend.services.orchestration.tools.registry import ToolRegistry
from backend.services.orchestration.tools.recommendation_tools import register_recommendation_tools


class TestUnifiedRecommendationEngine:
    def setup_method(self):
        self.engine = UnifiedRecommendationEngine()

    def test_latency_and_priority(self):
        start = time.time()
        feed = self.engine.generate_feed(
            user_id="usr_test_rec",
            concept="recursion",
            dna={"preferred_style": "Visual", "mastery_per_concept": {"recursion": 0.40}},
            session_duration_mins=95.0, # Will trigger fatigue
            recent_errors=3,
            lessons=[{"id": 10, "title": "Recursion Basics", "concept": "recursion", "order": 1}],
            resources=[{"id": "res_1", "title": "Recursion Vid", "format": "video", "difficulty": 0.4}],
            review_concepts=[{"concept": "hash_tables", "hours_since": 250, "mastery": 0.50}] # Will trigger review
        )
        duration_ms = (time.time() - start) * 1000.0
        
        assert feed.execution_time_ms < 200.0
        assert duration_ms < 500.0  # Overall test safety margin
        assert feed.is_fatigued is True
        assert len(feed.recommendations) >= 3
        
        # #1 Priority should be FATIGUE_INTERVENTION (score 850 or 1000)
        assert feed.recommendations[0].action_type == "FATIGUE_INTERVENTION"
        # #2 Priority should be SPACED_REVIEW (score 750 or 900)
        assert feed.recommendations[1].action_type == "SPACED_REVIEW"


class TestRecommendationToolsAndRoutes:
    def test_mastra_recommendation_tools(self):
        registry = ToolRegistry()
        registry.clear()
        register_recommendation_tools(registry)
        
        tools = registry.get_all_tools()
        assert "getUnifiedRecommendations" in tools
        
        res = registry.execute_tool("getUnifiedRecommendations", kwargs={"user_id": "usr_api"})
        assert "recommendations" in res
        assert res["execution_time_ms"] < 200.0

    @pytest.fixture
    def client(self):
        from backend.app import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_recommendation_route(self, client):
        payload = {"user_id": "usr_api", "concept": "loops"}
        resp = client.post('/api/v1/adaptive/recommendations', json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert "recommendation_feed" in data
