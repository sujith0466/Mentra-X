import pytest
from unittest.mock import patch, MagicMock
from backend.services.orchestration.context_builder import ContextBuilder

def test_context_builder_builds_valid_schema():
    builder = ContextBuilder()

    # Mock facades
    builder.twin_facade = MagicMock()
    builder.assessment_facade = MagicMock()
    builder.memory_facade = MagicMock()

    mock_twin = MagicMock()
    mock_twin.twin_version = 1
    mock_twin.twin_health = 0.8
    mock_twin.twin_status = "ACTIVE"
    mock_twin.exam_track = "JEE"
    mock_twin.learning_dna = '{"learning_style": "visual"}'
    
    builder.twin_facade.get_twin.return_value = mock_twin
    builder.memory_facade.retrieve_context.return_value = ["mock_doubt_1"]

    context = builder.build(user_id=1, workflow_id="wf_123", current_agent="TutorAgent", query="help")

    # Assert static context
    assert context["static_context"]["user"]["id"] == 1
    assert context["static_context"]["twin"]["version"] == 1
    assert context["static_context"]["learning_dna"]["learning_style"] == "visual"

    # Assert dynamic context
    assert "mock_doubt_1" in context["dynamic_context"]["memory"]["recent_doubts"]

    # Assert execution context
    assert context["execution_context"]["workflow_metadata"]["workflow_id"] == "wf_123"
    assert context["execution_context"]["workflow_metadata"]["current_agent"] == "TutorAgent"
