import pytest
from backend.services.orchestration.tools.registry import ToolRegistry, ToolDefinition
from backend.services.orchestration.tools.twin_tools import register_twin_tools
from backend.services.orchestration.tools.memory_tools import register_memory_tools
from backend.services.orchestration.tools.assessment_tools import register_assessment_tools

def test_tool_registry_singleton():
    reg1 = ToolRegistry()
    reg2 = ToolRegistry()
    assert reg1 is reg2

def test_register_all_tools():
    registry = ToolRegistry()
    registry.clear()
    
    register_twin_tools(registry)
    register_memory_tools(registry)
    register_assessment_tools(registry)
    
    tools = registry.get_all_tools()
    
    # We registered 3 tools: get_digital_twin, retrieve_semantic_memory, start_assessment_session
    assert "get_digital_twin" in tools
    assert "retrieve_semantic_memory" in tools
    assert "start_assessment_session" in tools
    
    # Check twin tool definition details
    twin_def = tools["get_digital_twin"]["definition"]
    assert twin_def.permissions == "twin:read"
    assert twin_def.is_mutable is False
    assert twin_def.supports_parallel is True
    
    # Check assessment tool definition details
    ass_def = tools["start_assessment_session"]["definition"]
    assert ass_def.permissions == "assessment:write"
    assert ass_def.is_mutable is True
    assert "AssessmentStarted" in ass_def.produces_events
