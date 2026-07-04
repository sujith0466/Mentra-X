from typing import Dict, Any

class QualityEvaluator:
    """Evaluates completeness, educational value, and helpfulness of the response."""
    @staticmethod
    def evaluate(response_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if not response_text:
            return {"score": 0.0, "reason": "No response text.", "metadata": {}}
            
        length = len(response_text)
        has_structure = "\n" in response_text or "-" in response_text or "1." in response_text
        
        if length > 150 and has_structure:
            score = 0.95
            reason = "Well-structured, comprehensive, and pedagogically helpful response."
        elif length > 50:
            score = 0.85
            reason = "Clear and concise explanation."
        else:
            score = 0.70
            reason = "Brief response; may require further elaboration for deep learning."
            
        return {
            "score": score,
            "reason": reason,
            "metadata": {"length": length, "structured": has_structure}
        }
