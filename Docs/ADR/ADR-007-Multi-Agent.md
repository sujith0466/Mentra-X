# ADR-007: Multi-Agent System over Monolithic LLM Prompt

**Status:** ACCEPTED  
**Date:** 2026-06-28  
**Author:** Sujith Kumar AI  
**Context Phase:** Phase 4 (Cognitive Swarm)

---

## Context

The educational AI workflow in Mentra X is highly complex. A single interaction requires:
1. Understanding the user's intent.
2. Retrieving data from multiple Qdrant vector collections.
3. Deciding on a pedagogical strategy.
4. Generating the content.
5. Verifying safety.
6. Generating a follow-up comprehension quiz.
7. Evaluating the student's answer.
8. Mutating the Digital Twin.

## Problem Statement

Should this entire workflow be managed by a single, monolithic LLM prompt that attempts to orchestrate all these steps, or should it be split into a system of specialized, interacting agents?

## Decision

We will implement a **6-agent Directed Acyclic Graph (DAG)**.

Each agent has a single, strictly defined responsibility, specialized tools, and strongly typed inputs and outputs. The agents are:
1. **Memory Agent:** Responsible exclusively for retrieving and assembling context from Qdrant.
2. **Tutor Agent:** Responsible exclusively for pedagogical content generation.
3. **Verification Agent:** Responsible exclusively for generating micro-quizzes and evaluating student comprehension.
4. **Assessment Agent:** Operates the Phase 2 diagnostic flows.
5. **Weakness Intelligence Agent:** Runs asynchronously (via cron) to detect long-term weakness clusters.
6. **Insight Agent:** Runs asynchronously to generate weekly reports and opportunity matches.

These agents do not "chat" with each other in natural language. They pass structured data (Pydantic models) along the edges of the DAG.

## Alternatives Considered

| Architecture | Separation of Concerns | Predictability | Latency | Debuggability |
|---|---|---|---|---|
| **Multi-Agent DAG** (Selected) | Excellent | High | Medium | Excellent |
| **Monolithic System Prompt** | Poor | Low | Fast | Poor |
| **Conversational Multi-Agent** (AutoGen) | Good | Very Low | Slow | Poor (emergent behavior) |

## Pros

- **Prompt Optimization:** The Tutor Agent's prompt is 100% focused on teaching pedagogy. It doesn't need instructions on how to parse JSON or call Qdrant tools.
- **Explainability:** If an explanation fails safety validation, we can look exactly at the Tutor Agent's output trace to see why, without memory retrieval logs cluttering the trace.
- **Parallelization:** Agents that don't depend on each other's outputs can run simultaneously.
- **Testability:** We can write unit tests for the Verification Agent by passing it mock Tutor Agent outputs.

## Cons

- Architectural complexity is higher.
- Overhead of defining strict Pydantic schemas for inter-agent communication.
- Marginal latency increase due to multiple discrete LLM calls instead of one large call (though this is heavily mitigated by streaming).

## Trade-offs

We are trading the simplicity of a single API call for the robust, production-ready predictability of a modular system. In an educational context where hallucination prevention is critical, monolithic prompts simply cannot guarantee that safety rules won't be "forgotten" mid-generation.

## Consequences

- The `mastra/agents/` directory will contain strictly one agent definition per file.
- All inter-agent data passing must use DTOs defined in `backend/dto/`.
- Developer observability panels will visualize the DAG execution step-by-step rather than showing a single AI "black box."

## Future Revisions

If foundational models become capable of native, highly reliable multi-step planning with guaranteed tool execution constraints (e.g., guaranteed safety gates), the orchestration layer could be simplified. However, the logical separation of concerns will remain.
