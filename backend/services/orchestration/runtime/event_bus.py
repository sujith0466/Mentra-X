import logging
import uuid
import threading
from typing import Dict, List, Callable, Any
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class EventBus:
    """
    Internal Event Bus for the Mastra Cognitive Swarm.
    Responsible for fanning out domain and system events to downstream consumers
    with strict idempotency guarantees.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(EventBus, cls).__new__(cls)
                cls._instance._subscribers = {}
                cls._instance._processed_events = set() # Stores idempotency_key for simple deduplication
        return cls._instance

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def publish(self, event_type: str, payload: Dict[str, Any]):
        """
        Publishes an event to all subscribers of the given event_type.
        Enforces idempotency using the idempotency_key in the payload.
        """
        idempotency_key = payload.get("idempotency_key")
        if not idempotency_key:
            logger.warning(f"Event {event_type} published without idempotency_key.")
        elif idempotency_key in self._processed_events:
            logger.debug(f"Event {event_type} with key {idempotency_key} already processed. Skipping.")
            return

        if idempotency_key:
            self._processed_events.add(idempotency_key)

        # Enhance payload with mandatory metadata if missing
        if "event_id" not in payload:
            payload["event_id"] = str(uuid.uuid4())
        if "timestamp" not in payload:
            payload["timestamp"] = datetime.now(timezone.utc).isoformat()
        if "event_version" not in payload:
            payload["event_version"] = "1.0.0"
        
        handlers = self._subscribers.get(event_type, [])
        for handler in handlers:
            try:
                handler(payload)
            except Exception as e:
                logger.error(f"Error executing handler {handler.__name__} for event {event_type}: {e}")

    def clear(self):
        """Used for testing to clear state."""
        self._subscribers.clear()
        self._processed_events.clear()
