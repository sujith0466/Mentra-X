from typing import Dict, Any
from backend.services.orchestration.agents.registry import AgentBase, AgentMetadata
from backend.services.orchestration.prompts.registry import PromptRegistry
from backend.services.orchestration.providers.mock_provider import MockProvider
import json

class InsightAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.metadata = AgentMetadata(
            name="InsightAgent",
            description="Generate high-level learning insights and recommendations.",
            version="1.0.0",
            enabled=True,
            priority=4,
            allowed_tools=[],
            allowed_collections=[],
            max_tokens=1500,
            temperature=0.4,
            timeout_ms=6000,
            retry_count=1
        )
        self.capabilities = ["insight_generation"]
        self.execution_policy = "asynchronous"
        self.retry_policy = "exponential_backoff"
        self.max_iterations = 1

    def health_check(self) -> bool:
        return True

    def can_handle(self, query: str) -> bool:
        return "insight" in query.lower() or "summary" in query.lower()

    def validate_input(self, unified_context: Dict[str, Any], query: str) -> bool:
        return True

    def validate_output(self, response: Dict[str, Any]) -> bool:
        return "insight" in response

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
            parsed = {"insight": provider_result["response"]}
            
        response = {
            "insight": parsed.get("insight", ""),
            "tools_used": provider_result["tools_used"],
            "telemetry": provider_result["telemetry"]
        }
        
        if not self.validate_output(response):
            raise ValueError("Invalid output")
            
        return response
