# Mentra X — Architecture Diagram v2 (Excalidraw Specification)

**Purpose:** Step-by-step guide to build the v2 architecture diagram in Excalidraw.  
**Tool:** [excalidraw.com](https://excalidraw.com) — free, browser-based, recommended.  
**Estimated time:** 45–60 minutes following this guide exactly.

---

## Quick Start Checklist

```
[ ] Open excalidraw.com
[ ] Set canvas background: #0A0A0F
[ ] Create title block first (north star for proportions)
[ ] Draw band backgrounds (bottom-up: MySQL → Qdrant/Enkrypt → Swarm → Gateway → Users)
[ ] Place agents and components on top of bands
[ ] Connect with arrows (color coded)
[ ] Add callouts, badges, legend last
[ ] Export: SVG → PNG at 2×
```

---

## 1. Global Settings

| Setting | Action |
|---|---|
| Background | Press `K` or click canvas → Background Color → `#0A0A0F` |
| Font | Nunito (Excalidraw default is fine; change if desired) |
| Stroke width | Set globally to 2 (top toolbar) |
| Rounded corners | ON for all rectangles |
| Grid | OFF |

---

## 2. Title Block (Top-Left)

Draw 3 text elements using the `T` (text) tool:

**Text 1:**
```
MENTRA X
```
Font size: 36 | Bold | Color: `#F9FAFB` | Position: x=40, y=24

**Text 2:**
```
AI-Powered Student Digital Twin
```
Font size: 18 | Color: `#A78BFA` | Position: x=40, y=72

**Text 3:**
```
Learning DNA  ·  Cognitive Swarm  ·  Stateful Memory RAG
```
Font size: 12 | Italic | Color: `#9CA3AF` | Position: x=40, y=100

**Target users row (5 pills):**
Draw 5 rectangles (rounded), width≈80px, height=26px, y=128:
- Fill: `#1F2937` | Border: `#374151` | Text color: `#F59E0B` | Size: 11px
- Labels: `🎯 JEE` `NEET` `UPSC` `CAT` `Board Exams`
- x positions: 40, 132, 224, 316, 408

---

## 3. Band Backgrounds (Draw these FIRST — they sit behind everything)

Use `R` (rectangle tool) for each band. These are the large colored zones.

### Band 1: User Layer
- x=30, y=170 | Width=1340, Height=150
- Fill: `#111827` | Stroke: `#1D4ED8` | Stroke width: 1 | Rounded: ON
- Label: `👤 USER LAYER` | Font: 13px | Color: `#60A5FA` | Position: top-left inside

### Band 2: Flask API Gateway
- x=30, y=340 | Width=1340, Height=95
- Fill: `#1F2937` | Stroke: `#374151` | Stroke: 1

### Band 3: Mastra Cognitive Swarm (largest band)
- x=30, y=455 | Width=1340, Height=530
- Fill: `#1E1347` | Stroke: `#7C3AED` | Stroke: 2 | Dashed: YES (toggle `Alt+D`)
- Label: `🧠 MENTRA COGNITIVE SWARM` | Font: 18px bold | Color: `#A78BFA`
- Sub-label (top-right): `Powered by Mastra AI` | Font: 11px | Color: `#7C3AED`

### Band 4A: Qdrant (left side)
- x=30, y=1005 | Width=660, Height=330
- Fill: `#062030` | Stroke: `#0891B2` | Stroke: 2

### Band 4B: Enkrypt (right side, with gap)
- x=710, y=1005 | Width=660, Height=330
- Fill: `#200808` | Stroke: `#DC2626` | Stroke: 2

### Band 5: MySQL Foundation
- x=30, y=1355 | Width=1340, Height=115
- Fill: `#111827` | Stroke: `#374151` | Stroke: 1

---

## 4. Band Labels

For each band, add a text element inside the band (top-left corner):

| Band | Text | Font | Color |
|---|---|---|---|
| 1 | `👤 USER LAYER` | 13px | `#60A5FA` |
| 2 | `🔐 FLASK API GATEWAY (Band 2)` | 12px | `#9CA3AF` |
| 3 | `🧠 MENTRA COGNITIVE SWARM` | 20px bold | `#A78BFA` |
| 4A | `🔵 QDRANT LEARNING DNA MEMORY ENGINE` | 14px bold | `#22D3EE` |
| 4A (sub) | `Stateful Memory RAG · 1536-dim Cosine · HNSW Index` | 10px italic | `#0891B2` |
| 4B | `🛡️ ENKRYPT AI SAFETY LAYER` | 14px bold | `#FCA5A5` |
| 4B (sub) | `Mandatory Educational Safety Middleware` | 10px | `#DC2626` |
| 5 | `🗄️ MENTRA RELATIONAL FOUNDATION (MySQL)` | 14px | `#FCD34D` |

---

## 5. User Layer Components (Band 1)

Draw 3 rectangles inside Band 1. Each: Width=400px, Height=105px, y=185.

**Common style:**
Fill: `#1F2937` | Stroke: `#374151` | Rounded: ON | Stroke width: 1

| Component | x | Title | Description |
|---|---|---|---|
| Study Dashboard | 50 | `📊 Study Dashboard` | Learning DNA Heatmap · XP · Streak · Weak-Area Alerts |
| Cognitive Chat UI | 470 | `💬 Cognitive Chat UI` | Main conversational interface for doubt-solving |
| LMS Video Player | 890 | `🎬 LMS Video Player` | Context-aware · Progress tracked |

Title font: 13px bold, `#F9FAFB`  
Description font: 10px, `#9CA3AF`

**Tech chips** (small rectangles inside each component, bottom area):
Size: 60px × 18px | Fill: `#111827` | Stroke: `#374151` | Text: `#9CA3AF`, 9px  
Labels: `React` `WebSockets` `Tailwind` (as applicable)

---

## 6. Flask API Gateway (Band 2)

4 chip shapes inside Band 2 (y=365):
Width: 200px | Height: 42px | Fill: `#111827` | Stroke: `#374151` | Rounded ON  
x positions (equally spaced): 80, 300, 520, 740  
Labels: `JWT Auth`, `Rate Limiter`, `Session Manager`, `Route Guard`  
Font: 12px | Color: `#9CA3AF`

---

## 7. Mastra DAG Orchestrator Node (NEW — Top of Band 3)

**Draw a distinctive rectangle (slightly different style):**

Position: x=500, y=475 | Width=340px, Height=70px  
Fill: `#4C1D95` | Stroke: `#7C3AED` | Stroke width: 3 | Rounded: ON

**Label (centered):**
`◆ Mastra DAG Orchestrator` | Font: 14px bold | Color: `#E9D5FF`

**Sub-label below:**
`Graph-based Multi-Agent Coordinator` | Font: 10px | Color: `#A78BFA`

**Mastra badge (top-right inside):**
Small rectangle 80px × 20px | Fill: `#7C3AED` | Text: `Mastra.AI` | 9px white

---

## 8. Execution Number Badges

Draw 6 small circles (24px diameter) along the primary flow path:

| Badge | x | y | Label |
|---|---|---|---|
| ① | 340 | 520 | `①` |
| ② | 500 | 580 | `②` |
| ③ | 700 | 680 | `③` |
| ④ | 1020 | 750 | `④` |
| ⑤ | 1150 | 820 | `⑤` |
| ⑥ | 1280 | 880 | `⑥` |

Circle style: Fill `#7C3AED` | Stroke: none | Text: `#FFFFFF` bold 12px

---

## 9. Agent Nodes (6 agents in 2 rows)

All agents: Width=290px, Height=145px | Rounded ON

**Base style:** Fill `#2D1B69` | Stroke `#4C1D95` | Stroke width: 1

**Row 1 positions (y=570):**

| Agent | x | Title | DNA Badge? | Special Badge |
|---|---|---|---|---|
| Assessment Agent | 55 | `① Assessment Agent` | — | `DIAGNOSTIC` grey |
| Memory Agent | 365 | `② Memory Agent` | YES ✅ | — |
| Tutor Agent | 675 | `③ Tutor Agent` | YES ✅ | — |

**Row 2 positions (y=735):**

| Agent | x | Title | DNA Badge? | Special Badge |
|---|---|---|---|---|
| Verification Agent | 55 | `⑤ Verification Agent` | — | `COMPREHENSION` grey |
| Weakness Intel Agent | 365 | `Weakness Intel Agent` | — | `⏰ CRON` amber |
| Insight Agent | 675 | `Insight Agent` | — | `WEEKLY REPORT` grey |

**For each agent, inside the box:**
- Title: 13px bold, `#F9FAFB`, top-center
- Description: 10px, `#9CA3AF`, middle
- `Mastra.AI` chip: Fill `#7C3AED`, text white, 9px, bottom-right
- `Python` chip: next to Mastra badge

**🧬 Learning DNA badge (Memory Agent + Tutor Agent):**  
Draw a small rectangle, 110px × 22px, top-right of agent box  
Fill: `#78350F` | Stroke: `#F59E0B` | Text: `🧬 Learning DNA` | 9px | Color: `#FCD34D`

**⏰ CRON badge (Weakness Intel Agent):**  
Draw a small rectangle, 80px × 22px, top-right  
Fill: `#78350F` | Stroke: `#D97706` | Dashed border | Text: `⏰ CRON` | 9px | Color: `#FCD34D`

---

## 10. Adaptive Teaching Engine Sidebar

Position: x=985, y=480, Width=220px, Height=310px  
Fill: `#1A0F3A` | Stroke: `#7C3AED` | Dashed border | Rounded: ON  
Label: `🎓 Adaptive Teaching Engine` | 13px bold | Color: `#A78BFA`

**5 level cards (stacked, y increments of 50px, starting y=520):**

Each card: Width=195px, Height=40px | Fill: `#0F0A2A` | Stroke: `#374151` | Rounded

| Card | Label | Left border color |
|---|---|---|
| Level 1 | `Level 1 — Simple Explanation` | Draw thin 4px rect on left edge in `#22C55E` |
| Level 2 | `Level 2 — Example-Based` | `#84CC16` |
| Level 3 | `Level 3 — Common Mistakes` | `#EAB308` |
| Level 4 | `Level 4 — Visual Analogy` | `#F97316` |
| Level 5 | `Level 5 — Exam Coaching` | `#EF4444` |

Font: 10px | Color: `#F9FAFB`

> **Trick for color left border in Excalidraw:** Draw a thin 4px-wide tall rectangle on the left side of each card in the respective color. It overlaps the card's left edge to simulate a CSS left border.

---

## 11. Qdrant 5 Collection Cards (Band 4A)

5 cards inside the Qdrant band, stacked vertically with 8px gaps.  
Each card: Width=615px, Height=44px | Fill: `#0C3547` | Stroke: `#164E63` | Rounded

Starting y=1040, x=45, y increments of 52px:

| Card | Left label | Right annotation |
|---|---|---|
| 1 | `📊 learning_dna` | `Primary Digital Twin Store` |
| 2 | `🔍 past_doubts` | `Semantic doubt history · top-K=3` |
| 3 | `📝 explanation_history` | `Teaching outcomes per student` |
| 4 | `📋 session_logs` | `Raw transcripts for Weakness Agent` |
| 5 | `⚠️ weak_concepts` | `Clustered failure patterns` |

Left label: 11px bold, `#67E8F9`  
Right annotation: 9px, `#9CA3AF`

**Learning DNA callout (right of Qdrant, outside band):**  
Draw at x=720, y=1020, Width=210px, Height=140px  
Fill: `#0C2A40` | Stroke: `#F59E0B` | Rounded  
Content:
```
🧬 Learning DNA
• Mastery score per concept
• Preferred teaching level
• Frustration index
• Analogy effectiveness history
• Memory retention curve
```
Font: 10px | Color: `#FCD34D`

**Ebbinghaus Decay callout (below DNA callout):**  
x=720, y=1175, Width=210px, Height=70px  
Fill: `#0C2A40` | Stroke: `#6366F1`  
```
📉 Ebbinghaus Concept Decay
Nightly cron: mastery × 0.85
per unreviewed concept
```
Font: 10px | Color: `#A5B4FC`

---

## 12. Enkrypt Sub-Components (Band 4B)

**4 validator cards** (stacked, same dimensions as Qdrant cards):  
Width=615px, Height=44px | Fill: `#350808` | Stroke: `#7F1D1D`  
x=725, starting y=1040

| Card | Label | Annotation |
|---|---|---|
| 1 | `∑ Math Accuracy Validator` | `JEE calculus · step-by-step logic` |
| 2 | `🔬 Science Fact Validator` | `NEET/Physics/Chemistry cross-reference` |
| 3 | `🚫 Hallucination Detector` | `UPSC claims vs NCERT reference corpus` |
| 4 | `📚 Pedagogy Evaluator` | `Tutor mode vs answer-key mode` |

**Confidence Scorer card (below validators):**  
Height=55px | Fill: `#4A0808` | Stroke: `#DC2626` | Stroke width: 2  
Label:
```
📊 Confidence Scorer
conf = 0.35×math + 0.30×sci + 0.20×(1−hallucination) + 0.15×pedagogy
```
Font: 10px | Color: `#FCA5A5`

**Safety Threshold annotation (below scorer):**
```
≥ 0.90 → ✅ Pass to Verification
0.75–0.89 → 🟡 HITL Expert Review  
< 0.75 → ⚠️ Regenerate (max 2×)
```

---

## 13. HITL Node and Fallback

**HITL Node:**  
x=1290, y=1070, Width=190px, Height=82px  
Fill: `#1A3A1A` | Stroke: `#22C55E` | Dashed | Rounded  
Label: `👨‍🏫 HITL Expert Review` | 12px | `#86EFAC`  
Sub: `Triggered: Score 0.75–0.89` | 9px | `#9CA3AF`

**Textbook Fallback:**  
x=980, y=1360, Width=210px, Height=52px  
Fill: `#1A0000` | Stroke: `#DC2626` | Dashed | Rounded  
Label: `📖 Verified Textbook Fallback` | 11px | `#FCA5A5`

---

## 14. Student Output Node

x=1350, y=1100, Width=120px, Height=120px  
Shape: Ellipse (`O` key in Excalidraw)  
Fill: `#1A2A1A` | Stroke: `#22C55E` | Stroke: 2  
Label: `👤 Student` | 13px bold | `#F9FAFB`

---

## 15. MySQL Foundation (Band 5)

6 pill shapes, y=1375, evenly distributed:  
Width=165px | Height=32px | Fill: `#1F2937` | Stroke: `#374151` | Rounded  
Labels: `Users` `Courses` `Quiz Scores` `XP Ledger` `Portfolios` `Skill Graph`  
Font: 11px | Color: `#FCD34D`

---

## 16. Legend Box

x=1310, y=1400, Width=250px, Height=210px  
Fill: `#0F1117` | Stroke: `#374151` | Rounded  
Title: `Legend` | 12px bold | `#9CA3AF`

Content (multi-line text with colored squares):
Draw small 12×12 filled squares before each line in the arrow color:

```
■  Mastra Orchestration
■  Qdrant Memory / RAG
■  Twin Mutation
■  Enkrypt Safety
□  Async / CRON / HITL (dashed)
□  Standard HTTP Flow

🧬  Learning DNA Component
⏰  Background CRON Workflow
①–⑥  Execution Sequence
```

---

## 17. Arrow Drawing Sequence (Draw arrows LAST)

Select the arrow tool (`A` key). For each arrow:
1. Click source component center
2. Click destination component center
3. With arrow selected, change color in right panel

**Arrow drawing order (follow this to avoid messy overlaps):**

```
Step 1: User Layer → Flask Gateway (grey)
Step 2: Flask Gateway → DAG Orchestrator (grey)
Step 3: DAG Orchestrator → all 6 agents (purple fan-out)
Step 4: Memory Agent → Qdrant collections × 3 (cyan parallel)
Step 5: Memory Agent → Tutor Agent (cyan, label: Hydrated Twin Context)
Step 6: Assessment Agent → learning_dna (cyan)
Step 7: Tutor Agent → Enkrypt validators (red)
Step 8: Confidence Scorer → Verification Agent (green, Pass)
Step 9: Confidence Scorer → Tutor Agent (RED DASHED CURVED, Regenerate)
Step 10: Confidence Scorer → HITL Node (amber dashed)
Step 11: Confidence Scorer → Textbook Fallback (red)
Step 12: Verification Agent → Student (green)
Step 13: Verification Agent → learning_dna (green, mutate mastery)
Step 14: Verification Agent → explanation_history (green, upsert)
Step 15: Weakness Intel Agent → session_logs (cyan)
Step 16: Weakness Intel Agent → weak_concepts (green, upsert)
Step 17: Weakness Intel Agent → learning_dna (green, update weakness_state)
Step 18: Weakness Intel Agent → Insight Agent (purple)
Step 19: Insight Agent → MySQL (green, Push Revision Plan)
Step 20: MySQL → DAG Orchestrator (amber, Deterministic Ground Truth)
Step 21: Tutor Agent → Teaching Engine sidebar (purple dashed)
Step 22: HITL Node → learning_dna (green dashed, Expert-Verified)
```

**Regeneration loop (Step 9) is the most important arrow:**  
In Excalidraw, after drawing the arrow, drag the midpoint to create a curve.  
Make it arc BELOW the Enkrypt band and loop back LEFT to the Tutor Agent.  
Set: Stroke color `#EF4444` | Width: 3 | Dashed: ON  
Add label in the middle of the arc: `⚠️ Regenerate Response`

---

## 18. Final Export

1. Select All (`Ctrl+A`)
2. File → Export Image
3. Format: SVG (preferred) or PNG
4. Scale: 2× for PNG
5. Background: `#0A0A0F` (checked)
6. Save as: `architecture_v2.png` or `.svg`

**Submission format:** Upload PNG as the Architecture Diagram field in the hackathon form.
