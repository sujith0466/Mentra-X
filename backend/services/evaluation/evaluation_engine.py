import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from .faithfulness import FaithfulnessEvaluator
from .hallucination import HallucinationEvaluator
from .relevance import RelevanceEvaluator
from .latency import LatencyEvaluator
from .cost import CostEvaluator
from .quality import QualityEvaluator
from .safety import SafetyEvaluator

logger = logging.getLogger(__name__)

class EvaluationResult:
    def __init__(self, workflow_id: str, results: Dict[str, Dict[str, Any]], overall_score: float):
        self.workflow_id = workflow_id
        self.results = results
        self.overall_score = round(overall_score, 2)
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "overall_score": self.overall_score,
            "metrics": self.results,
            "timestamp": self.timestamp
        }


class EvaluationEngine:
    """
    Central Evaluation Engine executing modular evaluation plugins against LLM responses.
    Evaluates faithfulness, hallucination, relevance, safety, latency, cost, and quality.
    """
    PLUGINS = {
        "faithfulness": FaithfulnessEvaluator,
        "hallucination": HallucinationEvaluator,
        "relevance": RelevanceEvaluator,
        "latency": LatencyEvaluator,
        "cost": CostEvaluator,
        "quality": QualityEvaluator,
        "safety": SafetyEvaluator,
    }

    @classmethod
    def evaluate_response(
        cls,
        workflow_id: str,
        response_text: str,
        context: Dict[str, Any],
        persist: bool = True
    ) -> EvaluationResult:
        results = {}
        total_score = 0.0
        count = 0

        for metric_name, plugin in cls.PLUGINS.items():
            try:
                res = plugin.evaluate(response_text, context)
                score = float(res.get("score", 0.0))
                results[metric_name] = {
                    "score": round(score, 2),
                    "reason": res.get("reason", ""),
                    "metadata": res.get("metadata", {})
                }
                total_score += score
                count += 1
            except Exception as e:
                logger.error(f"Error executing evaluator plugin {metric_name}: {e}")
                results[metric_name] = {"score": 0.0, "reason": f"Plugin error: {e}", "metadata": {}}

        overall = total_score / max(1, count)
        eval_result = EvaluationResult(workflow_id, results, overall)

        if persist:
            cls._persist_results(workflow_id, results, context)
            cls._update_prompt_analytics(context, overall, results)

        return eval_result

    @classmethod
    def get_evaluations(cls, workflow_id: str) -> List[Dict[str, Any]]:
        try:
            from backend.models import EvaluationRecord
            records = EvaluationRecord.query.filter_by(workflow_id=workflow_id).all()
            return [
                {
                    "evaluation_type": r.evaluation_type,
                    "score": r.score,
                    "reason": r.reason,
                    "metadata": r.metadata_json,
                    "provider": r.provider,
                    "prompt_version": r.prompt_version,
                    "created_at": r.created_at.isoformat() if r.created_at else None
                }
                for r in records
            ]
        except Exception as e:
            logger.error(f"Error querying EvaluationRecord for {workflow_id}: {e}")
            return []

    @classmethod
    def _persist_results(cls, workflow_id: str, results: Dict[str, Dict[str, Any]], context: Dict[str, Any]):
        try:
            from backend.models import db, EvaluationRecord
            provider = context.get("provider", "MastraProvider")
            prompt_ver = context.get("prompt_version", "1.0.0")
            
            for m_type, m_data in results.items():
                rec = EvaluationRecord(
                    workflow_id=workflow_id,
                    evaluation_type=m_type,
                    score=m_data["score"],
                    reason=m_data["reason"],
                    metadata_json=m_data["metadata"],
                    provider=provider,
                    prompt_version=prompt_ver
                )
                db.session.add(rec)
            db.session.commit()
        except Exception as e:
            logger.error(f"Failed to persist EvaluationRecords for {workflow_id}: {e}")
            try:
                from backend.models import db
                db.session.rollback()
            except Exception:
                pass

    @classmethod
    def _update_prompt_analytics(cls, context: Dict[str, Any], overall_score: float, results: Dict[str, Dict[str, Any]]):
        prompt_id = context.get("prompt_id")
        prompt_ver = context.get("prompt_version", "1.0.0")
        if not prompt_id:
            return
        try:
            from backend.services.orchestration.prompt_repository import PromptRepository
            latency = float(context.get("latency_ms", 1200.0))
            tokens = int(context.get("total_tokens", 250))
            cost = float(context.get("cost_usd", tokens * 0.000002))
            success = 1.0 if results.get("safety", {}).get("score", 1.0) > 0.0 else 0.0
            PromptRepository.record_eval_analytics(prompt_id, prompt_ver, overall_score, latency, tokens, cost, success)
        except Exception as e:
            logger.debug(f"Prompt analytics update skipped: {e}")
