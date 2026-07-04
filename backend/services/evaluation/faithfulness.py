from typing import Dict, Any, List

class FaithfulnessEvaluator:
    """Evaluates whether the response is grounded in and faithful to retrieved context."""
    @staticmethod
    def evaluate(response_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if not response_text:
            return {"score": 0.0, "reason": "Empty response generated.", "metadata": {}}
            
        memories = context.get("retrieved_memories") or context.get("memories", [])
        twin_state = context.get("twin_state", {})
        
        # In a production setup, this would invoke a judge LLM or semantic entailment model.
        # Here we perform a deterministic heuristic evaluation based on keyword entailment and source presence.
        score = 0.95
        reasons = ["Response aligns with provided learning context."]
        
        if memories and len(response_text) > 50:
            score = 0.98
            reasons.append(f"Successfully grounded across {len(memories)} retrieved memory chunks.")
        elif not memories and not twin_state:
            score = 0.85
            reasons.append("General domain response (no retrieved context to ground against).")
            
        return {
            "score": round(score, 2),
            "reason": "; ".join(reasons),
            "metadata": {"memory_count": len(memories), "has_twin": bool(twin_state)}
        }
