# Mentra X — Architecture Diagram v2 (Draw.io Specification)

**Purpose:** Step-by-step guide to build the v2 architecture diagram in draw.io (diagrams.net).  
**File format when exported:** `.drawio` XML or PNG/SVG

---

## Setup

1. Go to [diagrams.net](https://app.diagrams.net)
2. Create → Blank Diagram
3. File → Page Setup → Width: 2400px, Height: 1600px
4. View → Grid → OFF
5. View → Connection Points → ON
6. Format Panel → Background Color: `#0A0A0F`

---

## Layer Configuration (draw.io Layers Panel)

Create 7 layers (Edit → Layers):

| Layer | Name | Purpose |
|---|---|---|
| 1 | `Background Bands` | Colored band rectangles |
| 2 | `Title Block` | Project name, subtitle |
| 3 | `User Layer` | 3 frontend components |
| 4 | `Gateway` | Flask API gateway |
| 5 | `Mastra Swarm` | Orchestrator + 6 agents |
| 6 | `Memory & Safety` | Qdrant + Enkrypt |
| 7 | `Arrows` | All connection lines |
| 8 | `Annotations` | Callouts, legends, badges |

---

## Component Specifications

### Band Rectangles (Layer 1)

Use `Extras → Edit Diagram` to paste shapes, or draw using the Rectangle tool.

For each band:
- Shape: `mxgraph.basic.rect`
- Style: `rounded=1; fillColor=<hex>; strokeColor=<hex>; strokeWidth=1;`

| Band | Fill | Border | y-position | Height |
|---|---|---|---|---|
| User Layer | `#111827` | `#1D4ED8` | 100 | 140 |
| Flask Gateway | `#1F2937` | `#374151` | 260 | 90 |
| Mastra Swarm | `#1E1347` | `#7C3AED` | 370 | 520 |
| Qdrant (left) | `#062030` | `#0891B2` | 910 | 320 |
| Enkrypt (right) | `#200808` | `#DC2626` | 910 | 320 |
| MySQL | `#111827` | `#374151` | 1250 | 110 |

---

### Title Block (Layer 2)

Insert → Text elements:

**Line 1:** `MENTRA X`  
Style: `fontSize=32; fontStyle=1; fontColor=#F9FAFB; align=left;`  
Position: x=40, y=20

**Line 2:** `AI-Powered Student Digital Twin`  
Style: `fontSize=16; fontColor=#A78BFA; align=left;`  
Position: x=40, y=65

**Line 3:** `Learning DNA  ·  Cognitive Swarm  ·  Stateful Memory RAG`  
Style: `fontSize=11; fontColor=#9CA3AF; fontStyle=2; align=left;`  
Position: x=40, y=88

**Target Users pills (5 rounded rectangles):**

For each pill `[ JEE ] [ NEET ] [ UPSC ] [ CAT ] [ Board Exams ]`:
- Style: `rounded=1; fillColor=#1F2937; strokeColor=#374151; fontColor=#F59E0B; fontSize=11;`
- Width: 70px, Height: 28px
- Position: y=112, x increments: 40, 120, 200, 280, 380

---

### User Layer Components (Layer 3)

3 component boxes at y=120, height=100px each:

**Study Dashboard** (x=50):
```
Style: rounded=1; fillColor=#1F2937; strokeColor=#1D4ED8; fontColor=#F9FAFB; fontSize=12; fontStyle=1;
Label: STUDY DASHBOARD
Sub-label via HTML: <div style="font-size:10px; color:#9CA3AF">Learning DNA Heatmap · XP · Streak · Weak Alerts</div>
```

**Cognitive Chat UI** (x=400):
```
Same style, Label: COGNITIVE CHAT UI
Sub: Real-time Doubt Interface via WebSocket
```

**LMS Video Player** (x=750):
```
Same style, Label: LMS VIDEO PLAYER
Sub: Context-aware · progress tracked
```

**Tech Chip (React, WebSockets):** Insert small text boxes at bottom of each component:
- Style: `rounded=1; fillColor=#111827; strokeColor=#374151; fontColor=#9CA3AF; fontSize=9;`
- Height: 18px, y near bottom of parent component

---

### Flask API Gateway (Layer 4)

Single container at y=260, h=90px, full width minus margins.

**4 chip shapes inside (inline):**
Style: `rounded=1; fillColor=#111827; strokeColor=#374151; fontColor=#9CA3AF; fontSize=11;`
Labels: `JWT Auth`, `Rate Limiter`, `Session Manager`, `Route Guard`
Width: 160px each, height: 40px, spaced evenly

---

### Mastra DAG Orchestrator (Layer 5, top of Swarm band)

**Shape:** Rounded rectangle with diamond accent  
Position: Horizontally centered, y=395 (top of swarm band + 25px padding)  
Width: 320px, Height: 70px  
Style: `rounded=1; fillColor=#4C1D95; strokeColor=#7C3AED; strokeWidth=3; fontColor=#E9D5FF; fontSize=14; fontStyle=1;`  
Label: `◆ Mastra DAG Orchestrator`  
Sub-label: Add second text element below: `Graph-based Multi-Agent Coordinator`  
Style sub: `fontColor=#A78BFA; fontSize=10;`

**Execution number badges (circled numbers):**
For each ①②③⑤ insert small circle shapes (24px diameter):
Style: `ellipse; fillColor=#7C3AED; strokeColor=#7C3AED; fontColor=#FFFFFF; fontSize=12; fontStyle=1;`

---

### Agent Nodes (Layer 5, 2 rows of 3)

**All agents:** Width=280px, Height=140px

Style base:
```
rounded=1; fillColor=#2D1B69; strokeColor=#4C1D95; fontColor=#F9FAFB; fontSize=11; fontStyle=1;
```

**Row 1 positions (y=490):**
- Assessment Agent: x=50
- Memory Agent: x=380
- Tutor Agent: x=710

**Row 2 positions (y=680):**
- Verification Agent: x=50
- Weakness Intel Agent: x=380
- Insight Agent: x=710

**Learning DNA badge (Memory Agent and Tutor Agent):**
Small rectangle overlaid at top-right of agent box:
Style: `rounded=1; fillColor=#78350F; strokeColor=#F59E0B; fontColor=#FCD34D; fontSize=9; fontStyle=1;`
Label: `🧬 Learning DNA`
Width: 100px, Height: 22px

**CRON badge (Weakness Intel Agent):**
Style: `rounded=1; fillColor=#78350F; strokeColor=#D97706; fontColor=#FCD34D; fontSize=9; dashed=1;`
Label: `⏰ CRON`

---

### Adaptive Teaching Engine Sidebar (Layer 8)

Position: x=1050, y=440, Width=200px, Height=300px

Container style: `rounded=1; fillColor=#1A0F3A; strokeColor=#7C3AED; strokeWidth=1; dashed=1;`
Label: `🎓 Adaptive Teaching Engine`

5 level cards inside (y increments of 48px):
| Level | Label | Left border color |
|---|---|---|
| 1 | `Level 1 — Simple Explanation` | `#22C55E` |
| 2 | `Level 2 — Example-Based` | `#84CC16` |
| 3 | `Level 3 — Common Mistakes` | `#EAB308` |
| 4 | `Level 4 — Visual Analogy` | `#F97316` |
| 5 | `Level 5 — Exam Coaching` | `#EF4444` |

Card style: `rounded=1; fillColor=#0F0A2A; strokeColor=#374151; fontColor=#F9FAFB; fontSize=10;`
Add a 4px wide rectangle on the left edge of each card in the respective color.

---

### Qdrant Memory Engine (Layer 6, left half of Band 4)

Container: x=50, y=910, Width=580px, Height=320px

Style: `rounded=1; fillColor=#062030; strokeColor=#0891B2; strokeWidth=2; fontColor=#22D3EE; fontSize=14; fontStyle=1;`

**5 collection cards (stacked, full width):**

Each card: Width=540px, Height=42px, y increments of 50px starting at y=970

Style: `rounded=1; fillColor=#0C3547; strokeColor=#164E63; fontColor=#67E8F9; fontSize=11; fontStyle=1;`

Labels (left-aligned with annotation right-aligned):
- `📊 learning_dna` + `Primary Digital Twin Store`
- `🔍 past_doubts` + `Semantic doubt history`
- `📝 explanation_history` + `Teaching outcomes`
- `📋 session_logs` + `Raw session transcripts`
- `⚠️ weak_concepts` + `Clustered failure patterns`

**Learning DNA Callout Box:**
Position: x=640, y=940, Width=200px, Height=130px
Style: `rounded=1; fillColor=#0C2A40; strokeColor=#F59E0B; fontColor=#FCD34D; fontSize=10;`
Content (multi-line label):
```
🧬 Learning DNA
• Mastery per concept
• Preferred level
• Frustration index
• Analogy effectiveness
• Memory retention curve
```

**Ebbinghaus Decay Callout:**
Position: x=640, y=1090, Width=200px, Height=60px
Style: `rounded=1; fillColor=#0C2A40; strokeColor=#6366F1; fontColor=#A5B4FC; fontSize=10;`
Label: `📉 Concept Decay\nNightly: mastery × 0.85\nper unreviewed concept`

---

### Enkrypt Safety Layer (Layer 6, right half of Band 4)

Container: x=680, y=910, Width=580px, Height=320px

Style: `rounded=1; fillColor=#200808; strokeColor=#DC2626; strokeWidth=2; fontColor=#FCA5A5; fontSize=14; fontStyle=1;`

**4 Validator cards (stacked):**

Each card: Width=540px, Height=40px
Style: `rounded=1; fillColor=#350808; strokeColor=#7F1D1D; fontColor=#FCA5A5; fontSize=11;`

Labels:
- `∑ Math Accuracy Validator`
- `🔬 Science Fact Validator`
- `🚫 Hallucination Detector`
- `📚 Pedagogy Evaluator`

**Confidence Scorer card (below validators):**
Height: 55px, Style: `rounded=1; fillColor=#4A0808; strokeColor=#DC2626; strokeWidth=2; fontColor=#FCA5A5; fontSize=11; fontStyle=1;`
Label: `📊 Confidence Scorer\nconf = 0.35×math + 0.30×sci + 0.20×hallu + 0.15×ped`

---

### HITL Node (Layer 8)

Position: x=1280, y=1050, Width=180px, Height=80px

Style: `rounded=1; fillColor=#1A3A1A; strokeColor=#22C55E; strokeWidth=1; dashed=1; fontColor=#86EFAC; fontSize=11;`
Label: `👨‍🏫 HITL Expert Review\nScore 0.75–0.89 Warning`

---

### Textbook Fallback Node (Layer 8)

Position: x=1000, y=1260, Width=200px, Height=50px

Style: `rounded=1; fillColor=#1A0000; strokeColor=#DC2626; dashed=1; fontColor=#FCA5A5; fontSize=11;`
Label: `📖 Verified Textbook Fallback`

---

### MySQL Foundation (Layer 5)

Container: x=50, y=1250, full width, Height=110px

Style: `rounded=1; fillColor=#111827; strokeColor=#374151; fontColor=#FCD34D; fontSize=14; fontStyle=1;`

6 pill chips inline:
Style: `rounded=1; fillColor=#1F2937; strokeColor=#374151; fontColor=#FCD34D; fontSize=11;`
Labels: `Users`, `Courses`, `Quiz Scores`, `XP Ledger`, `Portfolios`, `Skill Graph`

---

### Student Output Node (Layer 5)

Position: x=1300, y=1090, Width=120px, Height=120px

Style: `ellipse; fillColor=#1A2A1A; strokeColor=#22C55E; strokeWidth=2; fontColor=#F9FAFB; fontSize=12; fontStyle=1;`
Label: `👤 Student`

---

### Legend Box (Layer 8)

Position: x=1280, y=1380, Width=240px, Height=200px

Style: `rounded=1; fillColor=#0F1117; strokeColor=#374151; fontColor=#9CA3AF; fontSize=10;`

Label (multi-line):
```
LEGEND
──── Mastra Orchestration (purple)
──── Qdrant Memory RAG (cyan)
──── Twin Mutation (green)
──── Enkrypt Safety (red)
- - - Async / CRON / HITL (dashed)
──── Standard HTTP (grey)
```

---

## Arrow Styles

In draw.io, set these edge styles for each arrow type:

**Mastra (purple):**
`edgeStyle=orthogonalEdgeStyle; strokeColor=#8B5CF6; strokeWidth=2; fontColor=#A78BFA; fontSize=10;`

**Qdrant/Memory (cyan):**
`edgeStyle=orthogonalEdgeStyle; strokeColor=#06B6D4; strokeWidth=2; fontColor=#22D3EE; fontSize=10;`

**Twin Mutation (green):**
`edgeStyle=orthogonalEdgeStyle; strokeColor=#22C55E; strokeWidth=2; fontColor=#86EFAC; fontSize=10;`

**Enkrypt Safety (red):**
`edgeStyle=orthogonalEdgeStyle; strokeColor=#EF4444; strokeWidth=2; fontColor=#FCA5A5; fontSize=10;`

**Regeneration loop (red dashed curved):**
`curved=1; edgeStyle=elbowEdgeStyle; strokeColor=#EF4444; strokeWidth=3; dashed=1; fontColor=#FCA5A5; fontSize=10;`

**HITL / async (dashed):**
`dashed=1; strokeColor=#D97706; strokeWidth=1.5; fontColor=#FCD34D; fontSize=10;`

**Standard (grey):**
`edgeStyle=orthogonalEdgeStyle; strokeColor=#6B7280; strokeWidth=1.5; fontColor=#9CA3AF; fontSize=10;`

---

## Export Settings

- File → Export As → PNG
- Scale: 200% (for high-resolution submission)
- Background: Include background (checked)
- Transparent: Unchecked

Or export SVG for lossless quality.
