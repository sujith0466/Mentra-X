import time
import threading
import logging
from typing import Callable, Any
from functools import wraps

logger = logging.getLogger(__name__)

class RateLimitExceededError(Exception):
    pass

class RateLimiter:
    """
    Token bucket rate limiter to prevent LLM/Tool abuse.
    """
    def __init__(self, calls: int, period_sec: int):
        self.capacity = calls
        self.tokens = calls
        self.period = period_sec
        self.last_refill = time.time()
        self._lock = threading.Lock()

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with self._lock:
                now = time.time()
                elapsed = now - self.last_refill
                
                # Refill tokens
                refill_amount = int(elapsed * (self.capacity / self.period))
                if refill_amount > 0:
                    self.tokens = min(self.capacity, self.tokens + refill_amount)
                    self.last_refill = now

                if self.tokens > 0:
                    self.tokens -= 1
                else:
                    logger.warning(f"Rate limit exceeded for {func.__name__}")
                    raise RateLimitExceededError("Rate limit exceeded. Please slow down.")
                    
            return func(*args, **kwargs)
        return wrapper
