# Mentra X Architecture Copilot V4 Input Specification

**INSTRUCTIONS FOR ARCHITECTURE COPILOT:**
Do NOT use dense text descriptions. Represent each bullet point and item as a distinct visual node or sub-card. Follow the structural hierarchy below explicitly.

==================================================
## SECTION 1: PROJECT HEADER
==================================================

**Mentra X**
*AI-Powered Student Digital Twin*
*Learning DNA + Cognitive Swarm + Stateful Memory RAG*

**Target Users (Render as horizontal pills):**
- JEE Aspirants
- NEET Aspirants
- UPSC Aspirants
- CAT Aspirants
- Board Exam Students

==================================================
## SECTION 2: LAYERS
==================================================

Render the diagram using the following top-to-bottom band structure:
- **Layer 1:** Student Interface
- **Layer 2:** Mastra Cognitive Swarm
- **Layer 3:** Digital Twin Layer
- **Layer 4:** Qdrant Learning DNA Memory Engine
- **Layer 5:** Enkrypt Safety Layer
- **Layer 6:** MySQL Foundation

==================================================
## SECTION 3: MASTRA DAG ORCHESTRATOR
==================================================

**Central Node:** `Mastra DAG Orchestrator`

**Connections (Show clear fan-out from Orchestrator to all agents):**
- → Assessment Agent
- → Memory Agent
- → Tutor Agent
- → Verification Agent
- → Weakness Intel Agent
- → Insight Agent

==================================================
## SECTION 4: AGENTS
==================================================

Render these as 6 distinct nodes.

**1. Assessment Agent**
- Diagnostic Assessment
- Knowledge Mapping

**2. Memory Agent**
- Retrieve Learning DNA
- Retrieve Past Doubts
- Retrieve Weak Concepts

**3. Tutor Agent**
- Adaptive Teaching
- Personalized Explanation

**4. Verification Agent**
- Generate Quiz
- Validate Understanding

**5. Weakness Intel Agent [CRON]** *(Add visible CRON badge)*
- Detect Weak Areas
- Generate Revision Plans

**6. Insight Agent [WEEKLY]** *(Add visible WEEKLY badge)*
- Generate Reports
- Track Progress

==================================================
## SECTION 5: DIGITAL TWIN
==================================================

**Main Node:** `Student Digital Twin`

**Sub-components (Render as separate elements, not plain text):**
- Academic State
- Knowledge State
- Skill State
- Learning DNA
- Weakness State
- Progress State

**Learning DNA contains:**
- Mastery
- Learning Style
- Behavior
- Retention
- Weakness Patterns

==================================================
## SECTION 6: QDRANT
==================================================

**Main Container:** `Qdrant Learning DNA Memory Engine`
*(Ensure fully visible and not truncated)*

**Annotations (Render as floating badges/tags):**
- Stateful Memory RAG
- 1536-dim Embeddings
- Cosine Similarity
- HNSW Index
- Concept Decay Tracking

**Collections (Render as 5 distinct sub-cards inside the container):**
- `learning_dna`
- `past_doubts`
- `explanation_history`
- `session_logs`
- `weak_concepts`

**Connections:**
- Show parallel retrieval arrows from Memory Agent to multiple collections.

==================================================
## SECTION 7: ADAPTIVE TEACHING ENGINE
==================================================

Render as a dedicated sidebar or component block:
- **Level 1:** Simple Explanation
- **Level 2:** Worked Example
- **Level 3:** Common Mistakes
- **Level 4:** Visual Analogy
- **Level 5:** Exam Coaching Mode

==================================================
## SECTION 8: ENKRYPT SAFETY
==================================================

**Main Container:** `Enkrypt Safety Layer`

**Validators (Render as 4 distinct sub-cards, NOT text lists):**
- Hallucination Validator
- Math Validator
- Science Validator
- Pedagogy Validator

**Sub-node:** `Confidence Scoring`

**Decision Rules (Render as distinct conditional branches):**
- **Score > 0.90:** → Approve
- **0.75–0.89:** → HITL Review *(Render `HITL Review` node)*
- **Score < 0.75:** → Regenerate Response *(Draw a visible RED regeneration loop back to Tutor Agent)*
- **Double Failure:** → Verified Textbook Fallback *(Render `Verified Textbook Fallback` node)*

==================================================
## SECTION 9: WORKFLOW
==================================================

Annotate the primary flow paths with sequence numbers:
1. Assessment
2. Memory Retrieval
3. Tutor Reasoning
4. Enkrypt Validation
5. Verification
6. Student Response

==================================================
## SECTION 10: VISUAL REQUIREMENTS
==================================================

**Architecture Copilot Directives:**
- Ensure Qdrant container is fully visible and placed centrally or prominently.
- Explicitly draw Collection sub-cards inside Qdrant.
- Explicitly draw Validator sub-cards inside Enkrypt.
- Explicitly draw HITL node.
- Explicitly draw Verified Textbook Fallback node.
- Include Learning DNA badge on Tutor and Memory Agents.
- Include CRON badge on Weakness Intel Agent.
- Include WEEKLY badge on Insight Agent.
- Show distinct parallel retrieval lines from Memory Agent to Qdrant.
- Draw a prominent, colored regeneration loop for Enkrypt failure.
- Avoid large text paragraphs. Favor separate nodes over descriptions.
