# Mentra X — AI Observability Architecture

**Version:** 1.0  
**Owner:** Sujith Kumar AI  
**Active From:** Phase 4 (Mastra Cognitive Swarm)

---

## Overview

Observability in Mentra X is not a Phase 10 add-on — it is built into every agent interaction from Phase 4 onwards. Every AI decision must be traceable, every agent execution must be measurable, and every Twin mutation must be auditable.

### Why Observability from Phase 4

| Without Observability | With Observability |
|---|---|
| "The AI gave a wrong answer" — cannot investigate | Trace exact Tutor Agent prompt, Enkrypt scores, level selected |
| "The student's twin seems wrong" — cannot diagnose | View exact mutations with before/after values + agent that caused them |
| "The system is slow" — cannot pinpoint | Per-tool execution timing reveals which step is the bottleneck |
| "The weakness detection didn't fire" — cannot debug | Cron execution log shows session count, cluster results, plan generated |

---

## Observability Dimensions

### 1. Agent Execution Tracing

Every agent execution is captured as a structured `AgentTrace` object:

```python
@dataclass
class AgentTrace:
    # Identity
    trace_id: str                    # UUID per agent invocation
    session_id: str                  # Parent session
    user_id: str
    agent_name: str                  # "MemoryAgent" | "TutorAgent" | etc.
    timestamp_start: datetime
    timestamp_end: datetime

    # Timing
    total_duration_ms: int
    tool_durations_ms: dict[str, int]  # tool_name → duration
    llm_latency_ms: int | None         # None if no LLM call in this agent

    # LLM Usage
    prompt_id: str | None              # From prompt versioning system
    prompt_version: str | None
    input_tokens: int | None
    output_tokens: int | None
    llm_model: str | None

    # Memory
    qdrant_queries: list[QdrantQueryTrace]  # Each Qdrant query with timing
    memories_retrieved: int
    cache_hit: bool | None             # Redis cache hit for learning_dna

    # Enkrypt (if applicable)
    enkrypt_math_score: float | None
    enkrypt_science_score: float | None
    enkrypt_hallucination_score: float | None
    enkrypt_pedagogy_score: float | None
    enkrypt_composite: float | None
    enkrypt_action: str | None         # "APPROVE" | "REGENERATE" | "HARD_FAIL"
    enkrypt_retries: int

    # Twin
    twin_mutations: list[TwinMutationTrace]  # Each mutation in this agent
    twin_version_before: int | None
    twin_version_after: int | None

    # Teaching
    teaching_level_selected: int | None
    teaching_level_rationale: str | None  # Why this level was chosen
    avoided_strategies: list[str]

    # Result
    status: str                  # "success" | "partial" | "fallback" | "error"
    error_code: str | None       # e.g., "ENKRYPT_005"
    fallback_used: bool
```

### 2. Qdrant Query Tracing

```python
@dataclass
class QdrantQueryTrace:
    collection: str              # "learning_dna" | "past_doubts" | etc.
    query_type: str              # "get" | "search" | "upsert"
    duration_ms: int
    results_count: int
    top_score: float | None      # Cosine similarity of top result
    filter_used: str             # e.g., "user_id=aryan_001"
    cache_hit: bool
```

### 3. Twin Mutation Tracing

```python
@dataclass
class TwinMutationTrace:
    concept: str | None
    field: str                   # e.g., "mastery_per_concept.thermodynamics.entropy"
    old_value: Any
    new_value: Any
    mutation_type: str           # "verification_pass" | "decay" | "assessment"
    twin_version: int            # version AFTER this mutation
```

---

## ObservabilityLogger

```python
class ObservabilityLogger:
    """
    Central observability writer.
    Writes to:
    - MongoDB (mentra_ai.agent_traces collection) — full structured trace
    - application log — human-readable summary
    - MySQL ai_sessions table — latency columns
    """

    def log_agent_trace(self, trace: AgentTrace) -> None:
        # 1. Write full trace to MongoDB
        if feature_flags.ENABLE_OBSERVABILITY:
            self.mongo.agent_traces.insert_one(asdict(trace))

        # 2. Write summary to application log
        logger.info(
            f"Agent trace: {trace.agent_name}",
            extra={
                "trace_id": trace.trace_id,
                "session_id": trace.session_id,
                "agent": trace.agent_name,
                "duration_ms": trace.total_duration_ms,
                "status": trace.status,
                "enkrypt_composite": trace.enkrypt_composite,
                "twin_mutations": len(trace.twin_mutations),
                "memories_retrieved": trace.memories_retrieved,
                "cache_hit": trace.cache_hit
            }
        )

        # 3. Update latency columns in ai_sessions
        if trace.agent_name == "MemoryAgent":
            db.session.execute(
                text("UPDATE ai_sessions SET memory_retrieval_ms=:ms WHERE session_id=:sid"),
                {"ms": trace.total_duration_ms, "sid": trace.session_id}
            )

    def log_session_summary(self, session_id: str) -> None:
        """Called after full DAG completes. Summarizes all agent traces for session."""
```

---

## Observability Metrics

### Key Metrics Tracked (per session)

| Metric | Source | Target |
|---|---|---|
| Memory Agent total duration | `AgentTrace.total_duration_ms` | < 150ms p95 |
| Qdrant learning_dna retrieval | `QdrantQueryTrace.duration_ms` | < 30ms p95 |
| Qdrant past_doubts search | `QdrantQueryTrace.duration_ms` | < 50ms p95 |
| Redis cache hit rate | `QdrantQueryTrace.cache_hit` | > 85% |
| LLM response time | `AgentTrace.llm_latency_ms` | < 2000ms p95 |
| Enkrypt validation time | `AgentTrace` tool duration | < 500ms p95 |
| Total session E2E | Sum of all agent durations | < 3000ms p95 |
| Enkrypt approval rate | `enkrypt_action == "APPROVE"` | > 90% |
| Enkrypt hard fail rate | `enkrypt_action == "HARD_FAIL"` | < 2% |
| Twin mutations per session | `len(twin_mutations)` | 2–5 expected |
| Token usage per session | `input_tokens + output_tokens` | Monitor for cost |

### Aggregated Metrics (daily rollup)

```python
class MetricsAggregator:

    def compute_daily_metrics(self, date: date) -> DailyMetrics:
        return DailyMetrics(
            date=date,
            total_sessions=...,
            unique_students=...,
            avg_response_ms=...,
            p95_response_ms=...,
            enkrypt_approval_rate=...,
            enkrypt_hard_fail_count=...,
            avg_enkrypt_confidence=...,
            total_twin_mutations=...,
            total_tokens_used=...,
            cache_hit_rate=...,
            fallback_served_count=...,
            hitl_flags_raised=...
        )
```

---

## Observability Dashboard: `/admin/observability`

### Tab 1: Live Agent Feed

Real-time feed of agent traces (last 100 executions):

```
[14:32:01] MemoryAgent       sess_xyz  user_101  92ms   ✅
[14:32:01] TutorAgent        sess_xyz  user_101  1840ms ✅ Level 4 | Enkrypt: 0.96
[14:32:02] VerificationAgent sess_xyz  user_101  45ms   ✅ PASS | mastery: 0.00→0.05
[14:31:55] MemoryAgent       sess_abc  user_204  87ms   ✅ (cache hit)
[14:31:54] TutorAgent        sess_abc  user_204  2100ms ⚠️ Level 2→4 escalation
[14:31:54] EnkryptValidator  sess_abc  user_204  430ms  🔄 REGENERATE (science: 0.30)
```

### Tab 2: Session Trace Viewer

Select any session → view full trace breakdown:

```
Session: sess_xyz | User: Aryan | 2026-06-28 14:32:01

MEMORY AGENT (92ms)
  ├─ fetchLearningDNA     learning_dna     12ms  (cache HIT)
  ├─ retrievePastDoubts   past_doubts      34ms  3 results, top score: 0.87
  ├─ getExplanationHistory explanation_history 28ms  2 results, top score: 0.91
  └─ getWeakConcepts      weak_concepts    18ms  1 result (CRITICAL: Carnot)

  Context assembled: level=4, avoid=[Level 2], weakness=HIGH

TUTOR AGENT (1840ms)
  ├─ selectExplanationLevel  2ms  → Level 4 (Visual Analogy)
  │   Rationale: Level 2 failed on 2026-06-20; CRITICAL weakness; frustration=0.23
  ├─ generateExplanation     1780ms  Prompt: tutor/v1.2.0_level4_visual
  │   Tokens: 284 in + 421 out | Model: gpt-4o-mini
  └─ callEnkryptValidation   430ms  → APPROVE (0.963)
      Math: N/A | Science: 0.95 | Hallucination: 0.98 | Pedagogy: 0.97

VERIFICATION AGENT (45ms)
  ├─ generateMicroQuiz       38ms
  ├─ [waiting for student answer]
  ├─ evaluateAnswer          7ms  → 0.89 (PASS, threshold 0.75)
  └─ mutateKnowledgeState    12ms
      thermodynamics.entropy: 0.00 → 0.05
      preferred_level: 2 → 4
      twin_version: 15 → 16

TOTAL: 1977ms ✅
```

### Tab 3: Enkrypt Safety Monitor

- Distribution chart: Enkrypt composite score across all sessions
- Hard fail log with original output (admin only)
- Validator breakdown: which validator fails most frequently
- Subject breakdown: which subjects produce most rejections

### Tab 4: Performance Metrics

- Response time trends (24h, 7d, 30d)
- Cache hit rate trends
- Token usage and estimated cost
- Slowest sessions (sorted by total_duration_ms)

### Tab 5: Twin Mutations Log

- Latest twin mutations across all users
- Filter by: concept, mutation_type, agent_name, date
- "Suspicious mutation" alerts (mastery drop > 0.30 in single session)

---

## Prompt Observability

Every LLM call logs its prompt version:

```python
logger.info(
    "LLM call executed",
    extra={
        "prompt_id": "TUTOR_LEVEL_4_VISUAL",
        "prompt_version": "1.2.0",
        "template_variables": {
            "concept": "thermodynamics.entropy",
            "mastery": 0.00,
            "avoided_analogies": ["carnot_cycle"],
            "worked_analogies": []
        },
        "input_tokens": 284,
        "output_tokens": 421,
        "latency_ms": 1780
    }
)
```

This enables **prompt version performance analysis** — compare Enkrypt approval rates across prompt versions to detect regressions.

---

## Adding Observability to a New Agent

When creating a new Mastra agent tool, wrap it with the observability decorator:

```python
from backend.monitoring.observability import trace_agent_tool

@trace_agent_tool(agent_name="TutorAgent", tool_name="generateExplanation")
def generate_explanation(concept: str, level: int, context: HydratedContext) -> str:
    """Generates explanation at specified level using context."""
    ...
    # Timing, logging, and trace recording handled automatically by decorator
```
