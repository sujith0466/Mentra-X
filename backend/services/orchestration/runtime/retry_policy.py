import time
import logging
from typing import Callable, Any
from functools import wraps

logger = logging.getLogger(__name__)

class RetryExhaustedError(Exception):
    pass

def with_retry(max_retries: int = 3, base_delay: float = 0.5, max_delay: float = 5.0, backoff_factor: float = 2.0):
    """
    Decorator for executing a function with exponential backoff retries.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = base_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {delay}s...")
                        time.sleep(delay)
                        delay = min(delay * backoff_factor, max_delay)
                    else:
                        logger.error(f"All {max_retries} retries exhausted for {func.__name__}.")
            
            raise RetryExhaustedError(f"Failed after {max_retries} retries.") from last_exception
        return wrapper
    return decorator
