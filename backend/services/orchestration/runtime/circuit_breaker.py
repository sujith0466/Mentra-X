import time
import logging
from typing import Callable, Any
from functools import wraps

logger = logging.getLogger(__name__)

class CircuitOpenError(Exception):
    pass

class CircuitBreaker:
    """
    Prevents cascading failures by short-circuiting calls to a failing service.
    """
    def __init__(self, failure_threshold: int = 5, recovery_timeout_sec: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout_sec
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED" # CLOSED (ok), OPEN (failing), HALF_OPEN (recovering)

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            now = time.time()

            if self.state == "OPEN":
                if now - self.last_failure_time >= self.recovery_timeout:
                    logger.info(f"Circuit for {func.__name__} entering HALF_OPEN state.")
                    self.state = "HALF_OPEN"
                else:
                    raise CircuitOpenError(f"Circuit is OPEN for {func.__name__}. Fast failing.")

            try:
                result = func(*args, **kwargs)
                if self.state == "HALF_OPEN":
                    logger.info(f"Circuit for {func.__name__} recovered. Entering CLOSED state.")
                    self.state = "CLOSED"
                    self.failure_count = 0
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                if self.failure_count >= self.failure_threshold:
                    if self.state != "OPEN":
                        logger.error(f"Circuit for {func.__name__} entering OPEN state due to {self.failure_count} failures.")
                    self.state = "OPEN"
                raise
        return wrapper
