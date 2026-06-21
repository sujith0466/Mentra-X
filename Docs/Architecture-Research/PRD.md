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
