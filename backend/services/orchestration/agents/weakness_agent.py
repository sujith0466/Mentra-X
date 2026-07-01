from typing import Dict, Any
from backend.services.orchestration.agents.registry import AgentBase, AgentMetadata
from backend.services.orchestration.prompts.registry import PromptRegistry
from backend.services.orchestration.providers.mock_provider import MockProvider
import json

class WeaknessAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.metadata = AgentMetadata(
            name="WeaknessAgent",
            description="Continuously scan Digital Twin and Assessment logs for struggling concepts.",
            version="1.0.0",
            enabled=True,
            priority=5,
            allowed_tools=["get_digital_twin"],
            allowed_collections=[],
            max_tokens=2048,
            temperature=0.1,
            timeout_ms=5000,
            retry_count=3
        )
        self.capabilities = ["weakness_detection"]
        self.execution_policy = "asynchronous"
        self.retry_policy = "exponential_backoff"
        self.max_iterations = 1

    def health_check(self) -> bool:
        return True

    def can_handle(self, query: str) -> bool:
        return "weakness" in query.lower() or "struggling" in query.lower()

    def validate_input(self, unified_context: Dict[str, Any], query: str) -> bool:
        return True

    def validate_output(self, response: Dict[str, Any]) -> bool:
        return "detected_weaknesses" in response

    def execute(self, unified_context: Dict[str, Any], query: str) -> Dict[str, Any]:
        if not self.validate_input(unified_context, query):
            raise ValueError("Invalid input")
            
        prompt = PromptRegistry().get_prompt(self.metadata.name)
        provider = MockProvider()
        
        provider_result = provider.generate(
            prompt=prompt,
            context=unified_context,
            query=query,
            allowed_tools=self.metadata.allowed_tools
        )
        
        try:
            parsed = json.loads(provider_result["response"])
        except:
            parsed = {"detected_weaknesses": provider_result["response"]}
            
        response = {
            "detected_weaknesses": parsed.get("detected_weaknesses", []),
            "tools_used": provider_result["tools_used"],
            "telemetry": provider_result["telemetry"]
        }
        
        if not self.validate_output(response):
            raise ValueError("Invalid output")
            
        return response
