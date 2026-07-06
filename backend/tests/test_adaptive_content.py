"""
Mentra X — Unit & Integration Tests for Milestone 6.3 (Intelligent Content Selection)
Tests study material ranking by learning style, prerequisite dependency blocks,
and Qdrant outcome failure penalization.
"""

import pytest
from backend.services.adaptive.content_selector import ContentRankingEngine
from backend.services.adaptive.prerequisite_engine import PrerequisiteEngine
from backend.services.orchestration.tools.registry import ToolRegistry
from backend.services.orchestration.tools.content_tools import register_content_tools


class TestContentRankingEngine:
    def setup_method(self):
        self.engine = ContentRankingEngine()
        self.sample_resources = [
            {"id": "res_vid", "title": "Tree Visuals", "format": "video", "difficulty": 0.40},
            {"id": "res_math", "title": "Tree Proofs", "format": "formula", "difficulty": 0.45},
            {"id": "res_txt", "title": "Tree Article", "format": "article", "difficulty": 0.40}
        ]

    def test_visual_ranking_preference(self):
        dna = {"preferred_style": "Visual", "mastery_per_concept": {"trees": 0.40}}
        ranked = self.engine.rank_resources(self.sample_resources, dna, "trees")
        assert len(ranked) == 3
        # Video should rank #1 for Visual learner
        assert ranked[0].resource_id == "res_vid"
        assert "Recommended for Your Visual Style" in ranked[0].recommendation_tag

    def test_failed_resource_penalization(self):
        dna = {"preferred_style": "Visual", "mastery_per_concept": {"trees": 0.40}}
        # If res_vid failed before, it should drop down despite being visual
        ranked = self.engine.rank_resources(self.sample_resources, dna, "trees", failed_resource_ids=["res_vid"])
        assert ranked[0].resource_id != "res_vid"
        assert "Penalized" in ranked[-1].rationale


class TestPrerequisiteEngine:
    def setup_method(self):
        self.engine = PrerequisiteEngine()

    def test_prerequisite_blocked_when_low_mastery(self):
        dna = {"mastery_per_concept": {"recursion": 0.40, "arrays": 0.80}}
        res = self.engine.check_prerequisites("dynamic_programming", dna)
        assert res["allowed"] is False
        assert len(res["missing_prereqs"]) == 1
        assert res["missing_prereqs"][0]["concept"] == "recursion"
        assert "Cannot start 'dynamic_programming' yet" in res["warning_message"]

    def test_prerequisite_allowed_when_high_mastery(self):
        dna = {"mastery_per_concept": {"recursion": 0.75, "arrays": 0.85}}
        res = self.engine.check_prerequisites("dynamic_programming", dna)
        assert res["allowed"] is True
        assert len(res["missing_prereqs"]) == 0


class TestContentToolsAndRoutes:
    def test_mastra_content_tools(self):
        registry = ToolRegistry()
        registry.clear()
        register_content_tools(registry)
        
        tools = registry.get_all_tools()
        assert "rankContentForStudent" in tools
        assert "checkPrerequisites" in tools
        
        res = registry.execute_tool(
            "checkPrerequisites",
            kwargs={"target_concept": "recursion", "dna": {"mastery_per_concept": {"functions": 0.20}}}
        )
        assert res["allowed"] is False

    @pytest.fixture
    def client(self):
        from backend.app import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_rank_route(self, client):
        payload = {
            "resources": [{"id": "r1", "title": "Vid", "format": "video", "difficulty": 0.5}],
            "dna": {"preferred_style": "Visual"}
        }
        resp = client.post('/api/v1/adaptive/content/rank', json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert data["ranked_resources"][0]["resource_id"] == "r1"

    def test_check_prereqs_route(self, client):
        payload = {"target_concept": "dynamic_programming", "dna": {"mastery_per_concept": {"recursion": 0.10}}}
        resp = client.post('/api/v1/adaptive/prerequisites/check', json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert data["prerequisite_check"]["allowed"] is False
