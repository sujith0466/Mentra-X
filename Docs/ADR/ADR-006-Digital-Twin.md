# ADR-006: Student Digital Twin as Core Architecture Pattern

**Status:** ACCEPTED  
**Date:** 2026-06-28  
**Author:** Sujith Kumar AI  
**Context Phase:** Phase 1 (Digital Twin Engine)

---

## Context

Traditional session-based AI tutors have amnesia. Every time a student starts a new session, the AI forgets what the student knows, how the student learns, what analogies previously failed, and how quickly the student forgets concepts. 

Mentra X needs to provide a truly personalized tutoring experience that persists across years of high-stakes exam preparation. The system must adapt its teaching strategies, manage spaced repetition, and track skill growth continuously.

## Problem Statement

How should student personalization be modeled and stored? The system must capture:
- *What* the student knows (academic mastery).
- *How* the student learns (preferred styles, frustration tolerance).
- *What worked/failed* (past teaching strategies).
- *How fast they forget* (Ebbinghaus decay curve per concept).

## Decision

We will implement the **Student Digital Twin** as the core architectural pattern.

Instead of passing simple user profiles to the LLM, Mentra X maintains a persistent, continuously evolving cognitive model for every student. The Twin consists of 7 distinct states:

1. **Academic State:** Enrolled courses, total XP, progression.
2. **Knowledge State:** Concept-by-concept mastery scores (0.0–1.0).
3. **Skill State:** Domain expertise (e.g., abstract reasoning vs. rote memorization).
4. **Learning DNA:** Behavioral traits (preferred level, style, frustration tolerance).
5. **Career State:** Resume, interviews, professional goals.
6. **Project State:** Active projects, portfolio items.
7. **Opportunity State:** Matching parameters for internships/hackathons.

The Twin is stored across MySQL (for structured states 1, 3, 5, 6, 7) and Qdrant (for semantic/behavioral states 2, 4). 

Crucially, the Twin is versioned: every mutation increments `twin_version` and is recorded in an audit log, allowing us to replay a student's entire learning journey.

## Alternatives Considered

| Pattern | Persistence | Captures "How" to Teach | Pros | Cons |
|---|---|---|---|---|
| **Student Digital Twin** (Selected) | High (MySQL + Qdrant) | Yes (Learning DNA) | Deepest personalization, supports decay modeling | High engineering complexity |
| **Session Context Only** | None | No | Zero engineering overhead | AI amnesia; frustrating for student |
| **User Profile with Tags** | Low (MySQL flags) | Limited | Easy to build | Too shallow to model cognitive decay |
| **Knowledge Graph** | High (Neo4j) | No | Great for concept relationships | Overhead of graph DB; doesn't naturally store behavioral metrics |

## Pros

- **Hyper-Personalization:** The Tutor Agent knows exactly which analogies failed two months ago and avoids them.
- **Cognitive Modeling:** Enables the Continuous Learning Loop (Phase 7) to apply Ebbinghaus forgetting curves to mastery scores over time.
- **Observability:** Twin mutation logs provide concrete proof that the AI is actually impacting the student's measurable knowledge.
- **Engagement:** The Twin Health score provides a gamified, overarching metric for the student to improve.

## Cons

- High architectural complexity (synchronizing state across MySQL and Qdrant).
- Requires an event-driven mutator pattern to handle concurrent updates (e.g., an assessment finishing at the same time an AI session ends).

## Trade-offs

We are trading initial development speed for a massive competitive moat. A simple RAG chatbot is easy to build but highly commoditized. The Digital Twin provides compounding value — the longer a student uses Mentra X, the better the Twin becomes, creating immense switching costs.

## Consequences

- No AI agent is allowed to generate a response without first querying the Digital Twin via the Memory Agent.
- All twin mutations must flow through a centralized `TwinMutator` service to guarantee version increments and event bus emissions.
- The nightly scheduler is required to apply decay functions to the Twin's Knowledge State.

## Future Revisions

This architecture is foundational and unlikely to change at a macro level, though the specific storage mechanisms (e.g., migrating some states from MySQL to Qdrant) may evolve as data scales.
