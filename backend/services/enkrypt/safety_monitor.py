"""
Mentra X — Enkrypt Safety Monitor & Audit Logging (Phase 7 Layer 6)

Logs every Enkrypt validator intercept with individual pipeline scores,
manages Human-In-The-Loop (HITL) queues for hard failures, and aggregates
real-time enterprise safety metrics.
"""

import time
from typing import Dict, Any, List, Optional
from backend.services.enkrypt.dto import ValidationResultDTO


class SafetyMonitor:
    def __init__(self):
        # In-memory stores for high-speed intercept logging and HITL management
        self.intercept_logs: List[Dict[str, Any]] = []
        self.hitl_queue: List[Dict[str, Any]] = []
        self._next_intercept_id = 1
        self._next_hitl_id = 1

    def log_intercept(
        self,
        session_id: str,
        user_id: str,
        original_output: str,
        result: ValidationResultDTO,
        final_output: str,
        regeneration_count: int = 0,
        hitl_flagged: bool = False
    ) -> int:
        """
        Logs an intercept event and returns the intercept ID.
        """
        entry = {
            "id": self._next_intercept_id,
            "session_id": str(session_id),
            "user_id": str(user_id),
            "original_output": original_output,
            "math_score": result.math_score,
            "science_score": result.science_score,
            "hallucination_score": result.hallucination_score,
            "pedagogy_score": result.pedagogy_score,
            "composite_score": result.composite_confidence,
            "action_taken": result.recommended_action,
            "regeneration_count": regeneration_count,
            "final_output": final_output,
            "flagged_claims": result.flagged_claims,
            "hitl_flagged": hitl_flagged,
            "timestamp": time.time()
        }
        self.intercept_logs.append(entry)
        self._next_intercept_id += 1
        return entry["id"]

    def queue_hitl(
        self,
        session_id: str,
        user_id: str,
        concept: str,
        original_query: str,
        failed_output: str,
        scores: Dict[str, float]
    ) -> int:
        """
        Adds a hard-failed item to the Human-In-The-Loop (HITL) review queue.
        Returns the queue item ID.
        """
        entry = {
            "id": self._next_hitl_id,
            "session_id": str(session_id),
            "user_id": str(user_id),
            "concept": str(concept),
            "original_query": original_query,
            "failed_output": failed_output,
            "enkrypt_scores": scores,
            "status": "pending",  # "pending" | "reviewed" | "resolved"
            "reviewer_notes": "",
            "created_at": time.time(),
            "resolved_at": None
        }
        self.hitl_queue.append(entry)
        self._next_hitl_id += 1
        return entry["id"]

    def resolve_hitl_item(self, item_id: int, reviewer_notes: str, status: str = "resolved") -> bool:
        """
        Resolves an HITL queue item with reviewer feedback.
        """
        for item in self.hitl_queue:
            if item["id"] == int(item_id):
                item["status"] = status
                item["reviewer_notes"] = reviewer_notes
                item["resolved_at"] = time.time()
                return True
        return False

    def get_intercepts(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Returns recent intercept logs, most recent first.
        """
        return list(reversed(self.intercept_logs[-limit:]))

    def get_hitl_queue(self, status: Optional[str] = "pending") -> List[Dict[str, Any]]:
        """
        Returns HITL queue items filtered by status.
        """
        if status:
            return [item for item in self.hitl_queue if item["status"] == status]
        return list(self.hitl_queue)

    def get_metrics(self) -> Dict[str, Any]:
        """
        Calculates enterprise safety metrics across all logged intercepts.
        """
        total = len(self.intercept_logs)
        pending_hitl = sum(1 for item in self.hitl_queue if item["status"] == "pending")
        if total == 0:
            return {
                "total_intercepts": 0,
                "avg_confidence": 1.0,
                "approve_rate": 1.0,
                "regenerate_rate": 0.0,
                "hard_fail_rate": 0.0,
                "pending_hitl_count": pending_hitl,
                "validator_averages": {
                    "math": 1.0,
                    "science": 1.0,
                    "hallucination": 1.0,
                    "pedagogy": 1.0
                }
            }

        approves = sum(1 for log in self.intercept_logs if log["action_taken"] == "APPROVE")
        regens = sum(1 for log in self.intercept_logs if log["action_taken"] == "REGENERATE" or log["regeneration_count"] > 0)
        hard_fails = sum(1 for log in self.intercept_logs if log["action_taken"] == "HARD_FAIL" or log["hitl_flagged"])

        avg_conf = sum(log["composite_score"] for log in self.intercept_logs) / total
        avg_math = sum(log["math_score"] for log in self.intercept_logs) / total
        avg_sci = sum(log["science_score"] for log in self.intercept_logs) / total
        avg_hal = sum(log["hallucination_score"] for log in self.intercept_logs) / total
        avg_ped = sum(log["pedagogy_score"] for log in self.intercept_logs) / total

        pending_hitl = sum(1 for item in self.hitl_queue if item["status"] == "pending")

        return {
            "total_intercepts": total,
            "avg_confidence": round(avg_conf, 3),
            "approve_rate": round(approves / total, 3),
            "regenerate_rate": round(regens / total, 3),
            "hard_fail_rate": round(hard_fails / total, 3),
            "pending_hitl_count": pending_hitl,
            "validator_averages": {
                "math": round(avg_math, 3),
                "science": round(avg_sci, 3),
                "hallucination": round(avg_hal, 3),
                "pedagogy": round(avg_ped, 3)
            }
        }


# Global singleton instance for app-wide monitoring
safety_monitor = SafetyMonitor()
