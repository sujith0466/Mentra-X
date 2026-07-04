import os
import logging
import uuid
from typing import Optional, Any

logger = logging.getLogger(__name__)

# Attempt to import opentelemetry SDK and OTLP exporters
try:
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    logger.warning("OpenTelemetry SDK not installed; defaulting to internal ObservabilityMetrics fallback.")

class DummySpan:
    def __init__(self, name: str = "dummy"):
        self.name = name
    def set_attribute(self, key: str, value: Any):
        pass
    def set_status(self, status: Any, description: str = ""):
        pass
    def record_exception(self, exception: Exception):
        pass
    def end(self, end_time: Optional[float] = None):
        pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class DummyTracer:
    def start_as_current_span(self, name: str, **kwargs) -> DummySpan:
        return DummySpan(name)
    def start_span(self, name: str, **kwargs) -> DummySpan:
        return DummySpan(name)

class DummyCounter:
    def add(self, amount: int | float, attributes: Optional[dict] = None):
        pass

class DummyHistogram:
    def record(self, amount: int | float, attributes: Optional[dict] = None):
        pass

class DummyMeter:
    def create_counter(self, name: str, **kwargs) -> DummyCounter:
        return DummyCounter()
    def create_histogram(self, name: str, **kwargs) -> DummyHistogram:
        return DummyHistogram()

_tracer_instance = None
_meter_instance = None

def generate_trace_id() -> str:
    """Generates a 128-bit hex trace ID compatible with OTel and Jaeger."""
    return uuid.uuid4().hex

def generate_span_id() -> str:
    """Generates a 64-bit hex span ID compatible with OTel."""
    return uuid.uuid4().hex[:16]

def init_observability(service_name: str = "mentra-x-backend", otlp_endpoint: Optional[str] = None):
    """
    Initializes OpenTelemetry TracerProvider and MeterProvider with OTLP/Console export.
    """
    global _tracer_instance, _meter_instance
    if not OTEL_AVAILABLE:
        _tracer_instance = DummyTracer()
        _meter_instance = DummyMeter()
        return

    resource = Resource.create({"service.name": service_name, "service.version": "5.0.0"})

    # Setup Tracer Provider
    tracer_provider = TracerProvider(resource=resource)
    
    # Check if OTLP endpoint is provided via arg or env
    endpoint = otlp_endpoint or os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint:
        try:
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
            exporter = OTLPSpanExporter(endpoint=endpoint)
            tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
            logger.info(f"Configured OTLPSpanExporter to {endpoint}")
        except ImportError:
            logger.warning("OTLPSpanExporter not available, using ConsoleSpanExporter")
            tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    else:
        # Default to no-op or memory processor in development to avoid cluttering console unless debug
        if os.environ.get("OTEL_CONSOLE_EXPORT", "").lower() == "true":
            tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(tracer_provider)
    _tracer_instance = trace.get_tracer(service_name)

    # Setup Meter Provider
    try:
        if os.environ.get("OTEL_CONSOLE_EXPORT", "").lower() == "true":
            reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
            meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
            metrics.set_meter_provider(meter_provider)
            _meter_instance = metrics.get_meter(service_name)
        else:
            _meter_instance = DummyMeter()
    except Exception as e:
        logger.warning(f"Failed to initialize OTel MeterProvider: {e}")
        _meter_instance = DummyMeter()

def get_tracer(name: str = "mentra-x-backend"):
    global _tracer_instance
    if _tracer_instance is None:
        init_observability()
    return _tracer_instance or DummyTracer()

def get_meter(name: str = "mentra-x-backend"):
    global _meter_instance
    if _meter_instance is None:
        init_observability()
    return _meter_instance or DummyMeter()
