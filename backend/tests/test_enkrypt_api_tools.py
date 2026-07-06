"""
Mentra X — Unit & Integration Tests for Milestone 7.4 (Mastra Swarm Integration & REST API Routing)
Tests tool registration, tool execution, and Flask REST endpoints for the Enkrypt Safety Layer.
"""

import pytest
from flask import json
from backend.app import app
from backend.services.orchestration.tools import register_all_tools, ToolRegistry


class TestMastraSafetyTools:
    def setup_method(self):
        self.registry = register_all_tools()

    def test_tools_registered(self):
        assert self.registry.get_tool("callEnkryptValidation") is not None
        assert self.registry.get_tool("executeRegenerationLoop") is not None

    def test_call_enkrypt_validation_tool(self):
        tool = self.registry.get_tool("callEnkryptValidation")
        res = tool["func"](
            text="In Einstein's relativity, E = m*c^2 is valid.",
            subject="physics",
            level=1,
            exam_track="JEE"
        )
        assert res["composite_confidence"] == 1.0
        assert res["recommended_action"] == "APPROVE"

    def test_execute_regeneration_loop_tool(self):
        tool = self.registry.get_tool("executeRegenerationLoop")
        res = tool["func"](
            original_output="According to Newton's fourth law of thermodynamics, entropy always increases in reversible cycles and F = m*v.",
            concept="thermodynamics",
            exam_track="JEE",
            subject="physics"
        )
        assert res["attempts_used"] == 1
        assert "final_output" in res
        assert res["hitl_flagged"] is False
        assert "Enkrypt Verified after refinement" in res["final_output"]


class TestSafetyRestRoutes:
    def setup_method(self):
        self.client = app.test_client()

    def test_evaluate_endpoint(self):
        resp = self.client.post(
            "/api/safety/evaluate",
            data=json.dumps({"text": "Force is F = m*a.", "subject": "physics", "exam_track": "JEE"}),
            content_type="application/json"
        )
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["status"] == "success"
        assert data["validation_result"]["recommended_action"] == "APPROVE"

    def test_metrics_and_intercepts_endpoints(self):
        resp_m = self.client.get("/api/safety/metrics")
        assert resp_m.status_code == 200
        data_m = json.loads(resp_m.data)
        assert "metrics" in data_m
        assert "avg_confidence" in data_m["metrics"]

        resp_i = self.client.get("/api/safety/intercepts?limit=10")
        assert resp_i.status_code == 200
        data_i = json.loads(resp_i.data)
        assert "intercepts" in data_i
        assert isinstance(data_i["intercepts"], list)

    def test_hitl_queue_and_resolve_endpoints(self):
        # Trigger an evaluation that hard fails to populate HITL queue
        self.client.post(
            "/api/safety/evaluate",
            data=json.dumps({
                "text": "According to Newton's fourth law of thermodynamics, entropy always increases in reversible cycles and F = m*v.",
                "subject": "physics"
            }),
            content_type="application/json"
        )

        resp_q = self.client.get("/api/safety/hitl_queue?status=pending")
        assert resp_q.status_code == 200
        data_q = json.loads(resp_q.data)
        assert len(data_q["hitl_queue"]) >= 1

        item_id = data_q["hitl_queue"][0]["id"]
        resp_r = self.client.post(
            f"/api/safety/hitl_resolve/{item_id}",
            data=json.dumps({"reviewer_notes": "Resolved via admin panel.", "status": "resolved"}),
            content_type="application/json"
        )
        assert resp_r.status_code == 200
        data_r = json.loads(resp_r.data)
        assert data_r["status"] == "success"
