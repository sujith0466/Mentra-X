# Mentra X — Complete System Architecture Overview

**Project:** Mentra X  
**Track:** Student Doubt-Solving & Learning Agent  
**Version:** 1.0 — Round 1 Submission

---

## 1. Architecture Philosophy

Mentra X is built on three fundamental architectural principles:

1. **Memory-Native:** Every component exists to serve the Student Digital Twin. No interaction is ephemeral.
2. **Agent-Native:** Intelligence is not concentrated in a single LLM call. It is distributed across specialized Mastra agents that collaborate through structured graph workflows.
3. **Safety-First:** No output reaches a student without passing through the Enkrypt AI validation middleware. In high-stakes academic domains, hallucinations are unacceptable.

---

## 2. High-Level System Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                 │
│  Mentra Study Dashboard │ Cognitive Chat UI │ LMS Video Player       │
└──────────────┬───────────────────────────────────────────────────────┘
               │ HTTPS REST / WebSocket
┌──────────────▼───────────────────────────────────────────────────────┐
│                      FLASK API GATEWAY                               │
│  Authentication │ Rate Limiting │ Session Management │ Route Guard   │
└──────────────┬───────────────────────────────────────────────────────┘
               │ Structured Request Payload
┌──────────────▼───────────────────────────────────────────────────────┐
│                   MASTRA GRAPH ORCHESTRATOR                          │
│                    (The Cognitive Swarm Hub)                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────────┐   │
│  │ Memory   │  │ Tutor    │  │ Verify   │  │ Weakness Intel    │   │
│  │ Agent    │→ │ Agent    │→ │ Agent    │  │ Agent (Cron)      │   │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────────┘   │
│  ┌──────────┐  ┌──────────┐                                         │
│  │ Assess.  │  │ Insight  │                                         │
│  │ Agent    │  │ Agent    │                                         │
│  └──────────┘  └──────────┘                                         │
└──────┬────────────────────────────────────┬───────────────────────────┘
       │                                    │
┌──────▼──────────┐              ┌──────────▼────────────────────────┐
│  QDRANT LAYER   │              │     ENKRYPT SAFETY LAYER          │
│  Learning DNA   │              │  Math Validator │ Hallucination   │
│  Past Doubts    │              │  Detector       │ Confidence Score │
│  Session Logs   │              └───────────────────────────────────┘
│  Weak Concepts  │
└──────┬──────────┘
       │
┌──────▼──────────────────────────────────────────────────────────────┐
│                    RELATIONAL FOUNDATION (MySQL)                     │
│  Users │ Courses │ Enrollments │ Quiz Scores │ XP │ Portfolios      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Layer-by-Layer Breakdown

### 3.1 Frontend / Client Layer

**Components:**
- **Mentra Study Dashboard:** Displays real-time Learning DNA heatmap, subject-wise mastery scores, XP streaks, and pending weak-area revision tasks.
- **Cognitive Chat UI:** Conversational interface connected via WebSocket to the Mastra Orchestrator. Renders structured agent responses including explanations, micro-quizzes, and visual analogies.
- **LMS Video Player:** Existing Mentra LMS integration. Tracks watch-time per lesson and triggers contextual memory updates.

**Data Emitted:**
- `{user_id, doubt_text, subject_tag, session_id, current_page}`

---

### 3.2 Flask API Gateway

**Components:**
- JWT authentication and session validation.
- Request routing to the Mastra Orchestrator or legacy Mentra endpoints.
- Rate limiting per user tier.

**Key Endpoints:**
- `POST /api/v2/doubt` → Mastra Orchestrator entry
- `GET /api/v2/twin/{user_id}` → Digital Twin state read
- `GET /api/v2/report/{user_id}` → Weekly Insight Report

---

### 3.3 Mastra Graph Orchestrator

The Mastra Orchestrator is the central intelligence hub. It manages a Directed Acyclic Graph (DAG) of specialized agents:

**DAG Execution Order for Doubt Solving:**
```
Input → Memory Agent → Tutor Agent → Enkrypt Validator → Verification Agent → Output
```

**Parallel Async Workflow:**
```
Session End → Weakness Intelligence Agent (cron) → Qdrant Twin Update
```

---

### 3.4 Qdrant Memory Layer

Qdrant serves as the cognitive long-term memory. It stores:

| Collection | Content | Vector Model |
|---|---|---|
| `learning_dna` | Full Digital Twin JSON | text-embedding-3-small |
| `past_doubts` | Semantic doubt history | text-embedding-3-small |
| `explanation_history` | Teaching outcomes by level | text-embedding-3-small |
| `session_logs` | Raw session transcripts | text-embedding-3-small |
| `weak_concepts` | Clustered failure patterns | text-embedding-3-small |

---

### 3.5 Enkrypt Safety Layer

Enkrypt AI intercepts every Mastra Tutor Agent output before delivery:

| Validator | Domain | Action on Failure |
|---|---|---|
| Math Validator | JEE formulas, calculus steps | Block + Regenerate |
| Science Validator | NEET chemistry/biology facts | Block + Fallback |
| Factual Validator | UPSC history/governance | Warn + Badge |
| Pedagogy Evaluator | Teaching tone | Score penalty, not block |

**Confidence Threshold:**
- `Score > 0.90` → Pass, deliver to student.
- `Score 0.75–0.90` → Warn, deliver with yellow badge.
- `Score < 0.75` → Block, trigger Mastra regeneration loop.

---

### 3.6 Relational Foundation (MySQL)

The existing Mentra LMS database provides deterministic ground truth:

- **Users:** Identity, exam target, enrollment status.
- **Courses:** Chapter hierarchy, syllabus tags.
- **Quiz Scores:** Per-chapter performance for initial twin seeding.
- **XP Ledger:** Gamification state updated by agent interactions.

---

## 4. Core Data Flows

### 4.1 Doubt Resolution Flow
```
Student Doubt
    → Flask Gateway (auth, session)
    → Mastra Orchestrator
    → [PARALLEL] Memory Agent queries Qdrant (past_doubts, learning_dna)
    → Tutor Agent (hydrated with twin context)
    → [SERIAL] Enkrypt Safety Validation
    → Verification Agent (append micro-quiz)
    → Response to Student
    → [ASYNC] Qdrant state mutation (update past_doubts, session_logs)
```

### 4.2 Assessment Flow
```
New Student
    → Assessment Agent (adaptive branching via Mastra)
    → MySQL seeding from existing quiz scores
    → Initialize Digital Twin in Qdrant
    → Return to main learning loop
```

### 4.3 Memory Evolution Flow
```
Session Ends
    → Weakness Intelligence Agent (Mastra cron, every 5 sessions)
    → Query Qdrant session_logs (semantic clustering of failures)
    → Update weak_concepts collection
    → Mutate Digital Twin learning_dna
    → Push revision curriculum to MySQL/LMS dashboard
```
