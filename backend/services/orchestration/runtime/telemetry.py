import logging
from functools import wraps
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

logger = logging.getLogger(__name__)

# Initialize basic OpenTelemetry tracing (Console exporter for local dev/testing)
try:
    provider = TracerProvider()
    processor = SimpleSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
except Exception as e:
    logger.warning(f"Failed to initialize OpenTelemetry: {e}")

tracer = trace.get_tracer("mastra.cognitive.swarm.runtime")

def trace_execution(name: str):
    """
    Decorator to wrap function calls in OpenTelemetry spans.
    Automatically captures latency and basic metadata.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(name) as span:
                try:
                    # Capture basic context if present
                    if 'workflow_id' in kwargs:
                        span.set_attribute("workflow_id", kwargs['workflow_id'])
                    
                    result = func(*args, **kwargs)
                    span.set_attribute("status", "success")
                    return result
                except Exception as e:
                    span.set_attribute("status", "failed")
                    span.record_exception(e)
                    raise
        return wrapper
    return decorator
