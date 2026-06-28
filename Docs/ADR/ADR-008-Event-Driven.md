# ADR-008: Event-Driven Architecture for Twin Mutations

**Status:** ACCEPTED  
**Date:** 2026-06-28  
**Author:** Sujith Kumar AI  
**Context Phase:** Phase 4 (Cognitive Swarm) & Phase 7 (Continuous Learning)

---

## Context

In Mentra X, multiple system actions need to trigger downstream processes:
- A diagnostic assessment completion must seed the initial Digital Twin.
- A student passing a Verification micro-quiz must increase their mastery score in the Twin.
- A Twin mutation must invalidate the Redis hot cache.
- The completion of a 5th tutoring session must trigger the Weakness Intelligence Agent.
- The nightly cron job must trigger Ebbinghaus decay calculations.

## Problem Statement

How should cross-service communication and trigger logic be managed? If the `VerificationAgent` directly calls `TwinMutator.mutate_knowledge()` which directly calls `Redis.delete()`, the services become tightly coupled. If one fails, the whole chain fails. Adding a new reaction (e.g., sending an email) requires modifying the core verification code.

## Decision

We will implement an **Event-Driven Architecture** using an internal Event Bus.

Instead of direct function calls, services emit strongly-typed events (e.g., `VerificationPassedEvent`, `TwinMutatedEvent`). Other services subscribe to these events and execute asynchronously or synchronously in isolated handlers.

For Phase 4, the Event Bus is implemented as a lightweight, in-process Python module (`backend/events/event_bus.py`). It supports both sync and async dispatch.

## Alternatives Considered

| Approach | Coupling | Operational Overhead | Local Dev Friction | Pros | Cons |
|---|---|---|---|---|---|
| **In-Process Event Bus** (Selected) | Loose | Low | Zero | Simple to debug, loose coupling | Drops events on server crash |
| **Redis Streams / Kafka** | Very Loose | High | High | Highly reliable, scalable | Overkill for pre-launch, requires dedicated infrastructure |
| **Direct Function Calls** | Tight | None | None | Easy to trace in IDE | Spaghetti code, hard to add new side effects |
| **Celery Tasks Only** | Medium | Medium | Medium | Good for background work | Doesn't solve the pub/sub broadcast requirement well |

## Pros

- **Decoupling:** The Verification Agent doesn't need to know that Redis exists. It just emits `VerificationPassedEvent`.
- **Extensibility:** If we want to add a gamification system later (e.g., grant XP for passing), we just add a new subscriber to `VerificationPassedEvent` without touching the Verification Agent.
- **Auditability:** The Event Bus logs every emitted event, providing a perfect chronological trace of system state changes.

## Cons

- Events executed asynchronously in the in-process bus will be lost if the Flask worker crashes before they complete.
- Traceability requires searching logs rather than just clicking "Go To Definition" in an IDE.

## Trade-offs

We are choosing an in-process Event Bus to get the architectural benefits of decoupling without the infrastructure overhead of Kafka or Redis Streams on day one. 

Because educational state mutations (like a mastery increase of +0.05) are highly additive, the rare loss of an asynchronous event due to a server crash is acceptable and will self-correct during the next interaction or nightly sync.

## Consequences

- All inter-domain side effects must occur via the `event_bus`.
- Events must be defined as Python `@dataclass` objects inheriting from the `Event` base class.
- All events must include `user_id` and `session_id` for traceability.

## Future Revisions

When the platform scales to multiple load-balanced web workers with high concurrency, the `emit()` function inside `event_bus.py` will be swapped out to push payloads to Redis Streams. The event schemas and consumer logic will remain completely unchanged, ensuring a zero-rewrite migration path.
