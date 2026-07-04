from typing import Dict, Any

class HallucinationEvaluator:
    """Evaluates the likelihood of ungrounded or fabricated factual claims (0.0 = high hallucination, 1.0 = zero hallucination)."""
    @staticmethod
    def evaluate(response_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if not response_text:
            return {"score": 0.0, "reason": "No response text to evaluate.", "metadata": {}}
            
        # Check for known hallucination indicators or speculative phrases
        speculative_phrases = ["i guess", "probably", "i am not sure but", "might be invented", "fictional fact"]
        lower_resp = response_text.lower()
        
        penalties = 0.0
        found_phrases = []
        for phrase in speculative_phrases:
            if phrase in lower_resp:
                penalties += 0.2
                found_phrases.append(phrase)
                
        score = max(0.0, 1.0 - penalties)
        if penalties == 0.0:
            reason = "No ungrounded speculative assertions detected."
        else:
            reason = f"Detected speculative phrasing lowering certainty: {', '.join(found_phrases)}."
            
        return {
            "score": round(score, 2),
            "reason": reason,
            "metadata": {"speculative_phrases": found_phrases}
        }
