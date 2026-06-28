# ADR-004: Mastra as Multi-Agent Orchestration Framework

**Status:** ACCEPTED  
**Date:** 2026-06-28  
**Author:** Sujith Kumar AI  
**Context Phase:** Phase 4 (Cognitive Swarm)

---

## Context

Mentra X's educational AI architecture is too complex for a single LLM prompt. The system must simultaneously:
1. Retrieve semantic memory from 4 Qdrant collections.
2. Select an adaptive teaching strategy based on Learning DNA.
3. Generate educational content.
4. Pass content through a rigorous 4-stage safety validation (Enkrypt).
5. Generate comprehension quizzes to verify understanding.
6. Analyze long-term weakness clusters across sessions.

Executing this in a single prompt leads to context overflow, prompt confusion (the model forgets safety rules while teaching), and makes it impossible to implement loops (like regenerating failed content) or parallel execution (like querying Qdrant while generating the initial response structure).

## Problem Statement

How should the multi-agent AI system be orchestrated? The system requires:
- Directed Acyclic Graph (DAG) workflow definition.
- Parallel tool execution (to meet the <3s latency target).
- Cron-like scheduling for the Weakness Intelligence Agent.
- Strictly typed input/output contracts between agents.
- Human-in-the-Loop (HITL) capability for Enkrypt hard fails.

## Decision

We will use **Mastra** as the core agent orchestration framework.

Mastra provides native DAG capabilities, strong typing via Pydantic/Zod schemas, parallel node execution, and built-in hooks for observability. It allows us to treat agents as distinct state machines rather than just chained prompts.

## Alternatives Considered

| Framework | DAG Support | Parallel Execution | Typed Contracts | Pros | Cons |
|---|---|---|---|---|---|
| **Mastra** (Selected) | Native | Native | Native (Pydantic) | Excellent for production state machines, lightweight | Newer ecosystem |
| **LangChain/LangGraph** | Yes | Complex | Yes | Huge ecosystem | Extremely bloated, rapid breaking changes, high abstraction overhead |
| **LlamaIndex** | Partial | Partial | Yes | Great for RAG | Not designed for complex multi-agent state machines |
| **AutoGen** | Conversational | No | Weak | Good for conversational agents | Unpredictable execution flow, hard to guarantee safety pipeline |
| **CrewAI** | Sequential/Hierarchical | Partial | Partial | Easy to set up | Too rigid for complex conditional loops (like Enkrypt regeneration) |
| **Custom Python Script** | Manual | Manual (`asyncio`) | Manual | Total control | Re-inventing the wheel for state management and retries |

## Pros

- **Predictable Execution:** DAG architecture guarantees that Enkrypt validation runs *before* content reaches the user, every single time.
- **Latency:** Mastra's native parallel execution allows the Memory Agent to query 4 Qdrant collections simultaneously in ~80ms instead of ~300ms.
- **Type Safety:** Agent outputs are validated against Pydantic schemas before being passed to the next agent, preventing cascading hallucination errors.
- **Observability:** Easy to attach the `ObservabilityLogger` to Mastra's execution hooks to trace token usage and latency per node.

## Cons

- Mastra is a newer framework compared to LangChain, meaning fewer community tutorials and stack overflow answers.
- Requires strict adherence to schema definitions, slowing down initial prototyping compared to raw string passing.

## Trade-offs

We are trading the massive pre-built tool ecosystem of LangChain for the predictable, production-grade state management of Mastra. Given that Mentra X relies on custom educational tools (Qdrant, Enkrypt) rather than generic tools (Google Search, Calculator), the pre-built ecosystem is less valuable to us than execution reliability.

## Consequences

- All AI features from Phase 4 onward must be implemented as Mastra Agents and Mastra Tools.
- Developers must learn Mastra's DAG definition syntax.
- Legacy chatbot (`ai_routes.py`) will run completely separate from the Mastra swarm until deprecated.

## Future Revisions

This decision should be reconsidered if Mastra introduces breaking changes that threaten production stability, or if Python's native `asyncio` ecosystem develops a standard lightweight DAG orchestrator that removes the need for third-party dependencies.
