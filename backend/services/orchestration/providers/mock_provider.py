import time
import hashlib
from typing import Dict, Any
from backend.services.orchestration.providers.llm_provider import LLMProvider

class MockProvider(LLMProvider):
    """
    Mock LLM Provider for unit testing and deterministic execution.
    """
    def __init__(self, default_response: str = "Simulated response"):
        self.default_response = default_response

    def generate(self, prompt: str, context: Dict[str, Any], query: str, **kwargs) -> Dict[str, Any]:
        start_time = time.time()
        
        # Simulate network delay
        time.sleep(0.01)
        
        prompt_hash = hashlib.sha256(prompt.encode('utf-8')).hexdigest()
        
        # Simple mock matching based on prompt content
        response_text = self.default_response
        is_safe = True
        
        if "Verification" in prompt:
            response_text = '{"is_safe": true, "reason": "Passed mock checks."}'
        elif "Assessment" in prompt:
            response_text = '{"assessment_result": "Started session for Python", "tools_used": ["start_assessment_session"]}'
        elif "Memory" in prompt:
            response_text = '{"memory_context": "Found relevant past session on loops.", "tools_used": ["retrieve_semantic_memory"]}'
        elif "Insight" in prompt:
            response_text = '{"insight": "You\'ve been struggling with loops. Consider taking a break."}'
        elif "Weakness" in prompt:
            response_text = '{"detected_weaknesses": ["Loops", "Recursion"]}'
        elif "Tutor" in prompt:
            response_text = f"Simulated tutoring response for: {query}"
            
        latency = (time.time() - start_time) * 1000
        
        return {
            "response": response_text,
            "tools_used": kwargs.get("allowed_tools", []),
            "telemetry": {
                "model_name": "mock-model-v1",
                "provider": "MockProvider",
                "prompt_version": "1.0",
                "prompt_hash": prompt_hash,
                "token_usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
                "latency_ms": latency,
                "execution_cost": 0.0
            }
        }
