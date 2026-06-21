# Mentra X — Student Digital Twin Design

**Purpose:** Primary Innovation Document  
**Status:** The core differentiator of the Mentra X platform.

---

## 1. What is the Student Digital Twin?

The **Student Digital Twin** is a persistent, living computational model of a student's academic mind. Unlike a user profile (which stores what a student did), the Digital Twin models *how* they think, *why* they fail, and *what* they need next.

It is the first application of Digital Twin theory — pioneered in manufacturing by Siemens and NASA to model physical assets — to human cognitive science and personalized education.

Every student in Mentra X has exactly one Digital Twin. It is:
- **Initialized** on onboarding via the Assessment Agent.
- **Mutated** after every interaction via the Verification Agent.
- **Analyzed** every 5 sessions by the Weakness Intelligence Agent.
- **Decayed** nightly to model natural forgetting.
- **Retrieved** before every teaching session by the Memory Agent.

---

## 2. Twin Architecture: The Five States

### State 1: Academic State

Tracks the student's formal position within structured curricula.

```json
"academic_state": {
  "exam_target": "JEE Advanced",
  "enrolled_subjects": ["Physics", "Chemistry", "Mathematics"],
  "current_chapters": {
    "Physics": "Thermodynamics",
    "Chemistry": "Organic Reactions",
    "Mathematics": "Differential Equations"
  },
  "xp_total": 3450,
  "streak_days": 21,
  "completion_percentage": {
    "Physics": 0.62,
    "Chemistry": 0.45,
    "Mathematics": 0.78
  }
}
```

**Data Source:** Mentra MySQL (Enrollments, XP, Course Progress)  
**Update Trigger:** Course completion events, XP awards.

---

### State 2: Knowledge State

The granular, concept-level mastery model. This is where individual academic intelligence lives.

```json
"knowledge_state": {
  "Physics > Thermodynamics > Entropy": {
    "mastery_score": 0.38,
    "confidence_level": "low",
    "mistake_count": 14,
    "last_successful_recall": "2026-06-15T09:00:00Z",
    "total_doubt_sessions": 6,
    "explanation_levels_tried": [2, 3, 4],
    "resolved": false
  },
  "Mathematics > Differential Equations > Homogeneous": {
    "mastery_score": 0.89,
    "confidence_level": "high",
    "mistake_count": 1,
    "last_successful_recall": "2026-06-20T14:00:00Z",
    "resolved": true
  }
}
```

**Data Source:** Mastra Verification Agent (post-comprehension check), Quiz scores from MySQL.  
**Update Trigger:** Every doubt session and micro-quiz result.

**Mastery Score Range:** 0.0 (no understanding) → 1.0 (expert).  
**Confidence Levels:** `critical` < 0.30 | `low` 0.30–0.55 | `developing` 0.55–0.75 | `high` > 0.75

---

### State 3: Skill State

Cross-cutting technical and cognitive skills beyond subject knowledge.

```json
"skill_state": {
  "problem_solving": 0.71,
  "formula_recall": 0.44,
  "conceptual_understanding": 0.68,
  "exam_time_management": 0.52,
  "diagram_interpretation": 0.80
}
```

**Data Source:** Derived from Coding Platform scores, Quiz performance patterns, Interview results.  
**Update Trigger:** Weekly aggregation from Mentra LMS analytics.

---

### State 4: Learning DNA

The behavioral and cognitive fingerprint of the student. This is the highest-value state for teaching personalization.

```json
"learning_dna": {
  "primary_learning_style": "Visual",
  "secondary_learning_style": "Narrative",
  "frustration_index": 0.61,
  "avg_session_duration_minutes": 28,
  "engagement_drop_minute": 25,
  "preferred_teaching_level": 3,
  "analogy_effectiveness": {
    "mechanical_analogies": 0.9,
    "mathematical_proofs": 0.3,
    "real_world_scenarios": 0.85
  },
  "response_to_correction": "receptive",
  "prefers_examples_before_rules": true,
  "works_well_under_time_pressure": false
}
```

**Data Source:** Mastra agent behavioral signals (how quickly does the student ask for simplification? How many times do they rephrase their doubt?).  
**Update Trigger:** Every session. Exponential moving average smooths updates to prevent noise from single data points.

---

### State 5: Weakness State

Synthesized by the Weakness Intelligence Agent from session logs.

```json
"weakness_state": {
  "recurring_traps": [
    "Forgets negative sign when integrating sin(x)",
    "Confuses entropy with enthalpy"
  ],
  "low_mastery_concepts": [
    "Entropy",
    "Clausius Inequality",
    "Wave Optics Diffraction"
  ],
  "failure_patterns": [
    "Performs well on formula substitution, fails on conceptual derivation",
    "Answers correctly in isolation, fails under multi-step problems"
  ],
  "decayed_concepts": [
    "Wave Optics (last review: 14 days ago)",
    "Electrostatics Gauss Law (last review: 21 days ago)"
  ],
  "revision_urgency": {
    "Entropy": "CRITICAL",
    "Wave Optics": "HIGH",
    "Gauss Law": "MEDIUM"
  }
}
```

**Data Source:** Weakness Intelligence Agent (Mastra cron), Qdrant semantic clustering.  
**Update Trigger:** Every 5 sessions.

---

## 3. Twin Initialization Flow

```
Student joins Mentra X
       │
       ▼
Assessment Agent runs adaptive diagnostic
       │
       ▼
MySQL seed: quiz scores, enrollment history, XP
       │
       ▼
Generate initial_knowledge_state (topic mastery estimates)
Detect initial learning_dna signals (timing, rephrasing behavior)
       │
       ▼
Embed: summary text of all states
Upsert to Qdrant: learning_dna collection
       │
       ▼
Digital Twin ACTIVE — version 1
```

---

## 4. Twin Mutation Protocol

Every mutation is versioned. Previous states are archived for trend analysis.

| Event | Mutation |
|---|---|
| Student passes micro-quiz | `mastery_score[topic] += 0.05`, `version++` |
| Student fails micro-quiz | `mastery_score[topic] -= 0.05`, `mistake_count++`, `version++` |
| Student asks same question again | `frustration_index += 0.03`, `version++` |
| Session ends (5th session) | Full Weakness State rebuild, `version++` |
| 7 days since last concept review | `mastery_score[topic] *= 0.85` (decay), `version++` |
| Student explicitly says "I understood" | `confidence_level` upgraded one tier |

---

## 5. Personalization Logic

The Digital Twin directly controls the Tutor Agent's behavior through the following mappings:

| Twin Signal | Agent Response |
|---|---|
| `frustration_index > 0.7` | Jump to Level 4 or 5 explanation immediately |
| `preferred_level = 3` | Always start at Level 3 for new concepts |
| `primary_style = Visual` | Prefer visual analogies, avoid formula-heavy proofs |
| `mastery_score < 0.3` (critical) | Trigger Weakness Agent early (3 sessions instead of 5) |
| `engagement_drop_minute = 25` | Insert a comprehension break at minute 22 |
| `weakness_state.revision_urgency = CRITICAL` | Open session with "Before your doubt, let's briefly revise X" |
