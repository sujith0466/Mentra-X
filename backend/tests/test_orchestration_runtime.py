import pytest
import time
from unittest.mock import MagicMock
from backend.services.orchestration.runtime.event_bus import EventBus
from backend.services.orchestration.runtime.workflow_store import WorkflowStore
from backend.services.orchestration.runtime.execution_manager import ExecutionManager
from backend.services.orchestration.runtime.circuit_breaker import CircuitOpenError
from backend.services.orchestration.runtime.rate_limiter import RateLimitExceededError
from backend.services.orchestration.runtime.timeout_policy import TimeoutError
from backend.services.orchestration.runtime.runtime import AgentRuntime

def test_event_bus_idempotency():
    bus = EventBus()
    bus.clear()

    handler = MagicMock()
    bus.subscribe("TestEvent", handler)

    payload = {"idempotency_key": "key1", "data": "value"}
    
    # First publish should succeed
    bus.publish("TestEvent", payload)
    assert handler.call_count == 1

    # Second publish with same key should be ignored
    bus.publish("TestEvent", payload)
    assert handler.call_count == 1

def test_workflow_store_lifecycle():
    store = WorkflowStore()
    store.clear()

    wf = store.create_workflow("wf_1", "TestAgent")
    assert wf["workflow_status"] == "started"

    store.add_execution_event("wf_1", {"action": "test"})
    assert len(store.get_workflow("wf_1")["execution_events"]) == 1

    store.mark_completed("wf_1")
    assert store.get_workflow("wf_1")["workflow_status"] == "completed"

def test_execution_manager_timeout():
    manager = ExecutionManager(timeout_ms=100) # strict 100ms timeout
    
    def slow_func():
        time.sleep(0.3)
        return True

    from backend.services.orchestration.runtime.retry_policy import RetryExhaustedError

    with pytest.raises(RetryExhaustedError):
        manager.execute(slow_func)

def test_execution_manager_rate_limit():
    # 2 calls per second
    manager = ExecutionManager(rate_limit_calls=2, rate_limit_sec=1)
    
    def fast_func():
        return True

    manager.execute(fast_func)
    manager.execute(fast_func)

    with pytest.raises(RateLimitExceededError):
        manager.execute(fast_func)

def test_agent_runtime_integration():
    runtime = AgentRuntime()
    runtime.workflow_store.clear()
    
    wf = runtime.start_workflow("wf_int", "AgentA")
    assert wf["workflow_status"] == "started"

    manager = ExecutionManager()
    def simple_task():
        return "success"
    
    res = runtime.execute_agent_task("wf_int", simple_task, manager)
    assert res == "success"
    
    wf_updated = runtime.workflow_store.get_workflow("wf_int")
    assert len(wf_updated["execution_events"]) == 1
