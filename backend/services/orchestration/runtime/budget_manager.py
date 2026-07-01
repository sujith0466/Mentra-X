import threading
import logging

logger = logging.getLogger(__name__)

class BudgetExceededError(Exception):
    pass

class BudgetManager:
    """
    Tracks token usage and latency budgets for a single execution context.
    """
    def __init__(self, max_tokens: int = 4096, max_duration_ms: int = 15000):
        self.max_tokens = max_tokens
        self.max_duration_ms = max_duration_ms
        self.tokens_used = 0
        self._lock = threading.Lock()

    def add_tokens(self, count: int):
        with self._lock:
            self.tokens_used += count
            if self.tokens_used > self.max_tokens:
                logger.error(f"Token budget exceeded: {self.tokens_used} > {self.max_tokens}")
                raise BudgetExceededError(f"Exceeded max tokens of {self.max_tokens}")

    def get_remaining_tokens(self) -> int:
        with self._lock:
            return max(0, self.max_tokens - self.tokens_used)
