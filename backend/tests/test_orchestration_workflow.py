import pytest
from unittest.mock import patch, MagicMock
from backend.services.orchestration.orchestrator import Orchestrator
from backend.services.orchestration.agents.registry import AgentRegistry
from backend.services.orchestration.agents.tutor_agent import TutorAgent
from backend.services.orchestration.agents.memory_agent import MemoryAgent
from backend.services.orchestration.agents.assessment_agent import AssessmentAgent
from backend.services.orchestration.agents.verification_agent import VerificationAgent
from backend.services.orchestration.agents.insight_agent import InsightAgent
from backend.services.orchestration.agents.weakness_agent import WeaknessAgent

@pytest.fixture
def setup_orchestrator():
    registry = AgentRegistry()
    registry.clear()
    
    # Register all Milestone 4 agents
    registry.register_agent(TutorAgent())
    registry.register_agent(MemoryAgent())
    registry.register_agent(AssessmentAgent())
    registry.register_agent(VerificationAgent())
    registry.register_agent(InsightAgent())
    registry.register_agent(WeaknessAgent())
    
    orchestrator = Orchestrator()
    orchestrator.runtime.workflow_store.clear()
    orchestrator.runtime.event_bus.clear()
    return orchestrator

@patch("backend.services.orchestration.orchestrator.ContextBuilder.build")
def test_agent_selection_and_routing_memory(mock_build, setup_orchestrator):
    mock_build.return_value = {"static_context": {"user": {}}, "execution_context": {}, "dynamic_context": {}}
    # 'remember' should route to MemoryAgent
    orchestrator = setup_orchestrator
    response = orchestrator.process_query(user_id=1, workflow_id="wf_mem_1", query="Can you remember my last session?")
    
    assert "memory_context" in response
    wf_state = orchestrator.runtime.workflow_store.get_workflow("wf_mem_1")
    assert wf_state["current_agent"] == "MemoryAgent"
    assert wf_state["workflow_status"] == "completed"

@patch("backend.services.orchestration.orchestrator.ContextBuilder.build")
def test_agent_selection_and_routing_assessment(mock_build, setup_orchestrator):
    mock_build.return_value = {"static_context": {"user": {}}, "execution_context": {}, "dynamic_context": {}}
    # 'quiz' should route to AssessmentAgent
    orchestrator = setup_orchestrator
    response = orchestrator.process_query(user_id=1, workflow_id="wf_ass_1", query="I want a quiz on loops")
    
    assert "assessment_result" in response
    wf_state = orchestrator.runtime.workflow_store.get_workflow("wf_ass_1")
    assert wf_state["current_agent"] == "AssessmentAgent"

@patch("backend.services.orchestration.orchestrator.ContextBuilder.build")
def test_agent_selection_fallback_tutor(mock_build, setup_orchestrator):
    mock_build.return_value = {"static_context": {"user": {}}, "execution_context": {}, "dynamic_context": {}}
    # Generic query should route to TutorAgent
    orchestrator = setup_orchestrator
    response = orchestrator.process_query(user_id=1, workflow_id="wf_tut_1", query="Explain gravitational waves")
    
    assert "text" in response
    assert "Simulated tutoring response" in response["text"]
    wf_state = orchestrator.runtime.workflow_store.get_workflow("wf_tut_1")
    assert wf_state["current_agent"] == "TutorAgent"

@patch("backend.services.orchestration.orchestrator.ContextBuilder.build")
def test_workflow_transitions_and_verification_flow(mock_build, setup_orchestrator):
    mock_build.return_value = {"static_context": {"user": {}}, "execution_context": {}, "dynamic_context": {}}
    orchestrator = setup_orchestrator
    
    # Send a query to Insight Agent
    response = orchestrator.process_query(user_id=1, workflow_id="wf_ins_1", query="Give me an insight into my progress")
    
    wf_state = orchestrator.runtime.workflow_store.get_workflow("wf_ins_1")
    assert wf_state["workflow_status"] == "completed"
    
    # We can infer verification passed because an exception wasn't raised
    # Check execution events inside workflow store
    events = wf_state["execution_events"]
    # Should have two execution successes (Primary Agent + Verification Agent)
    assert len(events) == 2
    assert events[0]["func"] == "execute" # primary agent execute
    assert events[1]["func"] == "execute" # verification agent execute

@patch("backend.services.orchestration.orchestrator.ContextBuilder.build")
def test_event_emission_on_tool_usage(mock_build, setup_orchestrator):
    mock_build.return_value = {"static_context": {"user": {}}, "execution_context": {}, "dynamic_context": {}}
    orchestrator = setup_orchestrator
    
    events_received = []
    def mock_handler(payload):
        events_received.append(payload)
        
    orchestrator.runtime.event_bus.subscribe("get_digital_twin_executed", mock_handler)
    
    # Trigger weakness agent which uses get_digital_twin
    orchestrator.process_query(user_id=1, workflow_id="wf_weak_1", query="Why am I struggling?")
    
    assert len(events_received) == 1
    assert events_received[0]["tool"] == "get_digital_twin"
    assert events_received[0]["idempotency_key"] == "wf_weak_1_get_digital_twin"
