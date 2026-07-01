import threading
import logging
from typing import Callable, Any
from functools import wraps

logger = logging.getLogger(__name__)

class TimeoutError(Exception):
    pass

def with_timeout(timeout_ms: int):
    """
    Decorator for executing a function with a strict timeout.
    Uses threads for enforcement (in production, asyncio.wait_for is preferred for I/O).
    """
    timeout_sec = timeout_ms / 1000.0

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = [None]
            exception = [None]

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e

            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout_sec)

            if thread.is_alive():
                logger.error(f"Function {func.__name__} timed out after {timeout_ms}ms")
                raise TimeoutError(f"Execution exceeded {timeout_ms}ms timeout")
            
            if exception[0]:
                raise exception[0]

            return result[0]
        return wrapper
    return decorator
