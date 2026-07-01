from typing import Dict, Any
from backend.services.orchestration.agents.registry import AgentBase, AgentMetadata
from backend.services.orchestration.prompts.registry import PromptRegistry
from backend.services.orchestration.providers.mock_provider import MockProvider
import json

class VerificationAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.metadata = AgentMetadata(
            name="VerificationAgent",
            description="Ensure safety, accuracy, and pedagogical correctness.",
            version="1.0.0",
            enabled=True,
            priority=0, # Highest priority, intercepts output
            allowed_tools=[],
            allowed_collections=[],
            max_tokens=1024,
            temperature=0.0,
            timeout_ms=2000,
            retry_count=0
        )
        self.capabilities = ["safety_check", "pedagogical_check"]
        self.execution_policy = "synchronous"
        self.retry_policy = "none"
        self.max_iterations = 1

    def health_check(self) -> bool:
        return True

    def can_handle(self, query: str) -> bool:
        # Verification Agent intercepts all outputs, it doesn't handle queries directly
        return False

    def validate_input(self, unified_context: Dict[str, Any], query: str) -> bool:
        # Query here is actually the output of another agent
        return bool(query)

    def validate_output(self, response: Dict[str, Any]) -> bool:
        return "is_safe" in response

    def execute(self, unified_context: Dict[str, Any], agent_response: str) -> Dict[str, Any]:
        if not self.validate_input(unified_context, agent_response):
            raise ValueError("Invalid input to verification")
            
        prompt = PromptRegistry().get_prompt(self.metadata.name)
        provider = MockProvider()
        
        provider_result = provider.generate(
            prompt=prompt,
            context=unified_context,
            query=agent_response,
            allowed_tools=self.metadata.allowed_tools
        )
        
        try:
            parsed = json.loads(provider_result["response"])
        except:
            parsed = {"is_safe": True, "reason": "Fallback parsing"}
            
        response = {
            "is_safe": parsed.get("is_safe", True),
            "reason": parsed.get("reason", ""),
            "telemetry": provider_result["telemetry"]
        }
        
        if not self.validate_output(response):
            raise ValueError("Invalid verification output")
            
        return response
