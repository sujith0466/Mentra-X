import pytest
import os
from backend.services.orchestration.prompts.registry import PromptRegistry
from backend.services.orchestration.providers.mock_provider import MockProvider
from backend.services.orchestration.providers.mastra_provider import MastraProvider
from backend.services.orchestration.providers.openrouter_provider import OpenRouterProvider

def test_prompt_registry_loads_prompts():
    registry = PromptRegistry()
    registry.reload()
    
    tutor_prompt = registry.get_prompt("TutorAgent")
    assert "Tutor Agent" in tutor_prompt
    
    # test fallback
    unknown_prompt = registry.get_prompt("NonExistentAgent")
    assert "helpful AI assistant" in unknown_prompt

def test_mock_provider_generates_telemetry():
    provider = MockProvider()
    result = provider.generate(
        prompt="Test prompt for Tutor",
        context={},
        query="Hello"
    )
    
    assert "response" in result
    assert "telemetry" in result
    
    telemetry = result["telemetry"]
    assert telemetry["provider"] == "MockProvider"
    assert telemetry["token_usage"]["total_tokens"] > 0
    assert "prompt_hash" in telemetry
    assert "latency_ms" in telemetry

def test_mastra_provider_stub():
    provider = MastraProvider()
    result = provider.generate(
        prompt="Test prompt",
        context={},
        query="Hello"
    )
    
    assert "Mastra" in result["response"]
    assert result["telemetry"]["provider"] == "Mastra"

def test_openrouter_provider_stub():
    provider = OpenRouterProvider(model="anthropic/claude-3-sonnet")
    result = provider.generate(
        prompt="Test prompt",
        context={},
        query="Hello"
    )
    
    assert "OpenRouter" in result["response"]
    assert "claude-3-sonnet" in result["response"]
    assert result["telemetry"]["provider"] == "OpenRouter"
