from typing import Dict, Any

class LatencyEvaluator:
    """Evaluates execution speed against enterprise SLAs (<2000ms=1.0, <5000ms=0.85, else 0.70)."""
    @staticmethod
    def evaluate(response_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        latency_ms = float(context.get("latency_ms", 1200.0))
        
        if latency_ms < 2000.0:
            score = 1.00
            reason = f"Excellent latency ({latency_ms:.0f}ms < 2000ms SLA)."
        elif latency_ms < 5000.0:
            score = 0.85
            reason = f"Acceptable latency ({latency_ms:.0f}ms < 5000ms SLA)."
        else:
            score = 0.70
            reason = f"High latency ({latency_ms:.0f}ms > 5000ms SLA threshold)."
            
        return {
            "score": score,
            "reason": reason,
            "metadata": {"latency_ms": latency_ms}
        }
