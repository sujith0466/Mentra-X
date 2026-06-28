# ADR-005: Enkrypt AI as Educational Safety Middleware

**Status:** ACCEPTED  
**Date:** 2026-06-28  
**Author:** Sujith Kumar AI  
**Context Phase:** Phase 6 (Safety Layer)

---

## Context

Mentra X targets high-stakes exam preparation (JEE, NEET, UPSC, CAT). In these domains, factual accuracy is non-negotiable. A single hallucinated formula, incorrect scientific claim, or misleading pedagogical analogy can cause a student to lose critical marks, severely damaging trust in the platform.

Standard LLM outputs are inherently probabilistic. Even advanced models like GPT-4o hallucinate formulas or misapply concepts.

## Problem Statement

How do we guarantee that AI-generated educational content is mathematically accurate, scientifically correct, free of hallucinations, and pedagogically appropriate *before* it reaches the student?

## Decision

We will implement **Enkrypt AI** as a mandatory safety middleware layer (Phase 6).

The Enkrypt layer sits between the Tutor Agent's output and the student. It acts as an absolute gatekeeper. It evaluates the generated explanation using four distinct validators:
1. Math Validator
2. Science Validator
3. Hallucination Validator
4. Pedagogy Validator

A composite confidence score is calculated:
**Composite = (0.40 × Math) + (0.30 × Science) + (0.20 × Hallucination) + (0.10 × Pedagogy)**

- If Composite ≥ 0.90: Content is **Approved** and sent to the student.
- If 0.70 ≤ Composite < 0.90: Content is **Rejected** and a Regeneration Loop triggers (max 2 attempts).
- If Composite < 0.70 (or max retries hit): **Hard Fail**. The system intercepts the AI response and serves a pre-verified textbook fallback (e.g., "NCERT Physics XI, Chapter 12") while raising a Human-in-the-Loop (HITL) flag.

## Alternatives Considered

| Approach | Fact-Checking Rigor | Latency Impact | Reliability | Pros | Cons |
|---|---|---|---|---|---|
| **Enkrypt AI** (Selected) | Extremely High | +400ms | High | Purpose-built for AI safety, quantitative scoring | Third-party dependency, adds latency |
| **Prompt Engineering** | Low | None | Low | Free, zero latency | Prompt instructions to "be accurate" do not prevent hallucinations |
| **OpenAI Moderation API** | None (Safety only) | +150ms | High | Prevents hate/harm | Does not check math/science factual accuracy |
| **Guardrails AI** | Medium | +800ms | Medium | Open source, flexible | Requires writing custom regex/logic for every formula, slow |
| **Human Review Only** | Perfect | +Hours | High | 100% accurate | Cannot operate in real-time tutoring session |

## Pros

- **Absolute Brand Protection:** Prevents the system from delivering factually incorrect information.
- **Quantitative Safety:** Replaces subjective prompt instructions with a hard mathematical threshold (0.90).
- **Self-Healing:** The Regeneration Loop provides the failed Enkrypt context back to the LLM, allowing it to correct its own mistake automatically.
- **Graceful Degradation:** Textbook fallback ensures the student receives high-quality information even when the AI completely fails.

## Cons

- Adds 300–500ms of latency to the session.
- API cost overhead per query.
- Potential for false positives (rejecting a valid but unconventional explanation).

## Trade-offs

We are trading execution speed (latency) and API cost for absolute factual guarantee. In high-stakes education, accuracy is strictly more important than speed. The student can wait an extra 500ms, but they cannot afford to learn a wrong formula.

## Consequences

- All content generation agents MUST route their output through the Enkrypt tool.
- The UI must handle the slightly longer wait times gracefully (e.g., using skeleton loaders or "Analyzing response..." microcopy).
- The admin dashboard requires a HITL review queue to handle Hard Fail intercepts.
- The system must maintain a repository of textbook fallbacks for every concept tag.

## Future Revisions

This decision should be reconsidered if base foundational models reach zero-hallucination guarantees in STEM domains, or if the latency overhead of Enkrypt exceeds 1500ms at scale.
