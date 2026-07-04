import logging
import time
from functools import wraps
from backend.services.observability.otel_config import get_tracer
from backend.services.observability.metrics import ObservabilityMetrics

logger = logging.getLogger(__name__)

tracer = get_tracer("mastra.cognitive.swarm.runtime")

def trace_execution(name: str):
    """
    Decorator to wrap function calls in OpenTelemetry spans and record enterprise metrics.
    Automatically captures latency and basic metadata.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            metrics = ObservabilityMetrics()
            start_time = time.time()
            with tracer.start_as_current_span(name) as span:
                try:
                    if 'workflow_id' in kwargs:
                        span.set_attribute("workflow_id", kwargs['workflow_id'])
                    elif len(args) > 1 and isinstance(args[1], str) and ("wf_" in args[1] or "-" in args[1]):
                        span.set_attribute("workflow_id", args[1])
                    
                    result = func(*args, **kwargs)
                    duration_ms = (time.time() - start_time) * 1000
                    span.set_attribute("status", "success")
                    span.set_attribute("execution_duration_ms", duration_ms)
                    metrics.add_timeline_event("RUNTIME", name, duration_ms, {"status": "success"})
                    return result
                except Exception as e:
                    duration_ms = (time.time() - start_time) * 1000
                    span.set_attribute("status", "failed")
                    span.record_exception(e)
                    metrics.add_timeline_event("RUNTIME", name, duration_ms, {"status": "failed", "error": str(e)})
                    raise
        return wrapper
    return decorator
