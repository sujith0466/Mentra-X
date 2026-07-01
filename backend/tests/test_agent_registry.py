import pytest
from backend.services.orchestration.agents.registry import AgentRegistry, AgentBase, AgentMetadata

class MockAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.metadata = AgentMetadata(
            name="TestAgent",
            description="A test agent",
            version="1.0.0",
            enabled=True,
            priority=10,
            allowed_tools=["get_digital_twin"],
            allowed_collections=[],
            max_tokens=1000,
            temperature=0.0,
            timeout_ms=1000,
            retry_count=0
        )
        
    def execute(self, unified_context, query):
        return {"response": "test"}

class DisabledAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.metadata = AgentMetadata(
            name="DisabledAgent",
            description="A disabled agent",
            version="1.0.0",
            enabled=False,
            priority=1,
            allowed_tools=[],
            allowed_collections=[],
            max_tokens=1000,
            temperature=0.0,
            timeout_ms=1000,
            retry_count=0
        )
        
    def execute(self, unified_context, query):
        return {}

def test_agent_registry():
    registry = AgentRegistry()
    registry.clear()
    
    a1 = MockAgent()
    a2 = DisabledAgent()
    
    registry.register_agent(a1)
    registry.register_agent(a2)
    
    # discover_agents should only return enabled agents
    enabled_metadata = registry.discover_agents()
    assert len(enabled_metadata) == 1
    assert enabled_metadata[0].name == "TestAgent"
    
    # agent_capabilities
    caps = registry.agent_capabilities("TestAgent")
    assert "get_digital_twin" in caps["tools"]
    
    # health_check
    assert registry.health_check("TestAgent") is True
    assert registry.health_check("UnknownAgent") is False
