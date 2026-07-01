import logging
from typing import Callable, Any
from backend.services.orchestration.runtime.retry_policy import with_retry
from backend.services.orchestration.runtime.timeout_policy import with_timeout
from backend.services.orchestration.runtime.circuit_breaker import CircuitBreaker
from backend.services.orchestration.runtime.rate_limiter import RateLimiter
from backend.services.orchestration.runtime.budget_manager import BudgetManager

logger = logging.getLogger(__name__)

class ExecutionManager:
    """
    Composes all runtime policies (timeout, retry, circuit breaker, rate limiting).
    Allows executing a target function with full protective scaffolding.
    """
    def __init__(self, 
                 timeout_ms: int = 5000, 
                 retries: int = 1,
                 circuit_threshold: int = 5,
                 rate_limit_calls: int = 10,
                 rate_limit_sec: int = 60,
                 max_tokens: int = 4096):
        self.circuit_breaker = CircuitBreaker(failure_threshold=circuit_threshold)
        self.rate_limiter = RateLimiter(calls=rate_limit_calls, period_sec=rate_limit_sec)
        self.timeout_ms = timeout_ms
        self.retries = retries
        self.budget_manager = BudgetManager(max_tokens=max_tokens, max_duration_ms=timeout_ms)

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        Executes the function wrapped in all policies.
        Order of wrapping matters:
        RateLimit -> CircuitBreaker -> Retry -> Timeout -> Function
        """
        
        # 1. Timeout
        timed_func = with_timeout(self.timeout_ms)(func)
        
        # 2. Retry
        retry_func = with_retry(max_retries=self.retries)(timed_func)
        
        # 3. Circuit Breaker
        circuit_func = self.circuit_breaker(retry_func)
        
        # 4. Rate Limiter
        safe_func = self.rate_limiter(circuit_func)
        
        # We don't wrap budget here automatically as tokens are reported asynchronously
        # by the LLM response, but the runtime tracks it.
        
        return safe_func(*args, **kwargs)
