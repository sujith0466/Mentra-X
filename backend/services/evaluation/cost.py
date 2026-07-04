from typing import Dict, Any

class CostEvaluator:
    """Evaluates token efficiency and financial cost per transaction."""
    @staticmethod
    def evaluate(response_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        tokens = int(context.get("total_tokens") or len(response_text) // 4 or 250)
        cost_usd = float(context.get("cost_usd") or (tokens * 0.000002))
        
        if tokens < 1000:
            score = 1.00
            reason = f"Highly efficient token budget ({tokens} tokens, ${cost_usd:.6f})."
        elif tokens < 4000:
            score = 0.90
            reason = f"Moderate token usage ({tokens} tokens, ${cost_usd:.6f})."
        else:
            score = 0.75
            reason = f"Heavy token consumption ({tokens} tokens, ${cost_usd:.6f})."
            
        return {
            "score": score,
            "reason": reason,
            "metadata": {"total_tokens": tokens, "cost_usd": round(cost_usd, 6)}
        }
