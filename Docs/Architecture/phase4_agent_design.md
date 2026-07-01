# Phase 4 Agent Design Specifications

This document outlines the core agents that will make up the Mastra Cognitive Swarm.

---

## 1. Agent Registry (Plugin Architecture)

Instead of hardcoding agents into the Orchestrator DAG, Mastra will utilize a dynamic **Agent Registry**. This allows future agents (like Enkrypt Safety agents in Phase 6) to be integrated with zero orchestrator code changes.

### 1.1 Registry API
- `register_agent(agent_cls)`: Registers a new agent plugin at startup.
- `discover_agents()`: Returns a list of all currently available agents and their schemas.
- `agent_capabilities()`: Returns the list of tools and intents the agent can handle.
- `health_check()`: Pings the agent to ensure its underlying LLM provider (OpenRouter/Local) is responsive.

### 1.2 Agent Plugin Metadata
Every registered agent must define:
- `enabled`: `bool` (Allows feature-flagging agents on/off).
- `priority`: `int` (Determines conflict resolution in the Orchestrator).
- `version`: `str` (e.g., "1.0.0").

---

## 2. Assessment Agent
- **Purpose**: Facilitate Bayesian tracking, quiz generation, and adaptive testing flows.
- **Responsibilities**: Analyze student readiness, trigger quizzes via the LMS, and ingest score metrics.
- **Agent Policies**:
  - **Allowed Tools**: `start_assessment_session`, `submit_answer`
  - **Allowed Collections**: None
  - **Allowed Facades**: `AssessmentFacade`
  - **Max Tokens**: 2048
  - **Temperature**: 0.2
  - **Timeout**: 4000ms
  - **Retry Count**: 1
  - **Human Review Required**: False
  - **Fallback Behaviour**: Standard LLM qualitative quiz.
  - **Failure Policy**: Log error, alert Runtime.

---

## 3. Memory Agent
- **Purpose**: Recall past interactions, resolve recurring doubts, and surface learning DNA.
- **Responsibilities**: Vectorize queries, scan Qdrant, and format historical data into conversational context.
- **Agent Policies**:
  - **Allowed Tools**: `retrieve_semantic_memory`, `store_semantic_memory`
  - **Allowed Collections**: `learning_dna`, `past_doubts`, `explanation_history`, `session_logs`, `weak_concepts`
  - **Allowed Facades**: `MemoryFacade`
  - **Max Tokens**: 4096
  - **Temperature**: 0.3
  - **Timeout**: 3000ms
  - **Retry Count**: 2 (with exponential backoff)
  - **Human Review Required**: False
  - **Fallback Behaviour**: Stateless answering without semantic memory.
  - **Failure Policy**: Proceed without memory context.

---

## 4. Tutor Agent
- **Purpose**: Direct pedagogical interaction. Explaining concepts, providing analogies, scaffolding knowledge.
- **Responsibilities**: Conversational learning, leveraging the Twin and Memory contexts to personalize the explanation.
- **Agent Policies**:
  - **Allowed Tools**: None
  - **Allowed Collections**: None
  - **Allowed Facades**: None
  - **Max Tokens**: 4096
  - **Temperature**: 0.6
  - **Timeout**: 8000ms
  - **Retry Count**: 1
  - **Human Review Required**: False
  - **Fallback Behaviour**: Base foundational explanation.
  - **Failure Policy**: Abort generation if validation fails.

---

## 5. Verification Agent
- **Purpose**: Ensure safety, accuracy, and pedagogical correctness of all Swarm outputs.
- **Responsibilities**: Intercept outputs from the Tutor/Memory/Assessment agents and apply deterministic rule checks. Emits `VerificationPassed` or `VerificationFailed` events.
- **Agent Policies**:
  - **Allowed Tools**: None
  - **Allowed Collections**: None
  - **Allowed Facades**: None
  - **Max Tokens**: 1024
  - **Temperature**: 0.0
  - **Timeout**: 2000ms
  - **Retry Count**: 0
  - **Human Review Required**: False
  - **Fallback Behaviour**: Default to passing the response (fail-open) if model times out.
  - **Failure Policy**: Log `Safety Timeout` and pass.

---

## 6. Weakness Intelligence Agent
- **Purpose**: Continuously scan the Digital Twin and Assessment logs for struggling concepts.
- **Responsibilities**: Identify knowledge gaps proactively before the student asks. Emits `WeakConceptDetected` events.
- **Agent Policies**:
  - **Allowed Tools**: `get_digital_twin`
  - **Allowed Collections**: None
  - **Allowed Facades**: `TwinFacade`
  - **Max Tokens**: 2048
  - **Temperature**: 0.1
  - **Timeout**: 5000ms
  - **Retry Count**: 3
  - **Human Review Required**: False
  - **Fallback Behaviour**: Fails silently (background async agent).
  - **Failure Policy**: Drop analysis cycle.

---

## 7. Insight Agent
- **Purpose**: Generate high-level learning insights and recommendations for the student dashboard.
- **Responsibilities**: Digest the week's activity and formulate a motivational summary and next steps. Emits `InsightGenerated` events.
- **Agent Policies**:
  - **Allowed Tools**: `generate_weekly_insight`
  - **Allowed Collections**: None
  - **Allowed Facades**: `TwinFacade`, `AssessmentFacade`
  - **Max Tokens**: 1500
  - **Temperature**: 0.4
  - **Timeout**: 6000ms
  - **Retry Count**: 1
  - **Human Review Required**: False
  - **Fallback Behaviour**: Dashboard hides the widget.
  - **Failure Policy**: Silent drop.
