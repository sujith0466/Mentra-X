from typing import Dict, Any
from backend.services.orchestration.agents.registry import AgentBase, AgentMetadata
from backend.services.orchestration.prompts.registry import PromptRegistry
from backend.services.orchestration.providers.mock_provider import MockProvider
import json

class AssessmentAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.metadata = AgentMetadata(
            name="AssessmentAgent",
            description="Facilitate Bayesian tracking and adaptive testing.",
            version="1.0.0",
            enabled=True,
            priority=3,
            allowed_tools=["start_assessment_session"],
            allowed_collections=[],
            max_tokens=2048,
            temperature=0.2,
            timeout_ms=4000,
            retry_count=1
        )
        self.capabilities = ["quiz_generation", "bayesian_tracking"]
        self.execution_policy = "synchronous"
        self.retry_policy = "fixed_delay"
        self.max_iterations = 1

    def health_check(self) -> bool:
        return True

    def can_handle(self, query: str) -> bool:
        return "quiz" in query.lower() or "test me" in query.lower()

    def validate_input(self, unified_context: Dict[str, Any], query: str) -> bool:
        return True

    def validate_output(self, response: Dict[str, Any]) -> bool:
        return "assessment_result" in response

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
            parsed = {"assessment_result": provider_result["response"]}
            
        response = {
            "assessment_result": parsed.get("assessment_result", ""),
            "tools_used": provider_result["tools_used"] + parsed.get("tools_used", []),
            "telemetry": provider_result["telemetry"]
        }
        
        if not self.validate_output(response):
            raise ValueError("Invalid output")
            
        return response
