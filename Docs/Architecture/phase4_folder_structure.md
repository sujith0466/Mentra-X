# Phase 4 Folder Structure (Proposed)

The following structure is proposed for the implementation of Mastra Cognitive Swarm. It completely isolates the orchestrator, runtime, tools, and context building from the existing business logic.

```text
backend/
└── services/
    └── orchestration/            # NEW: Mastra Orchestration Layer
        ├── __init__.py
        ├── orchestrator.py       # Mastra entry point / DAG router
        ├── context_builder.py    # Synchronous context gatherer
        ├── runtime/              # NEW: Agent Runtime Layer
        │   ├── __init__.py
        │   ├── runtime.py        # Central execution lifecycle
        │   ├── execution_manager.py
        │   ├── workflow_store.py # NEW: Workflow state persistence and observability
        │   ├── retry_policy.py
        │   ├── timeout_policy.py
        │   ├── circuit_breaker.py# NEW: Fault tolerance documentation
        │   ├── rate_limiter.py   # NEW: Concurrency limits documentation
        │   ├── budget_manager.py # NEW: Token/Cost management documentation
        │   ├── telemetry.py
        │   └── event_bus.py      # Internal Event Bus
        ├── tools/                # Swarm Tool Registry
        │   ├── __init__.py
        │   ├── registry.py       # Tool definitions (SOT)
        │   ├── twin_tools.py
        │   ├── memory_tools.py
        │   └── assessment_tools.py
        ├── agents/               # Mastra Agent Definitions
        │   ├── __init__.py
        │   ├── registry.py       # NEW: Plugin-based Agent Registry
        │   ├── tutor_agent.py
        │   ├── memory_agent.py
        │   ├── assessment_agent.py
        │   ├── verification_agent.py
        │   ├── insight_agent.py
        │   └── weakness_agent.py
        └── state/
            ├── __init__.py
            └── execution_context.py

backend/
└── routes/
    └── mastra_routes.py          # NEW: Chat entry point for the swarm

backend/
└── services/
    └── twin/
        ├── twin_facade.py        # NEW/REFACTOR: Strict facade for agents
```
