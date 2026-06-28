# Mentra X — Event-Driven Architecture

**Version:** 1.0  
**Owner:** Sujith Kumar AI  
**ADR Reference:** ADR-008

---

## Overview

Mentra X uses an internal Event Bus to coordinate actions across services without tight coupling. When an action in one service needs to trigger actions in others, it emits an event rather than calling other services directly.

### Architecture Evolution

| Phase | Event Bus Implementation |
|---|---|
| Phases 1–3 | Direct service calls (acceptable at small scale) |
| Phase 4+ | Internal Python Event Bus (in-process, synchronous or async) |
| Production scale | Upgradeable to Redis Streams or Apache Kafka without changing event definitions |

---

## Event Bus Implementation

### `backend/events/event_bus.py`

```python
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Any
from collections import defaultdict
import asyncio

logger = logging.getLogger(__name__)


@dataclass
class Event:
    """Base class for all Mentra X domain events."""
    event_type: str
    user_id: str
    session_id: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    payload: dict = field(default_factory=dict)
    version: str = "1.0"


class EventBus:
    """
    In-process synchronous/async event bus.
    Supports multiple handlers per event type.
    All events are logged for observability.
    """

    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)
        self._event_log: list[Event] = []

    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Register a handler for an event type."""
        self._handlers[event_type].append(handler)
        logger.debug(f"Handler registered: {handler.__name__} → {event_type}")

    def emit(self, event: Event) -> None:
        """
        Emit an event synchronously.
        All registered handlers are called in order.
        Handler failures are logged but do not abort other handlers.
        """
        logger.info(
            f"Event emitted: {event.event_type}",
            extra={
                "event_type": event.event_type,
                "user_id": event.user_id,
                "session_id": event.session_id,
                "timestamp": event.timestamp.isoformat(),
                "version": event.version
            }
        )
        self._event_log.append(event)

        for handler in self._handlers.get(event.event_type, []):
            try:
                handler(event)
            except Exception as e:
                logger.error(
                    f"Event handler failed: {handler.__name__} for {event.event_type}",
                    extra={"error": str(e), "event_type": event.event_type},
                    exc_info=True
                )

    async def emit_async(self, event: Event) -> None:
        """Async version — emit event without blocking the response path."""
        asyncio.create_task(self._dispatch_async(event))

    async def _dispatch_async(self, event: Event) -> None:
        for handler in self._handlers.get(event.event_type, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                logger.error(
                    f"Async handler failed: {handler.__name__}",
                    extra={"error": str(e)},
                    exc_info=True
                )


# Singleton
event_bus = EventBus()
```

---

## Event Registry

### Complete Event Catalog

| Event Type | Producer | Consumer(s) | Trigger |
|---|---|---|---|
| `assessment.completed` | AssessmentService | TwinBuilder, MemoryService | Student completes diagnostic |
| `twin.created` | TwinBuilder | MemoryService (upsert DNA) | First twin initialization |
| `twin.mutated` | TwinMutator | Redis cache invalidation, ObservabilityLogger | Any twin state change |
| `twin.health_updated` | TwinHealthCalc | DashboardCache | Health score recomputed |
| `memory.stored` | MemoryService | ObservabilityLogger | Any Qdrant write |
| `memory.retrieved` | MemoryService | ObservabilityLogger | Any Qdrant read |
| `explanation.generated` | TutorAgent | MemoryService, ObservabilityLogger | Tutor produces explanation |
| `enkrypt.validated` | EnkryptValidator | ObservabilityLogger, SafetyMonitor | Enkrypt runs validation |
| `enkrypt.hard_fail` | RegenerationLoop | HITLService, TextbookFallback | Confidence below 0.70 after retries |
| `verification.passed` | VerificationAgent | TwinMutator (mastery +0.05), MemoryService | Student passes comprehension quiz |
| `verification.failed` | VerificationAgent | TwinMutator (mistake_count +1), MemoryService | Student fails comprehension quiz |
| `session.ended` | SwarmOrchestrator | MemoryService (session log), SessionCounter | AI session completes |
| `weakness.detected` | WeaknessAgent | RevisionPlanner, DashboardNotifier | Weakness cluster identified |
| `revision.scheduled` | SpacedRepetitionEngine | DashboardNotifier, EmailService | Revision task created |
| `decay.applied` | DecayScheduler | MemoryService (mastery update) | Nightly decay run |
| `opportunity.matched` | OpportunityService | DashboardNotifier | Student matches opportunity |
| `insight.generated` | InsightEngine | DashboardCache, EmailService | Weekly report produced |

---

## Event Schemas

### AssessmentCompleted

```python
@dataclass
class AssessmentCompletedEvent(Event):
    event_type: str = "assessment.completed"
    # payload:
    # {
    #   "session_id": str,
    #   "exam_track": str,
    #   "knowledge_state": dict,    — KnowledgeState per concept cluster
    #   "inferred_style": str,      — "Visual" | "Mathematical" | "Narrative"
    #   "inferred_level": int,      — 1–5
    #   "questions_served": int
    # }
```

**Producer:** `AssessmentService.complete_assessment()`  
**Consumers:**
- `TwinBuilder.seed_twin_from_assessment(event)` — writes KnowledgeState to twin
- `MemoryService.upsert_learning_dna(event)` — upserts DNA to Qdrant

**Retry Policy:** At-most-once delivery (event logged; if consumer fails, twin sync corrects on next hourly run)  
**Failure Handling:** If TwinBuilder fails, `TWIN_007` error logged; student sees generic assessment result; twin sync corrects within 1 hour

---

### TwinMutated

```python
@dataclass
class TwinMutatedEvent(Event):
    event_type: str = "twin.mutated"
    # payload:
    # {
    #   "twin_version": int,        — new version number
    #   "mutation_type": str,       — "verification_pass" | "decay" | "assessment" | "cron"
    #   "concept": str | None,      — concept affected (if applicable)
    #   "field_changed": str,       — e.g., "mastery_per_concept.thermodynamics.entropy"
    #   "old_value": Any,
    #   "new_value": Any,
    #   "agent_name": str | None
    # }
```

**Producer:** `TwinMutator.mutate()` (every mutation)  
**Consumers:**
- `RedisCacheInvalidator.invalidate_dna(event)` — deletes Redis key `dna:{user_id}`
- `ObservabilityLogger.log_mutation(event)` — writes to MongoDB audit log
- `TwinHealthCalc.schedule_recompute(event)` — queues health score recomputation

---

### VerificationPassed

```python
@dataclass
class VerificationPassedEvent(Event):
    event_type: str = "verification.passed"
    # payload:
    # {
    #   "concept": str,
    #   "teaching_level": int,
    #   "analogy_type": str | None,
    #   "semantic_score": float,      — 0.75–1.0
    #   "enkrypt_confidence": float,
    #   "explanation_id": str
    # }
```

**Producer:** `VerificationAgent.evaluate_answer()` when semantic score ≥ 0.75  
**Consumers:**
- `TwinMutator.mutate_knowledge(concept, +0.05)` — increase mastery
- `TwinMutator.mutate_dna(preferred_level, analogy_effectiveness)` — update DNA
- `MemoryService.store_explanation(success=True)` — write to explanation_history

---

### WeaknessDetected

```python
@dataclass
class WeaknessDetectedEvent(Event):
    event_type: str = "weakness.detected"
    # payload:
    # {
    #   "macro_weakness": str,        — cluster label
    #   "sub_topics": list[str],
    #   "severity": str,              — "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
    #   "severity_score": float,
    #   "occurrence_count": int,
    #   "sessions_analyzed": int,
    #   "revision_plan": dict
    # }
```

**Producer:** `WeaknessIntelligenceService.analyze()`  
**Consumers:**
- `SpacedRepetitionEngine.trigger_revision(event)` — creates revision_tasks in MySQL
- `DashboardNotifier.push_weakness_alert(event)` — pushes to student dashboard
- `MemoryService.upsert_weak_concepts(event)` — writes to Qdrant weak_concepts

---

### EnkryptHardFail

```python
@dataclass
class EnkryptHardFailEvent(Event):
    event_type: str = "enkrypt.hard_fail"
    # payload:
    # {
    #   "original_output": str,      — raw Tutor Agent output (never shown to student)
    #   "math_score": float,
    #   "science_score": float,
    #   "hallucination_score": float,
    #   "pedagogy_score": float,
    #   "composite_score": float,
    #   "regeneration_attempts": int,
    #   "fallback_concept": str,
    #   "fallback_source": str        — e.g., "NCERT Physics XI, Chapter 12"
    # }
```

**Producer:** `RegenerationLoop.execute()` when second attempt fails  
**Consumers:**
- `HITLService.raise_flag(event)` — writes to `hitl_queue` MySQL table
- `TextbookFallback.serve(event)` — delivers pre-verified content to student
- `SafetyMonitor.log_hard_fail(event)` — writes to `enkrypt_intercepts` table

---

## Handler Registration

### `backend/events/handlers/__init__.py`

```python
from backend.events.event_bus import event_bus
from backend.events.handlers import twin_handlers, memory_handlers, safety_handlers

def register_all_handlers():
    """Called once during app startup."""

    # Twin events
    event_bus.subscribe("assessment.completed", twin_handlers.seed_twin_from_assessment)
    event_bus.subscribe("twin.mutated", twin_handlers.invalidate_redis_cache)
    event_bus.subscribe("twin.mutated", twin_handlers.log_mutation_to_audit)

    # Memory events
    event_bus.subscribe("verification.passed", memory_handlers.store_explanation_success)
    event_bus.subscribe("verification.failed", memory_handlers.store_explanation_failure)
    event_bus.subscribe("session.ended", memory_handlers.store_session_log)

    # Safety events
    event_bus.subscribe("enkrypt.hard_fail", safety_handlers.raise_hitl_flag)
    event_bus.subscribe("enkrypt.hard_fail", safety_handlers.serve_textbook_fallback)
    event_bus.subscribe("enkrypt.validated", safety_handlers.log_intercept)

    # Intelligence events
    event_bus.subscribe("weakness.detected", intelligence_handlers.create_revision_tasks)
    event_bus.subscribe("weakness.detected", intelligence_handlers.push_dashboard_alert)
    event_bus.subscribe("insight.generated", intelligence_handlers.push_weekly_report)

    # Opportunity events
    event_bus.subscribe("opportunity.matched", opportunity_handlers.notify_student)
```

---

## Upgrade Path to Redis Streams

When user volume requires async event processing, replace the in-process bus with Redis Streams:

```python
# Drop-in replacement for EventBus.emit()
import redis
r = redis.Redis(host=os.getenv("REDIS_HOST"))

def emit_to_redis_stream(event: Event) -> None:
    r.xadd(
        f"mentrax:events:{event.event_type}",
        {
            "user_id": event.user_id,
            "session_id": event.session_id,
            "payload": json.dumps(event.payload),
            "version": event.version,
            "timestamp": event.timestamp.isoformat()
        },
        maxlen=10000    # Keep last 10K events per stream
    )
```

No changes required to event producers or consumer logic — only the bus implementation changes.
