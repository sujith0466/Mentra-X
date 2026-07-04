import time
import functools
import logging
from typing import Callable, Any, Dict, Optional
from backend.services.observability.otel_config import get_tracer, generate_span_id
from backend.services.observability.metrics import ObservabilityMetrics
from backend.services.observability.json_logger import set_span_id, get_span_id, get_json_logger

logger = get_json_logger("backend.observability.decorators")

def trace_agent_execution(agent_name: Optional[str] = None):
    """
    Decorator to trace agent execution time, retries, and outcome.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            target_name = agent_name
            if not target_name and args and hasattr(args[0], "metadata"):
                target_name = getattr(args[0].metadata, "name", "UnknownAgent")
            elif not target_name:
                target_name = func.__name__

            tracer = get_tracer()
            metrics = ObservabilityMetrics()
            start_time = time.time()
            new_span_id = generate_span_id()
            old_span_id = get_span_id()
            set_span_id(new_span_id)

            with tracer.start_as_current_span(f"agent.{target_name}") as span:
                span.set_attribute("mentra.agent.name", target_name)
                try:
                    result = func(*args, **kwargs)
                    duration_ms = (time.time() - start_time) * 1000
                    metrics.record_agent_execution(target_name, duration_ms, retries=0)
                    metrics.add_timeline_event("AGENT", target_name, duration_ms, {"status": "SUCCESS"})
                    span.set_attribute("mentra.execution.duration_ms", duration_ms)
                    span.set_attribute("mentra.status", "SUCCESS")
                    return result
                except Exception as e:
                    duration_ms = (time.time() - start_time) * 1000
                    metrics.record_agent_execution(target_name, duration_ms, retries=1)
                    metrics.add_timeline_event("AGENT", target_name, duration_ms, {"status": "FAILED", "error": str(e)})
                    span.set_attribute("mentra.status", "FAILED")
                    span.record_exception(e)
                    logger.error(f"Agent {target_name} failed after {round(duration_ms, 2)}ms: {e}", exc_info=True)
                    raise
                finally:
                    set_span_id(old_span_id)
        return wrapper
    return decorator

def trace_tool_call(tool_name: Optional[str] = None):
    """
    Decorator to trace tool execution latency and outcome.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            target_tool = tool_name or func.__name__
            tracer = get_tracer()
            metrics = ObservabilityMetrics()
            start_time = time.time()

            with tracer.start_as_current_span(f"tool.{target_tool}") as span:
                span.set_attribute("mentra.tool.name", target_tool)
                try:
                    result = func(*args, **kwargs)
                    duration_ms = (time.time() - start_time) * 1000
                    metrics.record_tool_execution(target_tool, duration_ms)
                    metrics.add_timeline_event("TOOL", target_tool, duration_ms, {"status": "SUCCESS"})
                    span.set_attribute("mentra.execution.duration_ms", duration_ms)
                    return result
                except Exception as e:
                    duration_ms = (time.time() - start_time) * 1000
                    metrics.record_tool_execution(target_tool, duration_ms)
                    metrics.add_timeline_event("TOOL", target_tool, duration_ms, {"status": "FAILED", "error": str(e)})
                    span.record_exception(e)
                    raise
        return wrapper
    return decorator

def trace_llm_generation(provider: str = "unknown", model: str = "unknown"):
    """
    Decorator to trace LLM provider generation, capturing prompt tokens, completion tokens,
    latency, and estimated cost.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            tracer = get_tracer()
            metrics = ObservabilityMetrics()
            start_time = time.time()
            
            # Extract prompt metadata if passed
            prompt_name = kwargs.get("prompt_name", "default")
            
            with tracer.start_as_current_span(f"llm.{provider}.{model}") as span:
                span.set_attribute("mentra.llm.provider", provider)
                span.set_attribute("mentra.llm.model", model)
                try:
                    result = func(*args, **kwargs)
                    duration_ms = (time.time() - start_time) * 1000
                    
                    # Extract telemetry from result if it matches LLMProvider dict structure
                    telemetry = result.get("telemetry", {}) if isinstance(result, dict) else {}
                    p_tokens = telemetry.get("token_usage", {}).get("prompt_tokens", 10)
                    c_tokens = telemetry.get("token_usage", {}).get("completion_tokens", 20)
                    cost = telemetry.get("execution_cost", 0.001)
                    p_ver = telemetry.get("prompt_version", "v1.0.0")
                    p_hash = telemetry.get("prompt_hash", "none")
                    
                    metrics.record_llm_generation(provider, model, duration_ms, p_tokens, c_tokens, cost)
                    metrics.add_timeline_event("LLM", f"{provider}/{model}", duration_ms, {
                        "tokens": p_tokens + c_tokens,
                        "cost_usd": cost,
                        "prompt_version": p_ver
                    })
                    
                    span.set_attribute("mentra.llm.tokens.prompt", p_tokens)
                    span.set_attribute("mentra.llm.tokens.completion", c_tokens)
                    span.set_attribute("mentra.llm.cost_usd", cost)
                    span.set_attribute("mentra.prompt.version", p_ver)
                    span.set_attribute("mentra.prompt.hash", p_hash)
                    return result
                except Exception as e:
                    duration_ms = (time.time() - start_time) * 1000
                    span.record_exception(e)
                    raise
        return wrapper
    return decorator

def trace_db_query(query_name: Optional[str] = None):
    """
    Decorator for database ORM or raw SQL query execution.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            target = query_name or func.__name__
            tracer = get_tracer()
            metrics = ObservabilityMetrics()
            start_time = time.time()
            with tracer.start_as_current_span(f"db.{target}") as span:
                span.set_attribute("mentra.db.operation", target)
                try:
                    result = func(*args, **kwargs)
                    duration_ms = (time.time() - start_time) * 1000
                    metrics.record_db_query(duration_ms)
                    span.set_attribute("mentra.execution.duration_ms", duration_ms)
                    return result
                except Exception as e:
                    span.record_exception(e)
                    raise
        return wrapper
    return decorator

def trace_vector_search(collection_name: Optional[str] = None):
    """
    Decorator for Qdrant vector retrieval or indexing operations.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            target = collection_name or func.__name__
            tracer = get_tracer()
            metrics = ObservabilityMetrics()
            start_time = time.time()
            with tracer.start_as_current_span(f"qdrant.{target}") as span:
                span.set_attribute("mentra.qdrant.collection", target)
                try:
                    result = func(*args, **kwargs)
                    duration_ms = (time.time() - start_time) * 1000
                    metrics.record_qdrant_search(duration_ms)
                    span.set_attribute("mentra.execution.duration_ms", duration_ms)
                    return result
                except Exception as e:
                    span.record_exception(e)
                    raise
        return wrapper
    return decorator
