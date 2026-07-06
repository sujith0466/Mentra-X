"""
Mentra X — End-to-End Integration & Regression Tests for Phase 7 (Enkrypt Safety Layer)
Verifies the full lifecycle of AI tutor generation, safety validation, automated regeneration,
enterprise audit monitoring, and Human-In-The-Loop (HITL) resolution across Mastra and REST layers.
"""

import pytest
from flask import json
from backend.app import app
from backend.services.orchestration.tools import register_all_tools
from backend.services.enkrypt.safety_monitor import safety_monitor


class TestEnkryptE2EIntegration:
    def setup_method(self):
        self.registry = register_all_tools()
        self.client = app.test_client()
        safety_monitor.intercept_logs.clear()
        safety_monitor.hitl_queue.clear()

    def test_full_enkrypt_lifecycle(self):
        # 1. Valid Tutor Explanation via Mastra Tool
        val_tool = self.registry.get_tool("callEnkryptValidation")
        res_valid = val_tool["func"](
            text="According to Einstein's relativity, mass-energy equivalence is given by E = m*c^2.",
            subject="physics",
            level=1,
            exam_track="JEE",
            session_id="e2e_session_1",
            user_id="student_101"
        )
        assert res_valid["recommended_action"] == "APPROVE"
        assert res_valid["composite_confidence"] >= 0.90
        assert len(safety_monitor.get_intercepts()) == 1

        # 2. Hard Failure & HITL Queueing via REST API
        resp_fail = self.client.post(
            "/api/safety/evaluate",
            data=json.dumps({
                "text": "According to Newton's fourth law of thermodynamics, entropy always increases in reversible cycles and F = m*v.",
                "subject": "physics",
                "exam_track": "JEE",
                "session_id": "e2e_session_2",
                "user_id": "student_102"
            }),
            content_type="application/json"
        )
        assert resp_fail.status_code == 200
        data_fail = json.loads(resp_fail.data)
        assert data_fail["validation_result"]["recommended_action"] == "HARD_FAIL"
        
        # Verify HITL Queue populated
        resp_q = self.client.get("/api/safety/hitl_queue?status=pending")
        data_q = json.loads(resp_q.data)
        assert len(data_q["hitl_queue"]) == 1
        hitl_id = data_q["hitl_queue"][0]["id"]

        # 3. Automated Regeneration via Mastra Tool
        regen_tool = self.registry.get_tool("executeRegenerationLoop")
        res_regen = regen_tool["func"](
            original_output="The car travels at 50 km/h and accelerates at 2 m/s directly without converting units.",
            concept="kinematics",
            exam_track="JEE",
            subject="physics",
            session_id="e2e_session_3",
            user_id="student_103"
        )
        assert res_regen["attempts_used"] == 1
        assert res_regen["hitl_flagged"] is False
        assert "Enkrypt Verified after refinement" in res_regen["final_output"]

        # 4. Enterprise Audit Metrics Verification
        resp_m = self.client.get("/api/safety/metrics")
        data_m = json.loads(resp_m.data)["metrics"]
        assert data_m["total_intercepts"] == 3
        assert data_m["pending_hitl_count"] == 1

        # 5. HITL Resolution via Admin API
        resp_res = self.client.post(
            f"/api/safety/hitl_resolve/{hitl_id}",
            data=json.dumps({"reviewer_notes": "Corrected formula in tutor prompt.", "status": "resolved"}),
            content_type="application/json"
        )
        assert resp_res.status_code == 200
        assert json.loads(resp_res.data)["status"] == "success"

        # Verify HITL Queue is cleared of pending items
        resp_q2 = self.client.get("/api/safety/hitl_queue?status=pending")
        data_q2 = json.loads(resp_q2.data)
        assert len(data_q2["hitl_queue"]) == 0

        # Verify updated metrics
        resp_m2 = self.client.get("/api/safety/metrics")
        data_m2 = json.loads(resp_m2.data)["metrics"]
        assert data_m2["pending_hitl_count"] == 0
