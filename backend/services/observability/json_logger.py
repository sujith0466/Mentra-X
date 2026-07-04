import logging
import json
import time
import datetime
import os
import re
from typing import Dict, Any, Optional

# Context variables for distributed tracing correlation
import contextvars

_correlation_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("correlation_id", default=None)
_trace_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("trace_id", default=None)
_span_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("span_id", default=None)
_workflow_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("workflow_id", default=None)
_user_id_var: contextvars.ContextVar[Optional[int]] = contextvars.ContextVar("user_id", default=None)

def set_correlation_id(correlation_id: Optional[str]):
    return _correlation_id_var.set(correlation_id)

def get_correlation_id() -> Optional[str]:
    return _correlation_id_var.get()

def set_trace_id(trace_id: Optional[str]):
    return _trace_id_var.set(trace_id)

def get_trace_id() -> Optional[str]:
    return _trace_id_var.get()

def set_span_id(span_id: Optional[str]):
    return _span_id_var.set(span_id)

def get_span_id() -> Optional[str]:
    return _span_id_var.get()

def set_workflow_id(workflow_id: Optional[str]):
    return _workflow_id_var.set(workflow_id)

def get_workflow_id() -> Optional[str]:
    return _workflow_id_var.get()

def set_user_id(user_id: Optional[int]):
    return _user_id_var.set(user_id)

def get_user_id() -> Optional[int]:
    return _user_id_var.get()

def get_trace_context() -> Dict[str, Any]:
    """Returns a dict of all current tracing metadata for propagation."""
    return {
        "trace_id": get_trace_id(),
        "span_id": get_span_id(),
        "correlation_id": get_correlation_id(),
        "workflow_id": get_workflow_id(),
        "user_id": get_user_id()
    }

def restore_trace_context(ctx: Dict[str, Any]):
    """Restores trace context from a dictionary payload."""
    if not isinstance(ctx, dict):
        return
    if ctx.get("trace_id"): set_trace_id(ctx["trace_id"])
    if ctx.get("span_id"): set_span_id(ctx["span_id"])
    if ctx.get("correlation_id"): set_correlation_id(ctx["correlation_id"])
    if ctx.get("workflow_id"): set_workflow_id(ctx["workflow_id"])
    if ctx.get("user_id") is not None: set_user_id(ctx["user_id"])

SENSITIVE_KEYS = {"password", "token", "jwt", "api_key", "secret", "authorization", "phone", "email", "ssn", "pii", "student_answer", "personal_profile"}
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
PHONE_REGEX = re.compile(r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b')
JWT_REGEX = re.compile(r'\beo[0-9a-zA-Z\-_]+\.[0-9a-zA-Z\-_]+\.[0-9a-zA-Z\-_]+\b')

def redact_sensitive_data(data: Any) -> Any:
    """Recursively redacts PII and sensitive credentials from log structures."""
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            k_lower = str(k).lower()
            if "email" in k_lower:
                new_dict[k] = "[EMAIL_REDACTED]"
            elif "phone" in k_lower:
                new_dict[k] = "[PHONE_REDACTED]"
            elif "jwt" in k_lower or "token" in k_lower:
                new_dict[k] = "[JWT_REDACTED]"
            elif any(s in k_lower for s in SENSITIVE_KEYS):
                new_dict[k] = "[REDACTED]"
            else:
                new_dict[k] = redact_sensitive_data(v)
        return new_dict
    elif isinstance(data, list):
        return [redact_sensitive_data(item) for item in data]
    elif isinstance(data, str):
        val = EMAIL_REGEX.sub("[EMAIL_REDACTED]", data)
        val = PHONE_REGEX.sub("[PHONE_REDACTED]", val)
        val = JWT_REGEX.sub("[JWT_REDACTED]", val)
        return val
    return data


class JSONFormatter(logging.Formatter):
    """
    Structured JSON Formatter for Mentra X Enterprise Observability.
    Outputs log records as JSON strings enriched with OpenTelemetry trace metadata,
    correlation IDs, workflow correlation, AI execution metrics, and automatic PII redaction.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Inject contextvars if present
        trace_id = get_trace_id() or getattr(record, "trace_id", None)
        if trace_id:
            log_entry["trace_id"] = trace_id

        span_id = get_span_id() or getattr(record, "span_id", None)
        if span_id:
            log_entry["span_id"] = span_id

        correlation_id = get_correlation_id() or getattr(record, "correlation_id", None)
        if correlation_id:
            log_entry["correlation_id"] = correlation_id

        workflow_id = get_workflow_id() or getattr(record, "workflow_id", None)
        if workflow_id:
            log_entry["workflow_id"] = workflow_id

        user_id = get_user_id() or getattr(record, "user_id", None)
        if user_id is not None:
            log_entry["user_id"] = user_id

        # Extra fields attached to log record
        for key in [
            "agent_name", "llm_provider", "model_name", "prompt_version", "prompt_hash",
            "execution_duration_ms", "tokens_used", "estimated_cost_usd",
            "tool_name", "collection_name", "db_table", "status_code", "error_type",
            "retry_count"
        ]:
            if hasattr(record, key):
                log_entry[key] = getattr(record, key)

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Apply privacy redaction
        log_entry = redact_sensitive_data(log_entry)

        return json.dumps(log_entry, ensure_ascii=False)


def setup_json_logging(log_level: int = logging.INFO):
    """
    Configures the root logger to use JSONFormatter.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    
    root_logger = logging.getLogger("backend")
    root_logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicate logs
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    root_logger.addHandler(handler)
    return root_logger

def get_json_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
