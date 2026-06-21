---
title: Mentra X - Product Requirements Document
---

<div style="text-align: center; margin-top: 200px;">
  <h1>MENTRA X</h1>
  <h2>Product Requirements Document (PRD)</h2>
  <h3>AI-Powered Student Digital Twin</h3>
  <br/>
  <h4>Built By:<br/>Sujith Kumar AI</h4>
  <br/>
  <p>Track: Student Doubt-Solving & Learning Agent</p>
  <p>HiDevs × Mastra Hackathon 2026</p>
</div>

<div style="page-break-after: always;"></div>

## Table of Contents
1. Executive Summary
2. Problem Statement
3. Solution Summary
4. Target Users
5. User Journey
6. Student Digital Twin
7. Learning DNA
8. Features & Success Metrics
9. Future Vision

<div style="page-break-after: always;"></div>

# 1. Executive Summary
# Mentra X — Executive Summary

**One-page briefing for hackathon judges.**

---

## Problem

Over **2.5 million students** in India prepare annually for the most competitive exams on Earth — JEE, NEET, UPSC, CAT. The failure rate exceeds 95%. The most critical gap is not access to content — it is access to a tutor who *remembers* them. Every AI tool available today forgets the student the moment their session ends. Every explanation is generic. Every hallucinated formula reaches them unchecked. Weakness compounds silently until exam day.

---

## Solution: Mentra X

Mentra X is the world's first **AI-powered Student Digital Twin** platform. It creates a living, persistent cognitive model of every student — and deploys a swarm of Mastra AI agents to teach them exactly the way they learn, verify that they understood, track every weakness, and generate personalized revision plans. Automatically. After every session. Forever.

**Tagline:** *The tutor that never forgets.*

---

## Architecture

Mentra X is built on three pillars and one foundation:

| Pillar | Technology | Role |
|---|---|---|
| **Intelligence** | Mastra AI | 6-agent Cognitive Swarm, DAG orchestration, cron workflows |
| **Memory** | Qdrant | Student Digital Twin, Stateful Memory RAG, 5 collections |
| **Safety** | Enkrypt AI | Math validation, hallucination detection, confidence scoring |
| **Foundation** | Mentra LMS (MySQL) | Courses, quizzes, XP, portfolios, skill graph |

---

## The Mentra Cognitive Swarm (Mastra)

Six specialized agents operate via a Mastra Directed Acyclic Graph:

1. **Assessment Agent** — Adaptive diagnostic calibration.
2. **Memory Agent** — Fetches the student's Digital Twin from Qdrant (parallel, 4 collections).
3. **Tutor Agent** — Delivers explanations at 1 of 5 teaching levels, calibrated to Learning DNA.
4. **Verification Agent** — Appends a comprehension micro-quiz; mutates the twin on result.
5. **Weakness Intelligence Agent** — Mastra cron-workflow; fires every 5 sessions to cluster failures.
6. **Insight Agent** — Generates weekly progress and revision reports.

**14 registered Mastra Tools. Human-in-the-Loop support included.**

---

## The Student Digital Twin (Qdrant)

Each student's twin lives in Qdrant across 5 vector collections. At the core is the **Learning DNA** — a behavioral vector encoding mastery scores per concept, preferred teaching level, frustration tolerance, and analogy effectiveness history. The twin mutates after every interaction. Concept decay is modeled via the Ebbinghaus Forgetting Curve. Memory is permanent. Context is total.

**Stateful Memory RAG — not document search, but human memory as vectors.**

---

## Safety Layer (Enkrypt AI)

Four Enkrypt validators — Mathematical Accuracy, Science Fact, Hallucination Detection, Pedagogy — score every Tutor Agent output. Responses below 0.90 confidence trigger an automatic Mastra regeneration loop. Double failures fall back to pre-verified textbook content. **Zero hallucinations reach the student.**

---

## Innovation

| What We Did | Why It Matters |
|---|---|
| Student Digital Twin in Qdrant | No competitor has persistent per-student cognitive memory |
| Learning DNA mutation per session | Teaching adapts to the individual, not just the topic |
| Enkrypt as mandatory middleware | First EdTech architecture with mathematical safety guarantees |
| Mastra cron-workflow for weakness detection | Asynchronous intelligence without user friction |
| Built on production Mentra LMS | Real data, real users — not a demo |

---

## Impact

- **Target:** 2.5M+ competitive exam aspirants (India) — scalable globally.
- **Measurable outcome:** +40% concept mastery improvement in 30 days (projected).
- **Safety guarantee:** < 1% hallucination rate (enforced by Enkrypt).
- **Market:** ₹12,000 crore ($1.5B) Indian EdTech market.

---

## Competitive Advantage

Replicating Mentra X requires Mastra (multi-agent orchestration) + Qdrant (vector memory) + Enkrypt (educational safety) + production LMS (relational ground truth) + months of integration engineering. It cannot be replicated with a single API call. The architectural moat is the combination, not any single component.

---

> **Mentra X — AI-Powered Student Digital Twin & Adaptive Learning Agent**  
> *Built by Sujith Kumar AI | HiDevs × Mastra Hackathon 2026*


<div style="page-break-after: always;"></div>

# 2. Solution Summary
# Mentra X — Solution Summary

**Project:** Mentra X  
**Challenge Track:** Student Doubt-Solving & Learning Agent  
**Tagline:** AI-Powered Student Digital Twin & Adaptive Learning Agent

---

## The Hook: 2.5 Million Students. Zero Memory.

Every year, 2.5 million students in India stake years of their lives — and their families' hopes — on a single exam. JEE. NEET. UPSC. CAT. The difference between clearing and failing is often one weak topic that was never properly reinforced. The AI tools that exist today fail these students not because they lack intelligence, but because they have **zero memory**. Every session starts from scratch. Every explanation is generic. Every hallucinated formula goes undetected. And every weakness is invisible until exam day.

**This is the $12 billion problem Mentra X solves.**

---

## The Solution: A Tutor That Never Forgets

Mentra X deploys the **Mentra Cognitive Swarm** — a graph of six specialized Mastra AI agents — backed by a persistent **Student Digital Twin** whose cognitive memory lives permanently in Qdrant, and whose every output is mathematically validated by Enkrypt AI before reaching the student.

This is not a chatbot. It is the first AI system that builds a **permanent model of a student's academic mind** — and uses that model to teach them the way only they can learn.

---

## The Architecture: Three Technologies. One Unbreakable System.

**Mastra (The Brain):** Six specialized agents orchestrated via a Directed Acyclic Graph — Memory Agent, Tutor Agent, Verification Agent, Assessment Agent, Weakness Intelligence Agent, and Insight Agent. Each agent has a defined role, typed inputs and outputs, and 14 registered Mastra Tools. The Weakness Intelligence Agent runs as a Mastra cron-workflow, firing automatically after every 5 student sessions to detect failure patterns without interrupting the real-time tutoring experience. No monolithic prompt. No single point of intelligence failure.

**Qdrant (The Memory):** Five purpose-built vector collections — `learning_dna`, `past_doubts`, `explanation_history`, `session_logs`, `weak_concepts` — store the student's entire cognitive history as 1536-dimensional embeddings. When a student asks about entropy, Qdrant tells the Tutor Agent: *"This student asked this exact concept before. Visual analogies worked. Step-by-step proofs failed."* This is **Stateful Memory RAG** — not document search, but human memory modeled as vectors. Concept decay is modeled using the Ebbinghaus Forgetting Curve, automatically degrading mastery scores for concepts not reviewed within their retention window.

**Enkrypt (The Truth):** In high-stakes exams, a hallucinated formula is catastrophic. Enkrypt AI intercepts every Tutor Agent output through four validation pipelines: Mathematical Accuracy, Science Fact Validation, Hallucination Detection, and Pedagogical Quality. A weighted confidence score is computed; anything below 0.90 triggers an automatic Mastra regeneration loop. Hard failures fall back to pre-verified textbook content. **Zero hallucinations reach the student.**

---

## The Innovation: Learning DNA

At the core of every Digital Twin is the student's **Learning DNA** — a behavioral vector encoding their preferred explanation style (Visual, Mathematical, Narrative), frustration tolerance, analogy effectiveness history, and engagement patterns. The DNA mutates after every interaction. When Aryan failed a Level 2 mathematical proof about entropy, his DNA updated: *preferred_level → 4, visual_scenarios → +0.05*. His next session opened with a LEGO analogy. He passed the verification quiz. His mastery score climbed.

**This is not personalization. This is cognitive modeling.**

---

## Why This Architecture Is Difficult to Replicate

Competitors cannot replicate Mentra X with a prompt or a wrapper. The moat requires: a multi-agent Mastra graph (6 specialized agents with 14 tools), a 5-collection Qdrant vector architecture with stateful RAG, Enkrypt safety middleware with domain-specific educational validators, and the Mentra LMS as the relational foundation. Built on top of an existing platform serving 31 active users across 34 MySQL tables — this is not a demo. This is a production system getting smarter with every session.

**Mentra X — The tutor that never forgets.**


<div style="page-break-after: always;"></div>

# 3. Product Requirements
# Mentra X — Product Requirements Document (PRD)

**Project:** Mentra X  
**Track:** Student Doubt-Solving & Learning Agent  
**Version:** 1.0 — Round 1 Submission  
**Date:** June 2026

---

## 1. Executive Summary

Mentra X is an AI-native, memory-persistent learning platform designed to serve millions of students preparing for India's most demanding competitive examinations — JEE, NEET, UPSC, CAT, and Board Exams. Built on the **Mentra Cognitive Swarm**, a graph of specialized Mastra AI agents, and powered by a **Student Digital Twin** that persists each student's unique **Learning DNA** in Qdrant vector memory, Mentra X is the first platform to deliver the intelligence, patience, and personalization of a world-class private tutor — at zero marginal cost per student.

Unlike existing AI tools that are stateless and generic, Mentra X builds a permanent cognitive model of every student. It remembers every doubt, every mistake, every analogy that worked, and every concept that decayed. It adapts its teaching style, escalates explanation depth, and validates every output for mathematical and factual accuracy using the Enkrypt AI safety layer.

The result is not a chatbot. It is a lifelong academic mentor that knows you better every single day.

---

## 2. Problem Statement

India produces over 2.5 million competitive exam aspirants annually. The gap between those who succeed and those who fail is almost entirely determined by access to high-quality, personalized guidance:

- **98% of students** cannot afford private tutors charging ₹5,000–₹50,000/month.
- **Generic AI tools** (ChatGPT, Gemini) provide identical, context-free answers regardless of the student's background, learning style, or history.
- **Static coaching apps** present the same video content regardless of what the student understood last week.
- **Doubt platforms** (Chegg, Doubtnut) answer questions in isolation, with zero longitudinal context or weakness tracking.

The core failure of existing solutions is not intelligence — it is **amnesia**. These tools forget the student the moment the session ends.

---

## 3. Why Existing Solutions Fail

| Failure Mode | Example | Impact |
|---|---|---|
| No persistent memory | Generic AI assistants | Student re-explains context every session |
| No weakness tracking | Static coaching apps | Weak concepts are never identified and reinforced |
| Hallucinated academic content | General LLMs | Wrong formulas, incorrect science facts |
| No comprehension verification | Chat-based doubt platforms | Student assumes understanding without confirmation |
| No adaptive teaching | Video-based MOOCs | Same explanation style regardless of student confusion |

---

## 4. Target Users

**Primary Users:**
- JEE Mains & Advanced aspirants (Grade 11–12, engineering track)
- NEET UG aspirants (Grade 11–12, medical track)
- UPSC CSE aspirants (Graduates, government service track)
- CAT/MBA aspirants (Graduates, management track)

**Secondary Users:**
- Board Exam students (Grade 10, 12)
- College students seeking supplementary learning

**Scale:** 50 million+ addressable students in India alone.

---

## 5. User Personas

### Persona 1 — Aryan, 17, JEE Advanced Aspirant
- Studies 10–12 hours daily.
- Strong in Mathematics, weak in Thermodynamics.
- Frustrated when AI gives the same explanation repeatedly despite not understanding.
- **Need:** Remembers his specific mistakes. Adapts after each failed attempt.

### Persona 2 — Priya, 23, UPSC CSE Aspirant
- Balances coaching, self-study, and mock tests.
- Struggles to retain historical timelines and policy frameworks.
- **Need:** Spaced repetition triggers, personalized revision based on forgetting curves.

### Persona 3 — Rohan, 25, CAT Aspirant
- Works a corporate job. Studies 2–3 hours at night.
- Weak in Verbal Reasoning, strong in Quant.
- **Need:** Quick doubt resolution before mock tests with strong accuracy guarantees.

---

## 6. User Journey

```
Student Joins Mentra X
       │
       ▼
Assessment Agent runs Adaptive Diagnostic
(Branching questions calibrated to JEE/NEET/UPSC difficulty)
       │
       ▼
Learning DNA is initialized in Qdrant
(Academic State, Knowledge State, Behavior Profile)
       │
       ▼
Student begins active learning (LMS + Chat Interface)
       │
       ▼
Student asks a doubt
       │
       ▼
Memory Agent retrieves Learning DNA from Qdrant
       │
       ▼
Tutor Agent generates adaptive explanation (Level 1–5)
       │
       ▼
Enkrypt validates accuracy (Math, Science, Pedagogy)
       │
       ▼
Verification Agent appends comprehension micro-quiz
       │
       ▼
Student responds → Digital Twin mutates in Qdrant
       │
       ▼
Every 5 sessions → Weakness Intelligence Agent generates report
       │
       ▼
Insight Agent delivers personalized revision curriculum
```

---

## 7. Product Vision

> *Mentra X is the first AI system that builds a permanent, living model of a student's academic mind — and uses that model to teach them the way only they can learn.*

We envision a future where the quality of a student's education is no longer determined by their postal code or their parents' income. Where every student in India has access to a tireless, infallible, deeply personalized tutor that understands their frustration, their cognitive style, and their weaknesses with precision no human tutor could match.

---

## 8. Functional Requirements

| ID | Feature | Priority |
|---|---|---|
| FR-01 | Adaptive Onboarding Diagnostic | P0 |
| FR-02 | Learning DNA initialization and persistence | P0 |
| FR-03 | Doubt-solving via Mastra Cognitive Swarm | P0 |
| FR-04 | Qdrant semantic memory retrieval | P0 |
| FR-05 | Enkrypt output validation per interaction | P0 |
| FR-06 | Adaptive Explanation Escalation (Levels 1–5) | P0 |
| FR-07 | Comprehension Verification micro-quiz | P1 |
| FR-08 | Weakness Intelligence Report (every 5 sessions) | P1 |
| FR-09 | Concept decay and spaced repetition triggers | P1 |
| FR-10 | Progress Report generation | P1 |
| FR-11 | XP and Streak gamification integration | P2 |
| FR-12 | Resume & Portfolio intelligence (existing Mentra) | P2 |

---

## 9. Non-Functional Requirements

- **Latency:** Doubt resolution P95 < 3 seconds end-to-end.
- **Accuracy:** Enkrypt-validated accuracy > 97% for math/science outputs.
- **Scalability:** Support 100,000 concurrent doubt sessions via horizontal Mastra worker scaling.
- **Memory Consistency:** Qdrant Digital Twin mutation must be idempotent and versioned.
- **Uptime:** 99.9% SLA for core tutoring pipeline.

---

## 10. Agent Ecosystem

| Agent | Role | Trigger |
|---|---|---|
| Assessment Agent | Initial diagnostic calibration | First login / new subject |
| Tutor Agent | Core adaptive doubt-solving | Every student query |
| Memory Agent | Qdrant RAG retrieval + context assembly | Pre-tutoring |
| Verification Agent | Comprehension micro-quiz injection | Post-explanation |
| Weakness Intelligence Agent | Recurring failure clustering | Every 5 sessions (cron) |
| Insight Agent | Progress report synthesis | Weekly / on demand |

---

## 11. Student Digital Twin

Every student in Mentra X is represented by a **Digital Twin** — a multi-dimensional, continuously evolving model stored in Qdrant vector memory. The twin integrates:

- **Relational sources:** MySQL quiz scores, course progress, XP.
- **Semantic sources:** Embedded doubt history, explanation outcomes, behavioral signals.
- **Decay modeling:** Concept retention curves that degrade mastery over time without reinforcement.

---

## 12. Learning DNA

The **Learning DNA** is the highest-value component of the Digital Twin. It is a structured vector payload encoding:

- Preferred explanation style (Visual / Mathematical / Narrative).
- Frustration tolerance index (determines when the agent skips guided reasoning and provides direct help).
- Memory strength per concept (a scalar derived from quiz performance + doubt frequency + time elapsed).
- Behavioral pattern history (does the student disengage after 20 minutes? Do they prefer examples before rules?).

The Learning DNA is embedded and stored in Qdrant's `learning_dna` collection and is retrieved by the Memory Agent as the first step of every interaction.

---

## 13. Adaptive Teaching Framework

Mentra X never gives the same explanation twice to the same student. The Tutor Agent selects one of five escalating teaching levels based on the student's Learning DNA:

| Level | Style | Trigger Condition |
|---|---|---|
| 1 | Simple Direct Explanation | High mastery, brief refresher needed |
| 2 | Worked Step-by-Step Example | Medium mastery, procedural gap |
| 3 | Common Mistake Analysis | Low mastery, historically error-prone |
| 4 | Real-World Visual Analogy | Failed Level 2/3 previously |
| 5 | Alternative Reasoning Paradigm | Chronic confusion, learning style mismatch |

---

## 14. Weak Area Intelligence

The Weakness Intelligence Agent runs asynchronously every 5 sessions as a Mastra chron-workflow. It:

1. Fetches the last 5 session logs from Qdrant's `session_logs` collection.
2. Clusters concepts by failure frequency using semantic similarity.
3. Identifies macro-weakness themes (e.g., "Entropy in Thermodynamics" not just "Physics").
4. Generates a revision curriculum pushed to the Mentra LMS dashboard.
5. Mutates the `weakness_state` field of the Digital Twin in Qdrant.

---

## 15. Success Metrics

| Metric | Target | Measurement |
|---|---|---|
| Doubt Resolution Accuracy | > 97% | Enkrypt confidence scores |
| Comprehension Verification Pass Rate | > 80% | Verification Agent outcomes |
| Weak Area Identification Precision | > 85% | Manual audit + student feedback |
| Student Retention (30-day) | > 70% | Session frequency tracking |
| Learning Velocity Improvement | +40% concept mastery in 30 days | Before/after twin comparison |

---

## 16. Expected Outcomes

**For Students:**
- Faster concept mastery through hyper-personalized explanations.
- Elimination of repeated doubts via persistent memory.
- Verified accuracy eliminating hallucination risk in critical exams.

**For the Platform:**
- Measurable improvement in student outcomes across JEE/NEET/UPSC cohorts.
- A defensible competitive moat built on the depth of individual Learning DNA profiles.

**For the Ecosystem:**
- A proof-of-concept that Mastra + Qdrant + Enkrypt can be composed into a production-grade, domain-specific education AI that surpasses any single-model approach.

---

## 17. Why Mentra X Wins — Competitive Analysis

Mentra X was designed from the ground up to address every failure mode of existing AI education solutions. The following matrix demonstrates why no current platform — AI or traditional — can replicate what we have built.

### Competitor Comparison Matrix

| Capability | ChatGPT | Gemini | Coaching Apps | Doubt Platforms | **Mentra X** |
|---|---|---|---|---|---|
| **Memory Persistence** | ❌ None | ❌ None | ⚠️ Basic history | ⚠️ Thread-level only | ✅ **Lifelong Qdrant Twin** |
| **Student Digital Twin** | ❌ | ❌ | ❌ | ❌ | ✅ **Full 5-state model** |
| **Adaptive Teaching Levels** | ❌ Single response | ⚠️ Prompt-dependent | ⚠️ Fixed video paths | ❌ | ✅ **5-level escalation** |
| **Weakness Detection** | ❌ | ❌ | ⚠️ Basic reports | ❌ | ✅ **Semantic clustering** |
| **Learning DNA** | ❌ | ❌ | ❌ | ❌ | ✅ **Behavioral vector profile** |
| **Stateful Memory RAG** | ❌ | ❌ | ❌ | ❌ | ✅ **Qdrant 5 collections** |
| **Comprehension Verification** | ❌ | ❌ | ⚠️ Quiz at chapter end | ❌ | ✅ **Per-session micro-quiz** |
| **Hallucination Validation** | ❌ | ❌ | ✅ Human-authored | ❌ | ✅ **Enkrypt AI middleware** |
| **Personalized Revision Plan** | ❌ | ❌ | ⚠️ Fixed schedules | ❌ | ✅ **AI-generated from twin** |
| **Long-Term Learning Memory** | ❌ Session only | ❌ Session only | ⚠️ Progress bars | ❌ | ✅ **Infinite Qdrant history** |
| **Concept Decay Modeling** | ❌ | ❌ | ❌ | ❌ | ✅ **Ebbinghaus curve** |
| **Multi-Agent Orchestration** | ❌ | ❌ | ❌ | ❌ | ✅ **6-agent Mastra swarm** |
| **Domain-Specific Safety** | ❌ | ❌ | ✅ Human-curated | ❌ | ✅ **Enkrypt JEE/NEET validator** |

### Why Competitors Cannot Replicate This

**ChatGPT / Gemini:** General-purpose LLMs have no persistent memory architecture, no student modeling, and no domain-specific safety validation. They will give a perfectly confident but potentially wrong answer to a JEE Physics question with no verification mechanism. Every session starts from zero.

**Coaching Apps (BYJU'S, Unacademy, PW):** These platforms provide excellent human-created content but deliver it uniformly. Their "personalization" amounts to progress tracking and basic quiz paths — not adaptive teaching strategy based on individual cognitive profiles.

**Doubt Platforms (Doubtnut, Chegg):** These answer questions in complete isolation. There is no concept of a student's history, no weakness tracking, no comprehension verification, and no guarantee of mathematical accuracy.

**The Moat:** The Student Digital Twin + Learning DNA combination is the architectural moat. Replicating it requires: a vector database infrastructure (Qdrant), a multi-agent orchestration framework (Mastra), an educational safety SDK (Enkrypt), and months of integration engineering. It cannot be replicated with a single API call.


---
Built by Sujith Kumar AI
HiDevs × Mastra Hackathon 2026
---
