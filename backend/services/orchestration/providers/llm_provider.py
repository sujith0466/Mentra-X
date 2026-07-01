from abc import ABC, abstractmethod
from typing import Dict, Any, List

class LLMProvider(ABC):
    """
    Abstract base class for all LLM providers (Mastra, OpenRouter, Mock, etc.).
    Agents communicate exclusively with this interface.
    """
    @abstractmethod
    def generate(self, prompt: str, context: Dict[str, Any], query: str, **kwargs) -> Dict[str, Any]:
        """
        Executes a prompt against the configured LLM.
        
        Args:
            prompt: The system prompt from the Prompt Registry.
            context: The UnifiedContext.
            query: The user query or agent input.
            **kwargs: Additional parameters like temperature, max_tokens, allowed_tools.
            
        Returns:
            Dict containing:
                - response: The actual string or JSON response from the model.
                - tools_used: List of tools triggered by the model.
                - telemetry: Dict of usage telemetry (token_usage, latency, cost, model_name).
        """
        pass
