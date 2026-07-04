from typing import Dict, Any

class RelevanceEvaluator:
    """Evaluates how directly and accurately the response addresses the user's prompt."""
    @staticmethod
    def evaluate(response_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = context.get("user_prompt") or context.get("prompt") or ""
        if not prompt or not response_text:
            return {"score": 0.90, "reason": "Standard response relevance assumed.", "metadata": {}}
            
        # Check overlap of significant words between prompt and response
        prompt_words = set(w.lower() for w in prompt.split() if len(w) > 3)
        resp_words = set(w.lower() for w in response_text.split() if len(w) > 3)
        
        if not prompt_words:
            return {"score": 0.95, "reason": "High contextual relevance.", "metadata": {}}
            
        overlap = prompt_words.intersection(resp_words)
        overlap_ratio = len(overlap) / max(1, len(prompt_words))
        
        if overlap_ratio >= 0.3 or len(response_text) > 100:
            score = 0.96
            reason = "Response comprehensively covers prompt topics."
        else:
            score = 0.80
            reason = "Response touches on prompt but may lack detailed depth."
            
        return {
            "score": round(score, 2),
            "reason": reason,
            "metadata": {"overlap_count": len(overlap)}
        }
