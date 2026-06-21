const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'Round-1');

function getFileContent(filename) {
    const filePath = path.join(dir, filename);
    if (fs.existsSync(filePath)) {
        return fs.readFileSync(filePath, 'utf-8');
    }
    return '';
}

const execSummary = getFileContent('Executive_Summary.md');
const sampleSession = getFileContent('Sample_Student_Session.md');

const newContent = `---
title: Mentra X - Supporting Documentation
---

<div style="text-align: center; margin-top: 200px;">
  <h1>MENTRA X</h1>
  <h2>Supporting Documentation</h2>
  <br/>
  <h4>Built By:<br/>Sujith Kumar AI</h4>
  <br/>
  <p>HiDevs × Mastra Hackathon 2026</p>
</div>

<div style="page-break-after: always;"></div>

## Table of Contents

1. Executive Summary
2. Sample Student Session
3. Learning DNA Evolution
4. Weakness Intelligence Workflow
5. Weekly Progress Report Example
6. Enkrypt Validation Example
7. Innovation Highlights
8. Expected Impact

<div style="page-break-after: always;"></div>

# 1. Executive Summary

${execSummary.replace(/# Mentra X — Executive Summary/g, '').replace(/\*\*One-page briefing for hackathon judges.\*\*/g, '')}

<div style="page-break-after: always;"></div>

# 2. Sample Student Session

${sampleSession.replace(/# Mentra X — Sample Student Session/g, '')}

<div style="page-break-after: always;"></div>

# 3. Learning DNA Evolution

This section demonstrates how the Qdrant-backed Learning DNA mutates over time based on student interaction.

### Session 1 End State
After failing to comprehend "Entropy" using a mathematical approach (Level 2).
* **Mastery:** 0.00 (Unknown/Failed)
* **Retention:** Baseline
* **Learning Style:** Visual (Identified via onboarding)
* **Preferred Teaching Level:** 2 (Default)
* **Weaknesses:** None formally logged yet (1 mistake registered)
* **Frustration Index:** 0.23 (Elevated post-failure)

### Session 3 End State
After successful comprehension using a Visual Analogy approach (Level 4) on Entropy, but subsequent struggles with "Carnot Efficiency".
* **Mastery:** Entropy (0.05 - Developing), Carnot (0.00 - Failed)
* **Retention:** Concept Decay triggered for Entropy (-0.01 per day)
* **Learning Style:** Visual (Strongly reinforced)
* **Preferred Teaching Level:** 4 (Updated based on success)
* **Weaknesses:** Carnot Efficiency (Flagged)
* **Frustration Index:** 0.18 (Stabilized)

### Session 5 End State
After the Mastra CRON job runs semantic clustering on multiple failures.
* **Mastery:** Entropy (0.04 - Decaying), Carnot (0.00 - Failed), Clausius Inequality (0.10)
* **Retention:** Entropy requires spaced repetition soon.
* **Learning Style:** Visual
* **Preferred Teaching Level:** 4
* **Weaknesses:** Macro-Cluster Detected: "Second Law & Heat Engine Applications" (High Severity)
* **Frustration Index:** 0.25 (Rising due to Carnot struggles)

<div style="page-break-after: always;"></div>

# 4. Weakness Intelligence Workflow

**Scenario:** Student repeatedly struggles with the concept of "Carnot Efficiency".

**1. Question (Student Input):** "Why can't a heat engine be 100% efficient? The math makes no sense to me."

**2. Detection (Mastra CRON / Qdrant):**
The Weakness Intel Agent fires asynchronously after the 5th session. It fetches all failed concepts from the \`session_logs\` Qdrant collection. It runs semantic clustering (Cosine Similarity > 0.75) and detects a repeating pattern around Heat Engines.

**3. Escalation:**
The agent mutates the student's \`weakness_state\` in the Digital Twin, flagging "Carnot Efficiency" as a CRITICAL severity weakness.

**4. Adaptive Explanation (Tutor Agent):**
In the next session, the Tutor Agent retrieves the Digital Twin, sees the CRITICAL flag, and bypasses standard Level 2 mathematical explanations. Knowing the student is a Visual learner (from Learning DNA), it jumps straight to Level 4 (Visual Analogy) using a "Water Wheel" analogy to explain thermal reservoirs.

**5. Improvement:**
The Verification Agent issues a micro-quiz. The student passes. The Learning DNA is mutated to reflect a mastery gain (+0.05), and the Frustration Index drops.

<div style="page-break-after: always;"></div>

# 5. Weekly Progress Report Example

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊  MENTRA X WEEKLY LEARNING REPORT
     Aryan | JEE Advanced | Week 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 PROGRESS THIS WEEK
  Sessions completed: 5
  XP Earned: 220
  Doubts resolved: 3 / 6

📈 MASTERY GAINS
  ✅ Entropy (Second Law)        0.00 → 0.05  [Level 4 analogy worked]
  ✅ Kinematics (Projectile)     0.55 → 0.72  [Strong]
  ✅ Algebra (Quadratic)         0.80 → 0.85  [Near mastery]

⚠️  CRITICAL WEAKNESSES
  🔴 Carnot Efficiency           Mastery: 0.00  [4 failures]
  🟠 Clausius Inequality         Mastery: 0.10  [2 failures]
  🟡 Wave Optics: Diffraction    Mastery: 0.15  [1 failure]

🎯 YOUR 3-DAY REVISION PLAN
  Day 1: Carnot Cycle — Level 4 Visual Session
          "Understand why efficiency can never be 100%"
  Day 2: Clausius Inequality — Worked Examples (Level 3)
          "The math behind entropy bookkeeping"
  Day 3: Mix Session — Full Thermodynamics Mock Problem Set

💡 LEARNING DNA INSIGHT
  Your LEGO analogy breakthrough shows Visual explanations
  work 3x better for you than formula-first approaches.
  All future sessions will default to Level 4 teaching.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<div style="page-break-after: always;"></div>

# 6. Enkrypt Validation Example

**Input Response (From Tutor Agent):**
"Entropy represents disorder. For example, when you drop a glass, it shatters, increasing entropy. The formula is ΔS = Q/T. Therefore, entropy always strictly increases in every single thermodynamic process, even reversible ones."

**Validation Checks (Enkrypt Middleware):**
* ✓ **Math Validator:** Checks \`ΔS = Q/T\`. Formula is correct. (Score: 1.0)
* ✓ **Science Validator:** Checks "entropy always strictly increases in every single thermodynamic process, even reversible ones." → **FLAGGED.** In a reversible process, entropy change of the universe is ZERO. (Score: 0.3)
* ✓ **Hallucination Validator:** Checks for grounded reality. Concept holds, but scientific constraint is violated. (Score: 0.6)
* ✓ **Pedagogy Validator:** Dropped glass analogy is standard and effective. (Score: 0.9)

**Confidence Score:**
Calculated via weighted matrix: \`(0.35 × Math) + (0.30 × Science) + (0.20 × Hallucination) + (0.15 × Pedagogy)\`
Total Score = \`0.35 + 0.09 + 0.12 + 0.135\` = **0.695**

**Final Decision:**
Score < 0.75 → **REJECT & REGENERATE.** 
The response is blocked from reaching the student. A regeneration loop is triggered in Mastra with the specific Science Validator failure context attached.

<div style="page-break-after: always;"></div>

# 7. Innovation Highlights

1. **Student Digital Twin:** Moving away from generic prompting to a persistent, 1536-dimensional vectorized cognitive model of the student stored in Qdrant.
2. **Learning DNA:** Tracking not just what the student knows, but *how* they learn (Level 1-5 preference, frustration indexing, analogy effectiveness).
3. **Stateful Memory RAG:** Utilizing 5 specialized Qdrant collections to fetch historical contexts, past failures, and behavioral states in parallel before generating a response.
4. **Adaptive Learning:** A 5-tier teaching escalation engine that dynamically shifts from simple definitions to visual analogies to exam-coaching modes based on real-time twin data.
5. **Multi-Agent Swarm:** Leveraging Mastra's Directed Acyclic Graph (DAG) orchestration to separate assessment, memory, tutoring, and verification into discrete, specialized agent nodes.
6. **Enkrypt Safety Layer:** An enterprise-grade, mathematically weighted validation middleware that prevents scientific hallucinations and guarantees mathematical accuracy via human-in-the-loop (HITL) and textbook fallbacks.

<div style="page-break-after: always;"></div>

# 8. Expected Impact

Mentra X targets the most high-stakes educational demographics in the world:

* **JEE Aspirants:** Replacing generic physics/math doubt apps with rigorous, Enkrypt-verified explanations that adapt to individual frustration thresholds.
* **NEET Aspirants:** Helping biology and chemistry students track long-term memorization through Qdrant concept decay modeling.
* **UPSC Aspirants:** Organizing massive syllabi by mapping exact weakness clusters across diverse subjects using the Mastra CRON clustering engine.
* **CAT Aspirants:** Adapting logical reasoning explanations to specific learning styles (visual vs. rule-based).
* **Board Students:** Democratizing access to an elite, personalized tutor that remembers their specific struggles from the beginning of the academic year to the final exam.

**Educational Impact:** Transitioning EdTech from "search engines for homework" to true, stateful, one-on-one personalized pedagogy at scale.

---
Built by Sujith Kumar AI
HiDevs × Mastra Hackathon 2026
---
`;

fs.writeFileSync(path.join(dir, 'Supporting_Document_final.md'), newContent);
console.log("Restructured Supporting_Document_final.md successfully.");
