# Architecture Diagram Builder Guide — Version 2.0

**Purpose:** Top-30 quality diagram specification for HiDevs × Mastra Hackathon 2026  
**Based on:** Round-1 Judge Review findings  
**Target:** Visually communicate 99/100 written-package depth without supporting documents  
**Upgrade from:** v1.0 (scored 72/100 visually) → v2.0 (target: 92/100)

---

## What Changed From v1.0

| v1.0 Gap | v2.0 Fix |
|---|---|
| No DAG orchestrator node | Added central Mastra DAG Orchestrator hub |
| No execution sequencing | Added ①–⑥ numbered flow labels |
| Single monolithic Qdrant box | Expanded to 5 labeled collection cards |
| No Enkrypt sub-validators | Added 4 validator cards + confidence scorer |
| No regeneration loop | Added red curved arrow: Enkrypt → Tutor Agent |
| No color-coded arrows | Full color system: purple/cyan/green/red |
| No Learning DNA annotation | Added DNA badges on Memory + Tutor Agents |
| No HITL pathway | Added HITL node in Enkrypt warning tier |
| Text truncation throughout | All descriptions full-length |
| No title block | Added Mentra X title with sub-labels |
| Cron not labeled | Weakness Intel Agent marked `[CRON]` |
| No teaching level callout | Added Level 1–5 callout adjacent to Tutor Agent |

---

## 1. Canvas Setup

| Setting | Value |
|---|---|
| Tool | Excalidraw (excalidraw.com) — recommended |
| Canvas dimensions | 2400 × 1600 px |
| Background | `#0A0A0F` (deep near-black) |
| Grid | Off |
| Font | Nunito or Inter |
| Export | SVG → PNG at 2× resolution (min 4800×3200 px for submission) |

---

## 2. Global Color Palette

| Element | Hex | Usage |
|---|---|---|
| Canvas background | `#0A0A0F` | Global |
| Layer band background | `#0F1117` | Band fills |
| Layer band border | `#1E2128` | Band outlines |
| Mastra purple (primary) | `#7C3AED` | Agent fills, orchestrator |
| Mastra purple (light) | `#A78BFA` | Mastra labels, text |
| Qdrant teal (primary) | `#0891B2` | Qdrant container border |
| Qdrant teal (light) | `#22D3EE` | Qdrant labels, text |
| Enkrypt red (primary) | `#DC2626` | Enkrypt container border |
| Enkrypt red (light) | `#FCA5A5` | Enkrypt labels, text |
| MySQL amber | `#D97706` | Foundation layer |
| User layer blue | `#1D4ED8` | User component borders |
| Gateway grey | `#374151` | Flask gateway |
| Success green | `#22C55E` | Twin mutations, pass paths |
| Arrow - Mastra DAG | `#8B5CF6` (purple) | Orchestrator fan-out |
| Arrow - Qdrant memory | `#06B6D4` (cyan) | Vector queries, retrieval |
| Arrow - twin mutation | `#22C55E` (green) | Post-verification updates |
| Arrow - Enkrypt safety | `#EF4444` (red) | Safety intercept, regen loop |
| Arrow - standard flow | `#6B7280` (grey) | HTTP, standard requests |
| Text primary | `#F9FAFB` | Main labels |
| Text secondary | `#9CA3AF` | Descriptions |
| Badge background | `#1F2937` | Tech stack chips |
| Learning DNA gold | `#F59E0B` | DNA badges and annotations |

---

## 3. Overall Layout — 6 Bands + Sidebar

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  TITLE BLOCK (Top-left, floating)                                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│  BAND 1 (h: 140px)    USER LAYER                                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│  BAND 2 (h: 90px)     FLASK API GATEWAY                                         │
├──────────────────────────────────────────────────────────────┬──────────────────┤
│  BAND 3 (h: 520px)    MENTRA COGNITIVE SWARM — Mastra        │  SIDEBAR         │
│                       [Orchestrator hub at top]              │  Teaching Engine  │
│                       [6 agents below]                       │  Levels 1–5      │
│                                                              │                  │
├───────────────────────────────────────┬──────────────────────┴──────────────────┤
│  BAND 4A (h: 320px)                   │  BAND 4B (h: 320px)                     │
│  QDRANT MEMORY ENGINE                 │  ENKRYPT SAFETY LAYER                   │
│  [5 collection cards]                 │  [4 validator cards + regen loop]        │
├───────────────────────────────────────┴─────────────────────────────────────────┤
│  BAND 5 (h: 110px)    MYSQL RELATIONAL FOUNDATION                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│  LEGEND (bottom-right corner, floating)                                         │
└─────────────────────────────────────────────────────────────────────────────────┘
                                                              [Student Output node, right]
```

---

## 4. Title Block (Top-Left Floating)

**Position:** x: 30px, y: 20px  
**No background — floating text block**

```
MENTRA X                                    [font: 32px, bold, #F9FAFB]
AI-Powered Student Digital Twin             [font: 16px, #A78BFA]
─────────────────────────────────────────
Learning DNA  ·  Cognitive Swarm  ·  Stateful Memory RAG
                                            [font: 12px, #9CA3AF, italic]
```

Below the subtitle, add a **Target Users pill row**:

```
[ 🎯 JEE ] [ NEET ] [ UPSC ] [ CAT ] [ Board Exams ]
```
Pill fill: `#1F2937`, border: `#374151`, text: `#F59E0B`, font: 11px

---

## 5. Band 1: User Layer

**Height:** 140px | **Fill:** `#111827` | **Border:** 1px `#1D4ED8` | **Border-radius:** 12px  
**Label:** `👤 USER LAYER` — 14px, `#60A5FA`

**3 component boxes (equal width, ~320px each, 20px gaps):**

Each box: Fill `#1F2937`, border `#374151`, border-radius 8px, height 90px

| Box | Title | Description | Tech Chips |
|---|---|---|---|
| 1 | **Study Dashboard** | Tracks Learning DNA heatmap, mastery scores, XP, streak, weak-area alerts | `React` `Tailwind CSS` |
| 2 | **Cognitive Chat UI** | Main conversational interface for doubt-solving via the Cognitive Swarm | `React` `WebSockets` |
| 3 | **LMS Video Player** | Context-aware video player with lesson progress tracking | `React` `Video.js` |

**Tech chips:** Fill `#111827`, border `#374151`, font 10px, color `#9CA3AF`

**Arrow out (center-bottom):** Label `HTTPS REST / WebSocket` → Band 2  
Color: `#6B7280`, style: solid, 2px

---

## 6. Band 2: Flask API Gateway

**Height:** 90px | **Fill:** `#1F2937` | **Border:** 1px `#374151`  
**Label:** `🔐 FLASK API GATEWAY (Band 2)` — 12px, `#9CA3AF`

**4 chip shapes inline (horizontally centered):**

`[ JWT Auth ]` `[ Rate Limiter ]` `[ Session Manager ]` `[ Route Guard ]`

Chip height: 36px | Fill: `#111827` | Border: `#374151` | Text: 12px `#9CA3AF`  
Tech chip on each: `Flask` `Python` `PyJWT`

**Arrow in (top):** from Band 1  
**Arrow out (bottom):** `Validated Request` → Band 3 Orchestrator  
Color: `#6B7280`

---

## 7. Band 3: Mentra Cognitive Swarm (Mastra) — MAIN BAND

**Height:** 520px | **Fill:** `#1E1347` | **Border:** 2px dashed `#7C3AED` | **Border-radius:** 16px  
**Label (top-left):** `🧠 MENTRA COGNITIVE SWARM` — 20px bold, `#A78BFA`  
**Sub-label (top-right):** `Powered by Mastra AI` — 12px `#7C3AED`

### 7.1 Mastra DAG Orchestrator Node (NEW — Center Top of Band 3)

**Position:** Horizontally centered in Band 3, 40px from top edge  
**Shape:** Diamond or wide rounded rectangle, distinctive  
**Dimensions:** 280px wide × 60px tall  
**Fill:** `#4C1D95` | **Border:** 3px solid `#7C3AED` | **Border-radius:** 12px  
**Label:** `Mastra DAG Orchestrator` — 14px bold, `#E9D5FF`  
**Sub-label:** `Graph-based Multi-Agent Coordinator` — 10px, `#A78BFA`  
**Badge:** `Mastra.AI` chip on right side

**Arrow in (top):** from Flask Gateway — color `#6B7280`, label `Structured Request`  
**Fan-out arrows (bottom):** 6 purple arrows (`#8B5CF6`) fanning out to each agent below

---

### 7.2 Execution Sequence Labels

Place numbered circle badges on arrows in the primary execution flow:

| Badge | Position | Label |
|---|---|---|
| `①` | Orchestrator → Assessment Agent | `Onboarding` |
| `②` | Orchestrator → Memory Agent | `Context Retrieval` |
| `③` | Memory Agent → Tutor Agent | `Hydrated Twin Context` |
| `④` | Tutor Agent → Enkrypt | `Validate Output` |
| `⑤` | Enkrypt → Verification Agent | `Validated Response` |
| `⑥` | Verification Agent → Student | `Final Response + Quiz` |

Badge style: Circle 24px diameter, fill `#7C3AED`, text `#FFFFFF`, font 12px bold

---

### 7.3 Agent Nodes (6 agents in 2 rows)

**Shape:** Rounded rectangle, 280px × 140px  
**Fill:** `#2D1B69` | **Border:** 1px `#4C1D95` | **Border-radius:** 10px  
**Badge on each:** `Mastra.AI` + `Python` chips at bottom

**Row 1 (left to right):**

| Agent | Special Markup | Description |
|---|---|---|
| `Assessment Agent` | Badge: `DIAGNOSTIC` | Adaptive branching diagnostic calibrated to JEE/NEET/UPSC difficulty thresholds |
| `Memory Agent` | Badge: `🧬 Learning DNA` (gold) | Parallel Qdrant fetch: learning_dna + past_doubts + explanation_history + MySQL |
| `Tutor Agent` | Badge: `🧬 Learning DNA` (gold) | Core adaptive tutor. Selects Level 1–5 teaching based on Digital Twin state |

**Row 2 (left to right):**

| Agent | Special Markup | Description |
|---|---|---|
| `Verification Agent` | Badge: `COMPREHENSION` | Generates micro-quiz post-explanation. Mutates twin on student response |
| `Weakness Intel Agent` | Badge: `[CRON] ⏰` (amber) | Fires every 5 sessions. Semantic clustering of failure patterns |
| `Insight Agent` | Badge: `WEEKLY REPORT` | Synthesizes progress reports and revision curriculum from twin state |

**Learning DNA badge styling:**  
Fill: `#78350F`, border: `#F59E0B`, text: `#FCD34D`, font: 10px bold  
Apply to: Memory Agent, Tutor Agent

**CRON badge styling:**  
Fill: `#78350F`, border: `#D97706`, text: `#FCD34D`, dashed border, font: 10px bold

---

### 7.4 Human-in-the-Loop (HITL) Node (NEW)

**Position:** To the right of the Enkrypt band, floating  
**Shape:** Rounded rectangle, 180px × 80px  
**Fill:** `#1A3A1A` | **Border:** 1.5px dashed `#22C55E`  
**Label:** `👨‍🏫 HITL Expert Review` — 12px, `#86EFAC`  
**Description:** `Triggered when Enkrypt\nscore = 0.75–0.89 (warning)` — 10px, `#9CA3AF`

**Arrow in:** from Enkrypt Safety Layer (dashed green arrow, label `Warning Tier`)  
**Arrow out:** to Qdrant `reference_corpus` (dashed green arrow, label `Expert-Verified Content`)

---

## 8. Band 4A: Qdrant Memory Engine (Left Half)

**Width:** 48% of canvas | **Height:** 320px  
**Fill:** `#062030` | **Border:** 2px solid `#0891B2` | **Border-radius:** 12px  
**Label:** `🔵 QDRANT LEARNING DNA MEMORY ENGINE` — 16px bold, `#22D3EE`  
**Sub-label:** `Stateful Memory RAG · 1536-dim Cosine · HNSW Index` — 10px, `#0891B2`  
**Badge (top-right):** `Qdrant` chip

### 5 Collection Cards (stacked vertically, full width)

Each card: Height 42px | Fill: `#0C3547` | Border: 1px `#164E63` | Border-radius 6px

| Card | Label | Annotation |
|---|---|---|
| 1 | `📊 learning_dna` | `Primary Digital Twin Store — mastery, behavior, DNA` |
| 2 | `🔍 past_doubts` | `Semantic doubt history — cosine similarity retrieval` |
| 3 | `📝 explanation_history` | `Teaching level outcomes — what worked, what failed` |
| 4 | `📋 session_logs` | `Raw session transcripts — used by Weakness Agent` |
| 5 | `⚠️ weak_concepts` | `Clustered failure patterns — severity scored` |

Card text: 11px bold `#67E8F9` for label, 9px `#9CA3AF` for annotation

### Qdrant Annotations (floating callout boxes)

**Callout 1** (right side of Qdrant band):
```
🧬 Learning DNA
Behavioral vector encoding:
• Mastery score per concept
• Preferred teaching level
• Frustration index
• Analogy effectiveness
• Memory retention curve
```
Fill: `#0C2A40`, border: `#F59E0B` (gold), text: `#FCD34D`, font 10px

**Callout 2** (bottom of Qdrant band):
```
📉 Ebbinghaus Concept Decay
Nightly cron: mastery × 0.85
per unreviewed concept
```
Fill: `#0C2A40`, border: `#6366F1`, text: `#A5B4FC`, font 10px

### Arrows for Qdrant

**Parallel retrieval arrows (cyan `#06B6D4`, from top):**
- Memory Agent → `learning_dna` (label: `fetch_digital_twin`)
- Memory Agent → `past_doubts` (label: `semantic search top-K=3`)
- Memory Agent → `explanation_history` (label: `retrieve failures`)
- Assessment Agent → `learning_dna` (label: `initialize_twin`)

**Twin mutation arrows (green `#22C55E`, going INTO Qdrant):**
- Verification Agent → `learning_dna` (label: `mutate mastery ±0.05`)
- Verification Agent → `explanation_history` (label: `upsert success_flag`)
- Weakness Intel Agent → `weak_concepts` (label: `upsert clusters`)
- Weakness Intel Agent → `learning_dna` (label: `update weakness_state`)

---

## 9. Band 4B: Enkrypt Safety Layer (Right Half)

**Width:** 48% of canvas (with 4% gap between 4A and 4B)  
**Height:** 320px  
**Fill:** `#200808` | **Border:** 2px solid `#DC2626` | **Border-radius:** 12px  
**Label:** `🛡️ ENKRYPT AI SAFETY LAYER` — 16px bold, `#FCA5A5`  
**Sub-label:** `Mandatory Educational Safety Middleware` — 10px, `#DC2626`  
**Badge (top-right):** `Enkrypt AI` chip

### 4 Validator Cards (stacked vertically)

Each card: Height 42px | Fill: `#350808` | Border: 1px `#7F1D1D` | Border-radius 6px

| Card | Label | Annotation |
|---|---|---|
| 1 | `∑ Math Accuracy Validator` | `Verifies JEE calculus, step-by-step logic` |
| 2 | `🔬 Science Fact Validator` | `Cross-references NEET/Physics/Chemistry claims` |
| 3 | `🚫 Hallucination Detector` | `Semantic match vs NCERT reference corpus` |
| 4 | `📚 Pedagogy Evaluator` | `Ensures tutor mode, not answer-key mode` |

### Confidence Scorer Node

**Below the 4 validator cards:**  
Shape: Wide card, height 50px | Fill `#4A0808` | Border: 2px `#DC2626`

```
📊 Confidence Scorer
conf = 0.35×math + 0.30×science + 0.20×(1−hallucination) + 0.15×pedagogy
```
Font: 11px `#FCA5A5`

### Safety Decision Branches

Below the Confidence Scorer, show 3 decision paths:

**Path 1 (Green arrow, right):** `Score ≥ 0.90 → PASS`  
→ Arrow to Verification Agent, color `#22C55E`, label `Validated ✓`

**Path 2 (Amber arrow, right):** `Score 0.75–0.89 → WARN`  
→ Arrow to HITL node, color `#D97706`, label `Expert Review 🟡`

**Path 3 (Red curved arrow, LEFT back to Tutor Agent):** `Score < 0.75 → REGENERATE` ← **CRITICAL ADDITION**  
Arrow style: Curved, thick 3px, color `#EF4444`, dashed  
Label: `⚠️ Regenerate Response` on the curved arc  
Max attempts annotation: `Max 2 attempts`

### Hard Fallback Node

**Below Band 4B, outside main band:**  
Shape: Rounded rectangle 200px × 50px  
Fill: `#1A0000`, border: `1px dashed #DC2626`  
Label: `📖 Verified Textbook Fallback` — 11px, `#FCA5A5`  
Arrow in: from Confidence Scorer, label `Double Failure`, color `#EF4444`

---

## 10. Teaching Engine Sidebar (Right of Band 3)

**Position:** Floating sidebar to the right of Band 3  
**Width:** 200px | **Height:** 300px  
**Fill:** `#1A0F3A` | **Border:** 1.5px dashed `#7C3AED` | **Border-radius:** 12px  
**Label:** `🎓 Adaptive Teaching Engine` — 13px bold, `#A78BFA`  
**Arrow from:** Tutor Agent → Sidebar (dashed purple)

**5 level cards (stacked):**

| Card | Level | Label | Color |
|---|---|---|---|
| 1 | Level 1 | Simple Explanation | `#22C55E` |
| 2 | Level 2 | Example-Based Teaching | `#84CC16` |
| 3 | Level 3 | Common Mistakes Analysis | `#EAB308` |
| 4 | Level 4 | Visual Analogy | `#F97316` |
| 5 | Level 5 | Exam Coaching Mode | `#EF4444` |

Each card: height 40px, fill `#0F0A2A`, font 10px, left border 3px in the color above

**Callout below cards:**
```
Escalation triggered by:
• Frustration index > 0.7
• mastery_score < 0.3
• Repeated verification fail
```
Font: 9px, `#9CA3AF`

---

## 11. Band 5: MySQL Foundation

**Height:** 110px | **Fill:** `#111827` | **Border:** 1px `#374151`  
**Label:** `🗄️ MENTRA RELATIONAL FOUNDATION (MySQL)` — 14px, `#FCD34D`

**6 pill chips inline:**

`[ Users ]` `[ Courses ]` `[ Quiz Scores ]` `[ XP Ledger ]` `[ Portfolios ]` `[ Skill Graph ]`

Chip: Fill `#1F2937`, border `#374151`, text `#FCD34D`, font 11px

**Arrow up:** `Deterministic Ground Truth` → Mastra Orchestrator, color `#D97706`  
**Arrow in:** from Insight Agent → MySQL, label `Push Revision Plan`, color `#22C55E`

---

## 12. Student Output Node

**Position:** Far right of canvas, vertically centered between Bands 4 and 5  
**Shape:** Circle, 100px diameter  
**Fill:** `#1A2A1A` | **Border:** 2px solid `#22C55E`  
**Label:** `👤 Student` — 14px, `#F9FAFB`  
**Sub-label:** `Personalized\nLearning Response` — 9px, `#9CA3AF`

**Arrow in (left):** from Verification Agent, label `⑥ Final Response + Quiz`, color `#22C55E`, 2px  
**Arrow in (bottom-left):** from Enkrypt (warn path), label `🟡 With Warning Badge`, color `#D97706`, dashed

---

## 13. Legend Box (Bottom-Right, Floating)

**Size:** 220px × 200px | **Fill:** `#0F1117` | **Border:** 1px `#374151` | **Border-radius:** 8px  
**Label:** `Legend` — 12px bold `#9CA3AF`

```
──── Mastra Orchestration Flow   (purple)
──── Qdrant Memory / RAG         (cyan)
──── Twin Mutation               (green)
──── Enkrypt Safety              (red)
- - - Async / CRON / HITL        (dashed)
──── Standard HTTP Flow          (grey)

🧬  Learning DNA Component
[CRON]  Background Cron Workflow
①–⑥  Execution Sequence
```

Font: 10px, colors matching arrow types, left border strips in respective colors

---

## 14. Complete Arrow Inventory

| From | To | Color | Label | Style |
|---|---|---|---|---|
| Band 1 | Flask Gateway | `#6B7280` | HTTPS / WebSocket | Solid |
| Flask Gateway | DAG Orchestrator | `#6B7280` | Structured Request | Solid |
| DAG Orchestrator | Assessment Agent | `#8B5CF6` | ① Onboarding | Purple solid |
| DAG Orchestrator | Memory Agent | `#8B5CF6` | ② Context Retrieval | Purple solid |
| DAG Orchestrator | Tutor Agent | `#8B5CF6` | ③ Tutor Reasoning | Purple solid |
| DAG Orchestrator | Verification Agent | `#8B5CF6` | ⑤ Verify | Purple solid |
| DAG Orchestrator | Weakness Intel Agent | `#8B5CF6` | CRON trigger | Purple dashed |
| DAG Orchestrator | Insight Agent | `#8B5CF6` | Report | Purple solid |
| Memory Agent | learning_dna | `#06B6D4` | fetch_digital_twin | Cyan solid |
| Memory Agent | past_doubts | `#06B6D4` | semantic search | Cyan solid |
| Memory Agent | explanation_history | `#06B6D4` | retrieve failures | Cyan solid |
| Memory Agent | Tutor Agent | `#06B6D4` | Hydrated Twin Context | Cyan solid |
| Assessment Agent | learning_dna | `#06B6D4` | initialize_twin | Cyan solid |
| Tutor Agent | Enkrypt | `#EF4444` | ④ Validate Output | Red solid |
| Enkrypt | Verification Agent | `#22C55E` | Score ≥ 0.90 ✓ | Green solid |
| Enkrypt | Tutor Agent | `#EF4444` | ⚠️ Regenerate | Red dashed curved |
| Enkrypt | HITL Node | `#D97706` | Warning 0.75–0.89 | Amber dashed |
| Enkrypt | Textbook Fallback | `#EF4444` | Double Failure | Red solid |
| Verification Agent | Student | `#22C55E` | ⑥ Final Response + Quiz | Green solid |
| Verification Agent | learning_dna | `#22C55E` | mutate mastery | Green solid |
| Verification Agent | explanation_history | `#22C55E` | upsert success_flag | Green solid |
| Weakness Intel Agent | session_logs | `#06B6D4` | fetch last 5 sessions | Cyan solid |
| Weakness Intel Agent | weak_concepts | `#22C55E` | upsert clusters | Green solid |
| Weakness Intel Agent | learning_dna | `#22C55E` | update weakness_state | Green solid |
| Weakness Intel Agent | Insight Agent | `#8B5CF6` | Weakness Clusters | Purple solid |
| Insight Agent | MySQL | `#22C55E` | Push Revision Plan | Green solid |
| MySQL | DAG Orchestrator | `#D97706` | Deterministic Ground Truth | Amber solid |
| HITL Node | reference_corpus | `#22C55E` | Expert-Verified Content | Green dashed |

---

## 15. Time Estimate By Tool

| Tool | Estimated Time |
|---|---|
| **Excalidraw** | 45–60 minutes |
| **draw.io** | 60–75 minutes |
| **Figma** | 75–90 minutes |
| **Canva** | 90–120 minutes (limited for complex diagrams) |

**Recommended: Excalidraw** — fastest, supports exact hex colors, free export to SVG/PNG.
