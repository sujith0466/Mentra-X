# Mentra X — Enkrypt AI Safety Architecture

**Purpose:** Maximize Enkrypt AI Coverage scoring (20%)  
**SDK:** Enkrypt AI Evaluation & Safety Framework

---

## 1. Why Enkrypt AI is Non-Negotiable

In competitive exam preparation, a single hallucinated formula can destroy a student's JEE rank. A fabricated historical date can cost them the UPSC Mains. A wrong chemical equation can eliminate their NEET score.

General LLMs hallucinate at rates of 3–15% depending on domain specificity. In a high-stakes educational context, even a 1% hallucination rate across 10 million queries produces 100,000 harmful responses.

Mentra X addresses this with **mandatory Enkrypt AI middleware** — positioned not as an optional quality layer, but as a hard blocker between the Mastra Tutor Agent and the student interface.

**Enkrypt is not optional. It is the safety contract.**

---

## 2. Architectural Position

```
Mastra Tutor Agent
       │
       ▼
┌──────────────────────────────────────┐
│     ENKRYPT AI SAFETY MIDDLEWARE     │
│                                      │
│  [Math Validator]                    │
│  [Science Fact Validator]            │
│  [Hallucination Detector]            │
│  [Pedagogical Evaluator]             │
│  [Risk Classifier]                   │
│  [Confidence Scorer]                 │
│                                      │
│  Decision: PASS | WARN | BLOCK       │
└──────────────────────────────────────┘
       │
       ▼ (Pass)          ▼ (Block)
Verification Agent    Mastra Regeneration Loop
```

---

## 3. Validation Pipelines

### 3.1 Mathematical Accuracy Validator

**Trigger Condition:** Response contains LaTeX, `$$`, `=`, integral signs, or numeric equations.

**Process:**
1. Extract all mathematical expressions from Tutor Agent output.
2. Parse into symbolic expression tree.
3. Verify: does step N logically follow from step N-1?
4. Spot-check final answer against known solution patterns.
5. Score: `math_accuracy (0.0–1.0)`.

**Critical Exam Domains:**
- JEE: Calculus, Coordinate Geometry, Differential Equations, Complex Numbers.
- CAT: Quantitative Aptitude, Data Interpretation.

**Failure Action:** Block output. Inject into Mastra context: `"Your previous derivation contained a logical error in Step 3. Regenerate with a corrected intermediate step."`

---

### 3.2 Science Fact Validator

**Trigger Condition:** Response tagged with `subject: Physics | Chemistry | Biology`.

**Process:**
1. Extract all factual claims (laws, constants, biological processes).
2. Cross-reference against embedded NCERT/standard textbook corpus in Qdrant (`reference_corpus` collection).
3. Score factual alignment: `science_accuracy (0.0–1.0)`.

**Critical Exam Domains:**
- NEET: Organic Chemistry, Human Physiology, Genetics.
- JEE: Thermodynamics, Electrostatics, Optics.

**Failure Action:**
- If fabricated constant detected (e.g., wrong value of Avogadro's number): **Hard block + fallback to safe textbook definition.**
- If minor inaccuracy: **Warn with orange UI badge.**

---

### 3.3 Hallucination Detector

**Trigger Condition:** Response tagged with `subject: History | Polity | Economy | Geography` (UPSC/CAT).

**Process:**
1. Extract entity claims (names, dates, events, policy titles).
2. Embed claims.
3. Compare against known-good fact corpus via Qdrant semantic search.
4. Threshold: if no high-confidence match found for a claim, flag as potential hallucination.
5. Score: `hallucination_risk (0.0–1.0)`.

**Failure Action:**
- `hallucination_risk > 0.5`: Block + Regenerate.
- `hallucination_risk 0.25–0.5`: Deliver with red caution badge: `"This claim could not be verified. Cross-check with official sources."`

---

### 3.4 Pedagogical Evaluator

**Trigger Condition:** Every single response (no exception).

**Process:**
1. Check: does the response explain the *why*, not just the *what*?
2. Check: does the response conclude with a guiding question or next step?
3. Check: is the explanation calibrated to the student's detected teaching level?
4. Score: `pedagogy_quality (0.0–1.0)`.

**This evaluator does NOT block.** It contributes to the overall confidence score and flags low-pedagogy responses for the Insight Agent to use in report generation.

---

### 3.5 Risk Classifier

**Trigger Condition:** All responses.

**Process:**
1. Scan for: harmful content, off-topic material, exam-rule violations (e.g., giving full exam answers).
2. Classify risk: `LOW | MEDIUM | HIGH`.

**Failure Action:**
- `HIGH` risk: Block entirely, log incident, trigger admin notification.
- `MEDIUM`: Soft redirection ("That question falls outside the scope of this tutor").

---

### 3.6 Confidence Scorer (Aggregator)

Aggregates all evaluator scores into a single `confidence_score (0.0–1.0)`:

```
confidence_score = (
  0.35 × math_accuracy +
  0.30 × science_accuracy +
  0.20 × (1.0 - hallucination_risk) +
  0.15 × pedagogy_quality
)
```

**Decision Matrix:**

| Confidence Score | Action | UI Indicator |
|---|---|---|
| ≥ 0.90 | Pass → Verification Agent | ✅ No badge |
| 0.75 – 0.89 | Pass with warning | 🟡 "AI generated — verify with textbook" |
| 0.50 – 0.74 | Block → Mastra regeneration (attempt 2) | ⚠️ Regenerating... |
| < 0.50 | Hard block → Safe textbook fallback | 🔴 "This concept exceeds AI confidence. Refer to Chapter X." |

---

## 4. Regeneration Loop

```
First attempt: Tutor Agent generates response
Enkrypt scores: 0.72 (below threshold)
       │
       ▼
Inject into Mastra context:
"Your previous answer scored 0.72 on accuracy.
Identified issue: [math_step_3_invalid].
Regenerate with corrected derivation and verified constants."
       │
       ▼
Tutor Agent regenerates
Enkrypt scores second attempt: 0.94
       │
       ▼
PASS → Verification Agent
```

**Maximum regeneration attempts:** 2.  
**If 2 failures:** Hard fallback to safe pre-verified textbook excerpt.

---

## 5. Enkrypt Integration — Exact Code Hooks

```python
from enkrypt_sdk import SafetyEvaluator

evaluator = SafetyEvaluator(domain="education", exam_type="JEE")

result = evaluator.evaluate(
    content=tutor_agent_output,
    subject_tag=request.subject,
    student_level=twin.behavior_state.preferred_level
)

if result.confidence_score >= 0.90:
    pass_to_verification_agent(result.content)
elif result.confidence_score >= 0.75:
    deliver_with_warning(result.content, badge="yellow")
else:
    trigger_mastra_regeneration(
        agent="tutor_agent",
        error_context=result.failure_reason
    )
```
