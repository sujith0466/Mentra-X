# Phase 4 Context Builder Design

## 1. Purpose
The Context Builder acts as a synchronous pre-processor for the Mastra Orchestrator. Before a user query is sent to any LLM, the Context Builder retrieves state from isolated Facades and constructs a single, immutable `UnifiedContext` object. This prevents redundant database queries by individual agents.

## 2. Context Structure
The Unified Context is logically split into three sections:

### 2.1 StaticContext
Metadata that rarely changes during a single session:
- **User**: User ID, Name, Level, Total XP.
- **Digital Twin**: Continuous state variables (Frustration Index, Skill Mastery).
- **Learning DNA**: Persistent learning style preferences stored in Qdrant.

### 2.2 DynamicContext
State that fluctuates rapidly based on immediate activity:
- **Assessment**: Currently active quizzes, last quiz score, or Bayesian estimation tracks.
- **Memory**: The most semantically relevant vectors from Qdrant based on the user's latest query, and recent session short-term history.
- **Weak Concepts**: Structurally tagged areas of struggle.
- **Opportunity State**: Curated next-best-actions based on current progress.

### 2.3 ExecutionContext
Metadata strictly managed by the Agent Runtime Layer:
- **Workflow Metadata**: `workflow_id`, `current_agent`, `attempt_number`.
- **Runtime Metadata**: Current timeout budgets, retry counts.
- **Trace Metadata**: `trace_id`, `span_id`, timestamps (for OpenTelemetry).

## 3. The Unified Context Object (JSON Schema)

```json
{
  "static_context": {
    "user": {
      "id": 42,
      "name": "Alex",
      "level": 5
    },
    "twin": {
      "version": "1.4",
      "frustration_index": 0.2,
      "mastered_skills": ["Python", "SQL"]
    },
    "learning_dna": "Prefers visual analogies over mathematical formulas."
  },
  "dynamic_context": {
    "assessment": {
      "active_session_id": null,
      "last_quiz_score": 85.0
    },
    "memory": {
      "recent_doubts": ["What is a decorator?", "Why did my SQL query timeout?"]
    },
    "weak_concepts": ["Generators", "Window Functions"],
    "opportunity_state": {
      "next_best_action": "Review Python Generators module"
    }
  },
  "execution_context": {
    "workflow_metadata": {
      "workflow_id": "wf_123456789",
      "current_agent": "TutorAgent",
      "attempt_number": 1
    },
    "runtime_metadata": {
      "timeout_budget_ms": 5000,
      "retry_count": 0
    },
    "trace_metadata": {
      "trace_id": "trace_abcdef",
      "span_id": "span_12345",
      "timestamp": "2026-07-01T10:00:00Z"
    }
  }
}
```

> [!IMPORTANT]
> The `UnifiedContext` remains strictly **immutable** during execution. Agents cannot alter this state in memory; any state change must be emitted as an event through the Event Bus.

## 4. Execution Flow
`Orchestrator` -> `ContextBuilder.build(user_id, prompt, workflow_id)` -> `TwinFacade`, `MemoryFacade`, `AssessmentFacade` -> `UnifiedContext` -> `Agent Runtime` -> `Mastra Agent`.
