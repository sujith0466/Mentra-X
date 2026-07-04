import pytest
import uuid
from backend.models import db, ExplainabilityRecord
from backend.services.explainability.reasoning_trace import ReasoningTrace, ReasoningStep
from backend.services.explainability.decision_graph import DecisionGraphBuilder
from backend.services.explainability.confidence_engine import ConfidenceEngine
from backend.services.explainability.citation_engine import CitationEngine
from backend.services.explainability.counterfactual_engine import CounterfactualEngine
from backend.services.explainability.explanation_service import ExplanationService

@pytest.fixture
def app():
    from backend.app import app as flask_app
    flask_app.config['TESTING'] = True
    with flask_app.app_context():
        db.create_all()
        try:
            from backend.models import ensure_privacy_schema
            ensure_privacy_schema(db.session)
        except Exception:
            pass
        yield flask_app

def test_reasoning_trace_sanitization():
    trace = ReasoningTrace("wf-test-1")
    step = trace.add_step("TutorAgent", "<thought>Internal CoT scratchpad</thought> Explained quadratic equations to user.")
    assert "<thought>" not in step.action_summary
    assert "Explained quadratic equations to user." in step.action_summary

def test_decision_graph_builder():
    events = [
        {"event_type": "agent_action", "agent_name": "TutorAgent", "tool_name": "qdrant_retrieve", "status": "SUCCESS", "latency_ms": 25.0},
        {"event_type": "agent_action", "agent_name": "AssessmentAgent", "tool_name": "quiz_lookup", "status": "SUCCESS", "latency_ms": 15.0}
    ]
    builder = DecisionGraphBuilder("wf-test-graph")
    graph = builder.build_from_workflow_events(events)
    
    assert graph["workflow_id"] == "wf-test-graph"
    assert graph["node_count"] >= 5 # wf root, 2 agents, 2 tools, verification, response
    assert any(n["node_type"] == "memory" for n in graph["nodes"].values())
    assert any(n["node_type"] == "assessment" for n in graph["nodes"].values())

def test_confidence_engine_calculation():
    res = ConfidenceEngine.calculate_confidence(
        retrieval_similarity=0.90,
        assessment_confidence=0.85,
        twin_completeness=0.80,
        retrieved_memory_count=4,
        verification_score=0.98,
        prompt_eval_score=0.95
    )
    assert 0.85 <= res.confidence_score <= 1.00
    assert round(res.confidence_score + res.uncertainty_score, 2) == 1.00
    assert "Confidence is computed at" in res.explanation

def test_citation_and_counterfactual_engines():
    ctx = {
        "retrieved_memories": [{"id": "mem-1", "content": "Prior notes on calculus", "score": 0.92}],
        "twin_state": {"user_id": "99", "learning_style": "visual"},
        "assessment_results": [{"quiz_id": "q-10", "score": 88}],
        "assessment_confidence": 0.85,
        "topic": "Calculus derivatives"
    }
    
    cit_engine = CitationEngine()
    citations = cit_engine.extract_from_workflow_context(ctx)
    assert len(citations) >= 3
    assert any(c["source_type"] == "MEMORY_ENTRY" for c in citations)
    assert any(c["source_type"] == "TWIN_FACT" for c in citations)
    
    counterfactuals = CounterfactualEngine.generate_counterfactuals(ctx)
    assert len(counterfactuals) >= 2
    assert any(cf["insight_type"] == "LATENCY_OPTIMIZATION" or cf["insight_type"] == "EDUCATIONAL" for cf in counterfactuals)

def test_explanation_service_and_api(app):
    with app.app_context():
        wf_id = f"wf-explain-{uuid.uuid4().hex[:8]}"
        events = [{"agent_name": "TutorAgent", "action_summary": "Provided math hint", "tool_name": "qdrant_retrieve"}]
        ctx = {"retrieval_similarity": 0.88, "verification_score": 0.95}
        
        # 1. Generate & persist explanation
        exp = ExplanationService.generate_explanation(wf_id, events, ctx, persist=True)
        assert exp["workflow_id"] == wf_id
        assert exp["confidence_score"] > 0.0
        
        # 2. Verify DB record
        rec = ExplainabilityRecord.query.get(wf_id)
        assert rec is not None
        assert rec.confidence_score == exp["confidence_score"]
        
        # 3. Test REST API endpoints
        client = app.test_client()
        resp_wf = client.get(f'/api/explainability/workflow/{wf_id}')
        assert resp_wf.status_code == 200
        
        resp_graph = client.get(f'/api/explainability/decision_graph/{wf_id}')
        assert resp_graph.status_code == 200
        
        resp_cit = client.get(f'/api/explainability/citations/{wf_id}')
        assert resp_cit.status_code == 200
