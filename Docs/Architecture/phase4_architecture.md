# Phase 4: Mastra Cognitive Swarm Architecture

## 1. Core Paradigm
Mastra acts exclusively as the **Orchestration Layer**. It replaces zero existing features. Instead, it coordinates the existing LMS, Digital Twin, Assessment, and Memory engines by passing them context and requesting tool execution.

## 2. Layered Architecture

```text
[ Browser / Frontend ]
          ↓
[ Mastra Orchestrator ] 
   (Cognitive Swarm)
          ↓
[ Agent Runtime ] -> Execution lifecycle, workflow state, telemetry
          ↓
[ Agent Registry ] -> Dynamic Plugin-based Agents
          ↓
[ Tools ] -> Mastra integrations
          ↓
[ Core Facades ]
  ├── TwinFacade
  ├── AssessmentFacade
  └── MemoryFacade
          ↓
[ Core Services ]
  ├── TwinMutator
  ├── BayesianEstimator
  └── QdrantRetriever
          ↓
[ Database / Repositories ]
  ├── MySQL (Truth)
  └── Qdrant (Semantic)
```

## 3. Communication Strategy & Internal Event Bus
- **Downward Only**: Agents call Facades. Facades call Services. Services call Repositories.
- **Event Bus Decoupling**: Agents emit events to an internal Event Bus. The Event Bus fans out these events to Twin, Memory, Insights, Analytics, etc.
- **Event Classification**:
  - **Domain Events**: `TwinUpdated`, `MemoryStored`, `AssessmentCompleted`
  - **System Events**: `WorkflowStarted`, `WorkflowCompleted`, `RetryTriggered`, `TimeoutOccurred`
  - **Telemetry Events**: `AgentLatency`, `ToolLatency`, `TokenUsage`, `EmbeddingGenerated`
- **Event Idempotency**: Every event strictly enforces idempotency to prevent duplicate mutations. Event payloads must include:
  - `event_id`
  - `workflow_id`
  - `idempotency_key`
  - `timestamp`
  - `event_version`
  - `source_agent`

## 4. Agent Runtime Layer & Workflow State
The Runtime centrally handles:
- **Execution & Policies**: Retries, timeouts, circuit breakers, rate limiting, and budget management.
- **Workflow State Store**: A dedicated store for workflow recovery, resumable execution, and observability. It maintains:
  - `workflow_id`
  - `workflow_status`
  - `current_step`
  - `completed_steps`
  - `current_agent`
  - `started_at`
  - `updated_at`
  - `execution_events`
  - `retry_count`
  - `error_context`

## 5. Observability & Telemetry (OpenTelemetry Ready)
Every orchestration action produces standardized distributed traces. Telemetry payloads include:
- `trace_id`
- `span_id`
- `parent_span_id`
- `workflow_id`
- `agent_id`
- `tool_id`
- `execution_time`

## 6. Integration Strategy
- **Authentication**: Mastra endpoints are guarded by `@student_required`. The Orchestrator automatically inherits the `user_id`.
- **Context Loading**: The Orchestrator calls the `ContextBuilder` which synchronously fetches Twin profiles, ongoing Assessment states, and Qdrant memory context *before* any agent is invoked.
- **Plugin Registry**: Agents are registered dynamically (via an Agent Registry) requiring zero orchestrator changes when adding future capabilities (like Enkrypt Safety in Phase 6).
