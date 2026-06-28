# Mentra X — Round 2 Demo Playbook

**Owner:** Sujith Kumar AI  
**Timing:** Exactly 5 Minutes  
**Target Audience:** Hackathon Judges (Technical + Product)  

## 1. Demo Story
**The Narrative:** Aryan is a 17-year-old JEE aspirant from a Tier-2 city. He is bright but struggles with abstract concepts in Physics. Standard coaching classes move too fast, and basic AI chatbots give him generic formulas that he memorizes but doesn't understand. 

Today, Aryan is stuck on "Thermodynamics: Entropy". We are going to show how Mentra X doesn't just give him the answer—it checks his *Learning DNA*, realizes he needs a visual analogy, guarantees the answer is safe via Enkrypt, and updates his cognitive twin based on his comprehension.

## 2. Demo Data (Pre-Seeded)
Before the demo, the database must contain:
- **User:** Aryan (ID: 101, Track: JEE)
- **Twin State:** 
  - `knowledge_state`: Thermodynamics (0.3/1.0), Kinematics (0.8/1.0)
  - `learning_dna`: `preferred_level: 4` (Visual), `frustration_tolerance: Low`
- **History:** 3 previous sessions where Level 2 (Mathematical) failed.

## 3. Golden Path (5-Minute Run)

| Time | Action | Visual |
|---|---|---|
| **0:00-0:30** | Introduce Mentra X and the problem. | Deck slide / Architecture Diagram |
| **0:30-1:00** | Show the Foundation. Log in as Aryan. | LMS Dashboard, courses, XP. |
| **1:00-1:45** | Ask: "I don't understand Entropy." | Chat UI. Open the **Developer Panel** side-by-side. |
| **1:45-2:30** | Trace the execution in Dev Panel. | Show Memory Agent fetching DNA. Show Enkrypt scoring live. |
| **2:30-3:15** | Answer the generated micro-quiz correctly. | Show the Twin Mastery score increasing (`0.30 -> 0.35`). |
| **3:15-4:00** | Fast-forward: Run the Weakness Cron Job. | Terminal: `python scheduler/jobs.py --force`. UI updates with alert. |
| **4:00-4:30** | Show the Twin Dashboard. | The 7-State visualization. |
| **4:30-5:00** | Close on Opportunity feed. | Shows a Hackathon match based on Twin skills. |

## 4. Talking Points (What gets high scores)

- **Foundation (0:30):** *"Mentra X isn't just an AI wrapper. We built this on top of a mature LMS with 34 tables, real authentication, and gamification."*
- **The Twin (1:00):** *"Notice Aryan didn't say 'explain it simply'. The system already knows he needs Level 4 Visual Analogies because it remembers his past failures."*
- **Safety (1:45):** *"In high-stakes exams like JEE, a hallucinated formula ruins a student's rank. Our Enkrypt layer mathematically guarantees accuracy before the student ever sees the text."*
- **Verification (2:30):** *"Most AIs just dump text. Mentra X forces comprehension. The Twin mastery score ONLY goes up if he passes this semantic micro-quiz."*
- **Intelligence (3:15):** *"Because we store every interaction in Qdrant, our async agents can run cluster analysis across months of data to find hidden weaknesses before the exam."*

## 5. Expected Judge Questions & Answers

**Q1: How do you prevent hallucinations in Physics/Math?**
*Answer:* "We use Enkrypt AI as a strict middleware gate. The response is scored across 4 vectors (Math, Science, Hallucination, Pedagogy). If the composite score is under 0.90, the agent is forced to regenerate. If it fails twice, we intercept the AI entirely and serve a pre-verified NCERT textbook fallback."

**Q2: Why use Qdrant instead of just standard SQL?**
*Answer:* "The Learning DNA and explanation histories are behavioral and semantic. When the student asks about 'Carnot Cycles', we need to run a cosine similarity search against their past doubts to see what analogies failed for similar concepts. SQL can't do semantic search."

**Q3: What makes this different from ChatGPT?**
*Answer:* "Statefulness and Safety. ChatGPT has session amnesia. Our Digital Twin evolves over months. ChatGPT gives immediate answers; our system forces comprehension verification (quizzes) before moving on. ChatGPT hallucinates; we use a 4-layer validation gate."

**Q4: How did you implement the multi-agent system?**
*Answer:* "We used Mastra to build a Directed Acyclic Graph (DAG). It's not a single prompt. The Memory Agent, Tutor Agent, and Verification Agent execute in a strict pipeline with Pydantic typed contracts."

## 6. Architecture Moat (60-second summary)
If asked to summarize the tech:
"It’s a Flask/MySQL foundation. The AI layer is a Mastra-orchestrated DAG. Memory is handled by 5 Qdrant vector collections acting as the Digital Twin. Safety is guaranteed by Enkrypt AI. It’s event-driven, so AI sessions asynchronously trigger Twin mutations and spaced-repetition cron jobs."

## 7. Fallback Scenarios (If things break)

| Failure | Symptoms | The Pivot (What to do) |
|---|---|---|
| **OpenAI API very slow** | Infinite spinner in chat | Switch to the "Offline Demo Plan" (open the pre-recorded video or load the cached UI state). Say: *"Conference Wi-Fi is spotty, so I'll show you the exact same trace we recorded an hour ago."* |
| **Qdrant Cloud down** | `MEMORY_010` error | Point out the graceful degradation: *"Notice how the system stayed up. We built in a fallback to read the Twin from MySQL JSON if the vector DB is unreachable."* |
| **Enkrypt API fails** | `ENKRYPT_001` | Say: *"Safety first. The API is unreachable, so rather than risk a hallucination, our system defaulted to the textbook fallback."* |

## 8. Demo Environment Checklist
Complete 30 minutes before demo:
- [ ] Ensure `.env` is set to `ENABLE_ALL=true`.
- [ ] Run `pytest backend/tests/e2e/ -v` (Must pass).
- [ ] Reset demo user: `python scripts/seed_demo_user.py aryan`.
- [ ] Open 3 browser tabs: LMS Dashboard, Chat UI, Dev Trace Panel.
- [ ] Keep terminal open and zoomed in for the Cron job execution.
- [ ] Turn off laptop notifications / Slack.
