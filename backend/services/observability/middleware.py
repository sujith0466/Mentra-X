import time
import uuid
from typing import Callable
from flask import request, g, jsonify, Response, Flask
from backend.services.observability.otel_config import get_tracer, generate_trace_id, generate_span_id
from backend.services.observability.json_logger import (
    set_correlation_id, set_trace_id, set_span_id, set_user_id, get_json_logger
)
from backend.services.observability.metrics import ObservabilityMetrics

logger = get_json_logger("backend.observability.middleware")

def observability_middleware(app: Flask):
    """
    Registers before_request and after_request handlers on a Flask application
    for distributed tracing, correlation ID injection, and latency monitoring.
    Also registers /api/observability/metrics and /api/observability/dashboard endpoints.
    """
    @app.before_request
    def before_request_trace():
        start_time = time.time()
        g.start_time = start_time

        # Extract or generate correlation ID
        correlation_id = request.headers.get("X-Request-ID") or f"req-{uuid.uuid4().hex[:12]}"
        set_correlation_id(correlation_id)
        g.correlation_id = correlation_id

        # Extract or generate trace ID
        trace_id = request.headers.get("X-Trace-ID") or generate_trace_id()
        set_trace_id(trace_id)
        g.trace_id = trace_id

        # Generate root HTTP span ID
        span_id = generate_span_id()
        set_span_id(span_id)
        g.span_id = span_id

        # Try to extract user_id if present in session or jwt or headers
        user_id = request.headers.get("X-User-ID") or request.args.get("user_id")
        if user_id and str(user_id).isdigit():
            set_user_id(int(user_id))
            g.user_id = int(user_id)

        # Start OTel span
        tracer = get_tracer()
        g.span = tracer.start_span(f"http.{request.method}.{request.path}")
        g.span.set_attribute("http.method", request.method)
        g.span.set_attribute("http.url", request.url)
        g.span.set_attribute("http.target", request.path)
        g.span.set_attribute("mentra.correlation_id", correlation_id)

    @app.after_request
    def after_request_trace(response: Response):
        duration_ms = (time.time() - getattr(g, "start_time", time.time())) * 1000
        status_code = response.status_code

        # Record metrics
        metrics = ObservabilityMetrics()
        metrics.record_http_request(duration_ms, status_code)

        # Update OTel span
        span = getattr(g, "span", None)
        if span:
            span.set_attribute("http.status_code", status_code)
            span.set_attribute("http.duration_ms", duration_ms)
            span.end()

        # Add correlation headers to response
        if hasattr(g, "correlation_id"):
            response.headers["X-Request-ID"] = g.correlation_id
        if hasattr(g, "trace_id"):
            response.headers["X-Trace-ID"] = g.trace_id

        return response

    @app.route("/api/observability/metrics", methods=["GET"])
    def get_metrics_endpoint():
        """
        Prometheus/JSON metrics endpoint for Prometheus scraping or Grafana ingestion.
        """
        metrics = ObservabilityMetrics()
        data = metrics.get_dashboard_metrics()
        
        # Check if Prometheus plaintext format requested
        if "text/plain" in request.headers.get("Accept", "") or request.args.get("format") == "prometheus":
            lines = [
                "# HELP mentra_http_requests_total Total HTTP requests processed.",
                "# TYPE mentra_http_requests_total counter",
                f"mentra_http_requests_total {data['counters']['http_requests_total']}",
                "# HELP mentra_http_errors_total Total HTTP errors (4xx/5xx).",
                "# TYPE mentra_http_errors_total counter",
                f"mentra_http_errors_total {data['counters']['http_errors_total']}",
                "# HELP mentra_llm_generations_total Total LLM provider inferences.",
                "# TYPE mentra_llm_generations_total counter",
                f"mentra_llm_generations_total {data['counters']['llm_generations_total']}",
                "# HELP mentra_llm_tokens_total Total LLM tokens consumed.",
                "# TYPE mentra_llm_tokens_total counter",
                f"mentra_llm_tokens_total {data['economics']['tokens_total']}",
                "# HELP mentra_llm_estimated_cost_usd_total Total estimated LLM cost in USD.",
                "# TYPE mentra_llm_estimated_cost_usd_total counter",
                f"mentra_llm_estimated_cost_usd_total {data['economics']['estimated_cost_usd_total']}",
                "# HELP mentra_workflows_active Active cognitive workflows.",
                "# TYPE mentra_workflows_active gauge",
                f"mentra_workflows_active {data['counters']['workflows_active']}",
                "# HELP mentra_workflows_completed_total Total completed cognitive workflows.",
                "# TYPE mentra_workflows_completed_total counter",
                f"mentra_workflows_completed_total {data['counters']['workflows_completed_total']}",
                "# HELP mentra_workflows_failed_total Total failed cognitive workflows.",
                "# TYPE mentra_workflows_failed_total counter",
                f"mentra_workflows_failed_total {data['counters']['workflows_failed_total']}",
                "# HELP mentra_retries_total Total agent/tool retry attempts.",
                "# TYPE mentra_retries_total counter",
                f"mentra_retries_total {data['counters']['retries_total']}",
                "# HELP mentra_timeouts_total Total execution timeout events.",
                "# TYPE mentra_timeouts_total counter",
                f"mentra_timeouts_total {data['counters']['timeouts_total']}",
                "# HELP mentra_circuit_breaker_activations_total Total circuit breaker activations.",
                "# TYPE mentra_circuit_breaker_activations_total counter",
                f"mentra_circuit_breaker_activations_total {data['counters']['circuit_breaker_activations_total']}",
                "# HELP mentra_requests_per_minute HTTP requests per minute.",
                "# TYPE mentra_requests_per_minute gauge",
                f"mentra_requests_per_minute {data['performance']['requests_per_minute']}",
                "# HELP mentra_http_latency_avg_ms Average HTTP request latency.",
                "# TYPE mentra_http_latency_avg_ms gauge",
                f"mentra_http_latency_avg_ms {data['latencies']['http']['avg_ms']}",
                "# HELP mentra_llm_latency_avg_ms Average LLM generation latency.",
                "# TYPE mentra_llm_latency_avg_ms gauge",
                f"mentra_llm_latency_avg_ms {data['latencies']['llm']['avg_ms']}",
                "# HELP mentra_agent_routing_latency_avg_ms Average agent routing latency.",
                "# TYPE mentra_agent_routing_latency_avg_ms gauge",
                f"mentra_agent_routing_latency_avg_ms {data['latencies']['agent_routing']['avg_ms']}",
                "# HELP mentra_tool_execution_latency_avg_ms Average tool execution latency.",
                "# TYPE mentra_tool_execution_latency_avg_ms gauge",
                f"mentra_tool_execution_latency_avg_ms {data['latencies']['tool']['avg_ms']}",
                "# HELP mentra_memory_retrieval_latency_avg_ms Average memory retrieval latency.",
                "# TYPE mentra_memory_retrieval_latency_avg_ms gauge",
                f"mentra_memory_retrieval_latency_avg_ms {data['latencies']['memory_retrieval']['avg_ms']}",
                "# HELP mentra_vector_search_latency_avg_ms Average Qdrant vector search latency.",
                "# TYPE mentra_vector_search_latency_avg_ms gauge",
                f"mentra_vector_search_latency_avg_ms {data['latencies']['qdrant']['avg_ms']}",
                "# HELP mentra_prompt_loading_latency_avg_ms Average prompt loading latency.",
                "# TYPE mentra_prompt_loading_latency_avg_ms gauge",
                f"mentra_prompt_loading_latency_avg_ms {data['latencies']['prompt_loading']['avg_ms']}",
            ]
            return Response("\n".join(lines) + "\n", mimetype="text/plain")
            
        return jsonify(data)

    @app.route("/api/observability/dashboard", methods=["GET"])
    def get_dashboard_endpoint():
        """
        Returns JSON dashboard state including recent timeline events and system health.
        """
        metrics = ObservabilityMetrics()
        return jsonify({
            "metrics": metrics.get_dashboard_metrics(),
            "timeline": metrics.get_timeline(limit=50)
        })

    logger.info("Registered Observability Middleware and endpoints (/api/observability/metrics, /api/observability/dashboard)")
