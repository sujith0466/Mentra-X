import logging
import uuid
import threading
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime, timezone
from backend.services.observability.json_logger import get_trace_context, restore_trace_context

logger = logging.getLogger(__name__)

class EventBus:
    """
    Persistent Event Bus for the Mastra Cognitive Swarm (Phase 5 Milestone 4).
    Responsible for fanning out domain and system events to downstream consumers
    with strict idempotency guarantees, persistent event log (EventRecord),
    Dead Letter Queue (DLQ), event replay support, and trace context propagation.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(EventBus, cls).__new__(cls)
                cls._instance._subscribers: Dict[str, List[Callable]] = {}
                cls._instance._processed_events = set()
                cls._instance._memory_dlq: List[Dict[str, Any]] = []
                cls._instance._memory_events: List[Dict[str, Any]] = []
        return cls._instance

    def subscribe(self, event_type: str, handler: Callable):
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(handler)

    def publish(self, event_type: str, payload: Dict[str, Any]):
        """
        Publishes an event to all subscribers of the given event_type.
        Enforces idempotency, records event to persistent EventRecord table,
        and routes failed events to Dead Letter Queue (DLQ).
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
        
        # Inject distributed trace context
        if "_trace_context" not in payload:
            payload["_trace_context"] = get_trace_context()

        self._memory_events.append({"event_type": event_type, "payload": payload, "status": "PUBLISHED"})
        self._persist_event(payload["event_id"], event_type, payload, "PUBLISHED")

        handlers = self._subscribers.get(event_type, [])
        all_succeeded = True
        last_error = None

        for handler in handlers:
            try:
                restore_trace_context(payload.get("_trace_context"))
                handler(payload)
            except Exception as e:
                all_succeeded = False
                last_error = str(e)
                logger.error(f"Error executing handler {handler.__name__} for event {event_type}: {e}")

        if all_succeeded:
            self._update_event_status(payload["event_id"], "PROCESSED")
        elif not all_succeeded:
            self._update_event_status(payload["event_id"], "DLQ", last_error)
            with self._lock:
                self._memory_dlq.append({"event_type": event_type, "payload": payload, "error": last_error})
            logger.warning(f"Event {payload['event_id']} ({event_type}) sent to Dead Letter Queue (DLQ).")

    def get_dlq_events(self) -> List[Dict[str, Any]]:
        """Retrieves events currently sitting in the Dead Letter Queue."""
        with self._lock:
            try:
                from backend.models import EventRecord
                records = EventRecord.query.filter_by(status="DLQ").all()
                return [
                    {
                        "event_id": r.event_id,
                        "event_type": r.event_type,
                        "payload": r.payload,
                        "error": r.error_message,
                        "created_at": r.created_at.isoformat() if r.created_at else None
                    }
                    for r in records
                ]
            except Exception:
                return list(self._memory_dlq)

    def retry_dlq_event(self, event_id: str) -> bool:
        """Re-attempts processing an event from the Dead Letter Queue."""
        target_payload = None
        target_type = None
        
        try:
            from backend.models import db, EventRecord
            record = EventRecord.query.filter_by(event_id=event_id, status="DLQ").first()
            if record:
                target_payload = record.payload
                target_type = record.event_type
                record.status = "RETRYING"
                record.retry_count += 1
                db.session.commit()
        except Exception:
            pass

        if not target_payload:
            with self._lock:
                for idx, item in enumerate(self._memory_dlq):
                    if item.get("payload", {}).get("event_id") == event_id:
                        target_payload = item["payload"]
                        target_type = item["event_type"]
                        del self._memory_dlq[idx]
                        break

        if not target_payload or not target_type:
            logger.warning(f"DLQ event {event_id} not found.")
            return False

        # Remove from processed_events so it can run again
        idempotency_key = target_payload.get("idempotency_key")
        if idempotency_key and idempotency_key in self._processed_events:
            self._processed_events.remove(idempotency_key)

        self.publish(target_type, target_payload)
        return True

    def replay_events(self, event_type: Optional[str] = None, from_timestamp: Optional[str] = None) -> int:
        """
        Replays historical events from persistent storage to active subscribers.
        Returns the count of replayed events.
        """
        replayed_count = 0
        events_to_replay = []
        try:
            from backend.models import EventRecord
            query = EventRecord.query.filter(EventRecord.status.in_(["PUBLISHED", "PROCESSED"]))
            if event_type:
                query = query.filter_by(event_type=event_type)
            if from_timestamp:
                query = query.filter(EventRecord.created_at >= from_timestamp)
            records = query.order_by(EventRecord.created_at.asc()).all()
            for r in records:
                if r.payload:
                    events_to_replay.append((r.event_type, r.payload))
        except Exception:
            with self._lock:
                for item in self._memory_events:
                    if event_type and item["event_type"] != event_type:
                        continue
                    events_to_replay.append((item["event_type"], item["payload"]))

        for etype, epayload in events_to_replay:
            # Temporarily remove idempotency key to permit replay
            ikey = epayload.get("idempotency_key")
            if ikey and ikey in self._processed_events:
                self._processed_events.remove(ikey)
            self.publish(etype, epayload)
            replayed_count += 1

        logger.info(f"Replayed {replayed_count} historical events.")
        return replayed_count

    def get_bus_metrics(self) -> Dict[str, Any]:
        """Returns aggregate event throughput and queue health metrics."""
        with self._lock:
            dlq_len = len(self._memory_dlq)
            try:
                from backend.models import DeadLetterQueueRecord
                dlq_len = DeadLetterQueueRecord.query.count()
            except Exception:
                pass
            return {
                "total_processed": len(self._processed_events),
                "dlq_count": dlq_len,
                "queue_depth": 0,
                "status": "HEALTHY" if dlq_len < 10 else "DEGRADED"
            }

    def clear(self):
        """Used for testing to clear state."""
        with self._lock:
            self._subscribers.clear()
            self._processed_events.clear()
            self._memory_dlq.clear()
            self._memory_events.clear()
            try:
                from backend.models import db, EventRecord
                EventRecord.query.delete()
                db.session.commit()
            except Exception:
                pass

    def _persist_event(self, event_id: str, event_type: str, payload: Dict[str, Any], status: str):
        try:
            from backend.models import db, EventRecord
            rec = EventRecord(
                event_id=event_id,
                event_type=event_type,
                payload=payload,
                status=status
            )
            db.session.add(rec)
            db.session.commit()
        except Exception:
            try:
                from backend.models import db
                db.session.rollback()
            except Exception:
                pass

    def _update_event_status(self, event_id: str, status: str, error_message: Optional[str] = None):
        try:
            from backend.models import db, EventRecord
            rec = EventRecord.query.filter_by(event_id=event_id).first()
            if rec:
                rec.status = status
                if error_message:
                    rec.error_message = error_message
                if status == "PROCESSED":
                    from backend.models import utcnow
                    rec.processed_at = utcnow()
                db.session.commit()
        except Exception:
            try:
                from backend.models import db
                db.session.rollback()
            except Exception:
                pass
