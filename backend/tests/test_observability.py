import pytest
import json
import logging
from flask import Flask
from backend.services.observability.otel_config import get_tracer, get_meter, init_observability, generate_trace_id
from backend.services.observability.json_logger import JSONFormatter, set_correlation_id, set_trace_id, set_span_id
from backend.services.observability.metrics import ObservabilityMetrics
from backend.services.observability.decorators import (
    trace_agent_execution, trace_tool_call, trace_llm_generation, trace_db_query, trace_vector_search
)
from backend.services.observability.middleware import observability_middleware

@pytest.fixture(autouse=True)
def reset_metrics():
    metrics = ObservabilityMetrics()
    metrics.clear()
    yield
    metrics.clear()

def test_init_observability():
    init_observability()
    tracer = get_tracer("test-tracer")
    meter = get_meter("test-meter")
    assert tracer is not None
    assert meter is not None

def test_json_formatter():
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test.logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test log message",
        args=(),
        exc_info=None
    )
    
    set_correlation_id("test-corr-123")
    set_trace_id("test-trace-456")
    set_span_id("test-span-789")
    
    output = formatter.format(record)
    data = json.loads(output)
    
    assert data["level"] == "INFO"
    assert data["message"] == "Test log message"
    assert data["correlation_id"] == "test-corr-123"
    assert data["trace_id"] == "test-trace-456"
    assert data["span_id"] == "test-span-789"

def test_observability_metrics_aggregation():
    metrics = ObservabilityMetrics()
    
    # Record events
    metrics.record_http_request(120.5, 200)
    metrics.record_http_request(55.0, 500) # error
    metrics.record_db_query(15.2)
    metrics.record_qdrant_search(45.0)
    metrics.record_llm_generation("gemini", "gemini-1.5-pro", 800.0, prompt_tokens=100, completion_tokens=50, cost_usd=0.002)
    metrics.record_agent_execution("TutorAgent", 850.0, retries=1)
    metrics.add_timeline_event("AGENT", "TutorAgent", 850.0, {"status": "SUCCESS"})
    
    dash_metrics = metrics.get_dashboard_metrics()
    
    assert dash_metrics["counters"]["http_requests_total"] == 2
    assert dash_metrics["counters"]["http_errors_total"] == 1
    assert dash_metrics["counters"]["db_queries_total"] == 1
    assert dash_metrics["counters"]["qdrant_searches_total"] == 1
    assert dash_metrics["counters"]["llm_generations_total"] == 1
    assert dash_metrics["counters"]["retries_total"] == 1
    
    assert dash_metrics["economics"]["tokens_total"] == 150
    assert dash_metrics["economics"]["estimated_cost_usd_total"] == 0.002
    assert dash_metrics["economics"]["tokens_by_provider"]["gemini"] == 150
    
    timeline = metrics.get_timeline()
    assert len(timeline) == 1
    assert timeline[0]["type"] == "AGENT"
    assert timeline[0]["name"] == "TutorAgent"

def test_decorators():
    metrics = ObservabilityMetrics()

    @trace_agent_execution(agent_name="TestAgent")
    def run_agent():
        return "agent_ok"

    @trace_tool_call(tool_name="test_tool")
    def run_tool():
        return "tool_ok"

    @trace_llm_generation(provider="test_prov", model="test_mod")
    def run_llm():
        return {
            "response": "ok",
            "telemetry": {
                "token_usage": {"prompt_tokens": 10, "completion_tokens": 20},
                "execution_cost": 0.0005,
                "prompt_version": "v1.0"
            }
        }

    @trace_db_query("select_users")
    def run_db():
        return True

    @trace_vector_search("search_memories")
    def run_vector():
        return []

    assert run_agent() == "agent_ok"
    assert run_tool() == "tool_ok"
    assert run_llm()["response"] == "ok"
    assert run_db() is True
    assert run_vector() == []

    dash = metrics.get_dashboard_metrics()
    assert dash["counters"]["agent_executions_total"] == 1
    assert dash["counters"]["tool_executions_total"] == 1
    assert dash["counters"]["llm_generations_total"] == 1
    assert dash["counters"]["db_queries_total"] == 1
    assert dash["counters"]["qdrant_searches_total"] == 1
    assert dash["economics"]["tokens_total"] == 30

def test_middleware_and_endpoints():
    app = Flask(__name__)
    observability_middleware(app)

    @app.route("/test-route")
    def test_route():
        return "hello world", 200

    client = app.test_client()
    
    # Trigger route
    res = client.get("/test-route", headers={"X-Request-ID": "test-req-99"})
    assert res.status_code == 200
    assert res.headers.get("X-Request-ID") == "test-req-99"
    assert "X-Trace-ID" in res.headers

    # Check metrics endpoint JSON format
    metrics_res = client.get("/api/observability/metrics")
    assert metrics_res.status_code == 200
    data = metrics_res.get_json()
    assert data["counters"]["http_requests_total"] >= 1

    # Check Prometheus text/plain format
    prom_res = client.get("/api/observability/metrics?format=prometheus", headers={"Accept": "text/plain"})
    assert prom_res.status_code == 200
    assert b"mentra_http_requests_total" in prom_res.data
    assert b"mentra_llm_tokens_total" in prom_res.data

    # Check dashboard endpoint
    dash_res = client.get("/api/observability/dashboard")
    assert dash_res.status_code == 200
    dash_data = dash_res.get_json()
    assert "metrics" in dash_data
    assert "timeline" in dash_data

def test_pii_redaction():
    from backend.services.observability.json_logger import redact_sensitive_data
    sample = {
        "user": "student",
        "password": "secret_password_123",
        "email": "test.student@university.edu",
        "phone": "555-019-2834",
        "jwt_token": "ey12345.payload.sign",
        "nested": {"api_key": "sk-1234567890"}
    }
    redacted = redact_sensitive_data(sample)
    assert redacted["password"] == "[REDACTED]"
    assert redacted["email"] == "[EMAIL_REDACTED]"
    assert redacted["phone"] == "[PHONE_REDACTED]"
    assert redacted["jwt_token"] == "[JWT_REDACTED]"
    assert redacted["nested"]["api_key"] == "[REDACTED]"
    assert redacted["user"] == "student"

def test_automatic_tool_instrumentation():
    from backend.services.orchestration.tools.registry import ToolRegistry, ToolDefinition
    metrics = ObservabilityMetrics()
    reg = ToolRegistry()
    reg.clear()

    def sample_tool(x: int) -> int:
        return x * 2

    defn = ToolDefinition(
        name="test_auto_tool",
        description="A test tool",
        version="1.0",
        owner="test",
        permissions="read",
        is_mutable=False,
        supports_streaming=False,
        supports_parallel=True,
        deterministic=True,
        needs_verification=False,
        produces_events=[],
        consumes_events=[],
        input_schema={},
        output_schema={},
        timeout_ms=1000,
        retry_count=0
    )

    reg.register_tool(defn, sample_tool)
    res = reg.execute_tool("test_auto_tool", 5)
    assert res == 10
    assert metrics.get_dashboard_metrics()["counters"]["tool_executions_total"] >= 1

def test_prompt_analytics_and_eval_hooks():
    metrics = ObservabilityMetrics()
    metrics.record_prompt_analytics(
        version_key="tutor-v1.0",
        prompt_hash="hash123",
        author="MentraAI",
        semantic_version="1.0.0",
        latency_ms=450.0,
        tokens=150,
        cost_usd=0.001,
        success=True,
        confidence=0.95,
        eval_score=0.92
    )
    pa = metrics.get_prompt_analytics()
    assert "tutor-v1.0" in pa
    assert pa["tutor-v1.0"]["avg_latency_ms"] == 450.0
    assert pa["tutor-v1.0"]["success_rate_pct"] == 100.0

    hook_results = []
    def eval_callback(payload):
        hook_results.append(payload.get("score"))

    metrics.register_evaluation_hook("faithfulness", eval_callback)
    metrics.trigger_evaluation_hooks("faithfulness", {"score": 0.99})
    assert len(hook_results) == 1
    assert hook_results[0] == 0.99

def test_event_bus_trace_propagation():
    from backend.services.orchestration.runtime.event_bus import EventBus
    from backend.services.observability.json_logger import set_trace_id, get_trace_id
    eb = EventBus()
    eb.clear()

    set_trace_id("trace-event-999")
    received_trace_ids = []

    def subscriber_handler(payload):
        received_trace_ids.append(get_trace_id())

    eb.subscribe("test.trace.event", subscriber_handler)
    eb.publish("test.trace.event", {"data": "test", "idempotency_key": "idemp-001"})

    assert len(received_trace_ids) == 1
    assert received_trace_ids[0] == "trace-event-999"
