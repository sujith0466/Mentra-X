"""
Mentra X — Unit & Integration Tests for Milestone 7.3 (Safety Monitoring, Audit Logging & HITL Queue)
Tests intercept event recording, enterprise metric calculations, and HITL workflow resolution.
"""

import pytest
from backend.services.enkrypt.safety_monitor import SafetyMonitor
from backend.services.enkrypt.dto import ValidationResultDTO


class TestSafetyMonitor:
    def setup_method(self):
        self.monitor = SafetyMonitor()

    def test_log_intercept_and_metrics(self):
        val_pass = ValidationResultDTO(
            math_score=1.0, science_score=1.0, hallucination_score=1.0, pedagogy_score=1.0,
            composite_confidence=1.0, flagged_claims=[], recommended_action="APPROVE"
        )
        val_fail = ValidationResultDTO(
            math_score=0.4, science_score=0.5, hallucination_score=0.3, pedagogy_score=0.8,
            composite_confidence=0.45, flagged_claims=["Error 1"], recommended_action="HARD_FAIL"
        )

        id1 = self.monitor.log_intercept("sess_1", "usr_1", "Good output", val_pass, "Good output", 0, False)
        id2 = self.monitor.log_intercept("sess_2", "usr_2", "Bad output", val_fail, "Fallback text", 2, True)

        assert id1 == 1
        assert id2 == 2

        metrics = self.monitor.get_metrics()
        assert metrics["total_intercepts"] == 2
        assert metrics["approve_rate"] == 0.5
        assert metrics["hard_fail_rate"] == 0.5
        assert metrics["avg_confidence"] == 0.725

        logs = self.monitor.get_intercepts(limit=10)
        assert len(logs) == 2
        assert logs[0]["id"] == 2  # Most recent first

    def test_queue_hitl_and_resolve(self):
        q_id = self.monitor.queue_hitl(
            session_id="sess_err",
            user_id="usr_err",
            concept="thermodynamics",
            original_query="Explain dS = Q/T",
            failed_output="Wrong formula text",
            scores={"math": 0.4, "science": 0.5, "composite": 0.45}
        )

        pending = self.monitor.get_hitl_queue(status="pending")
        assert len(pending) == 1
        assert pending[0]["id"] == q_id
        assert self.monitor.get_metrics()["pending_hitl_count"] == 1

        resolved = self.monitor.resolve_hitl_item(q_id, reviewer_notes="Verified against NCERT chapter 12. Adjusted prompt rules.")
        assert resolved is True

        pending_after = self.monitor.get_hitl_queue(status="pending")
        assert len(pending_after) == 0
        resolved_list = self.monitor.get_hitl_queue(status="resolved")
        assert len(resolved_list) == 1
        assert "NCERT chapter 12" in resolved_list[0]["reviewer_notes"]
