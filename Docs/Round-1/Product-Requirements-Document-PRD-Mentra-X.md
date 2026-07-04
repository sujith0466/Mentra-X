# Product Requirements Document (PRD): Mentra X

## 1. Executive Summary
Mentra X is an enterprise-grade, AI-powered Student Digital Twin and Adaptive Learning ecosystem. Unlike traditional AI chatbots, Mentra X utilizes a stateful "Learning DNA" model to provide persistent, personalized education. Built on the Mastra AI orchestration framework, Qdrant vector memory, and Enkrypt AI safety layers, the system evolves with the student, creating a continuous feedback loop that tracks mastery, predicts concept decay, and provides high-stakes exam preparation (JEE, NEET, UPSC, etc.) with 100% pedagogical reliability.

## 2. Problem Statement
Traditional educational platforms and generic AI tutors suffer from "session amnesia"—they do not truly know the student's long-term strengths, weaknesses, or preferred learning styles. Furthermore, AI hallucinations in technical subjects (Math/Science) pose a significant risk for students preparing for competitive exams where accuracy is paramount.

## 3. Goals & Objectives
*   **Persistent Personalization:** Develop a "Student Digital Twin" that serves as the visual and logical centerpiece of the learning experience.
*   **Pedagogical Accuracy:** Implement a mandatory safety gateway to eliminate hallucinations and ensure mathematical/scientific rigor.
*   **Adaptive Orchestration:** Use a multi-agent swarm to handle specialized tasks (Assessment, Tutoring, Weakness Analysis).
*   **Continuous Evolution:** Establish a closed-loop system where every interaction updates the student's Learning DNA and vector memory.
*   **Foundation Integration:** Leverage the existing Mentra LMS (Coding, Resume, XP systems) as a deterministic data foundation.

## 4. Target Users / Stakeholders
*   **Primary Users:** Students preparing for JEE, NEET, UPSC, CAT, and Board Exams.
*   **Stakeholders:** HiDevs × Mastra Hackathon Judges, Mentra Platform Administrators, Educational Content Experts (HITL).

## 5. Functional Requirements

### 5.1 Student Digital Twin (Centerpiece)
*   **State Tracking:** Must maintain real-time states for Academic progress, Knowledge levels, Skill acquisition, and Learning Behavior.
*   **Learning DNA:** A behavioral vector encoding mastery scores, preferred teaching levels, frustration indices, and memory retention curves.
*   **Twin Health Score:** A composite metric representing the student's overall readiness and engagement.

### 5.2 Mastra Cognitive Swarm (Agent Layer)
*   **Assessment Agent:** Conducts adaptive diagnostics calibrated to exam difficulty.
*   **Memory Agent:** Hydrates agent context by performing parallel fetches from Qdrant and the Digital Twin.
*   **Adaptive Tutor Agent:** Generates explanations across 5 levels (Simple, Example-based, Mistake Analysis, Visual Analogy, Exam Coaching).
*   **Verification Agent:** Generates post-explanation micro-quizzes and triggers Digital Twin mutations based on performance.
*   **Weakness Intel Agent (CRON):** Performs background semantic clustering of failure patterns and concept decay analysis.
*   **Insight Agent (Weekly):** Synthesizes long-term progress reports and revision curricula.
*   **Opportunity Intelligence Agent:** Recommends internships, scholarships, and hackathons based on the Twin's career state.

### 5.3 Adaptive Learning Loop
*   **Flow:** Student → Assessment → Twin/Memory Retrieval → Mastra Swarm Reasoning → Enkrypt Validation → Student Response → Twin/Memory Update.
*   **Persistence:** Every response must trigger an asynchronous update to the Qdrant vector store and the Student Digital Twin JSON state.

## 6. Non-Functional Requirements
*   **Reliability:** Mandatory fallback to verified textbook corpora (e.g., NCERT) if AI confidence is low.
*   **Accuracy:** Minimum confidence score of 0.90 for automated approval.
*   **Performance:** Low-latency WebSocket communication for the Cognitive Chat UI.
*   **Scalability:** HNSW indexing in Qdrant to support high-dimensional (1536-dim) student embeddings.

## 7. System Architecture Overview
The system follows a 6-layer hierarchical structure:
1.  **Presentation Layer:** React-based dashboards and chat interfaces.
2.  **API & Routing Layer:** Flask Gateway handling Auth and Session management.
3.  **Agent Swarm Layer:** Mastra DAG Orchestrator coordinating 7 specialized agents.
4.  **Digital Twin Layer:** The central state repository for student profiles.
5.  **Memory & Safety Layer:** Qdrant vector collections and Enkrypt safety pipelines.
6.  **Foundation Layer:** Existing MySQL database and Mentra LMS services.

## 8. Tech Stack
*   **Orchestration:** Mastra.AI (DAG Orchestrator)
*   **Vector Database:** Qdrant (HNSW Index, Cosine Similarity)
*   **Safety:** Enkrypt AI (Safety Middleware)
*   **Backend:** Flask, Python, PyJWT
*   **Frontend:** React, Tailwind CSS, Video.js, WebSockets
*   **Database:** MySQL (Relational Foundation)
*   **State:** JSON-based Persistent Memory

## 9. Data Requirements
*   **Qdrant Collections:** `learning_dna`, `past_doubts`, `explanation_history`, `session_logs`, `weak_concepts`, `assessment_results`.
*   **MySQL Tables:** Users, Courses, XP Ledger, Skill Graph, Portfolios, deterministic Ground Truth.
*   **Digital Twin Schema:** Must include Academic State, Knowledge State, Skill State, and Twin Health Score.

## 10. API Specifications
*   **Flask Gateway:**
    *   `POST /auth/login`: JWT-based authentication.
    *   `POST /ai/chat`: WebSocket/HTTP routing to Mastra DAG.
    *   `GET /twin/status`: Retrieves current Digital Twin health and DNA.
    *   `GET /analytics/weekly`: Fetches Insight Agent reports.

## 11. Security Requirements
*   **Authentication:** Mandatory JWT (PyJWT) for all API requests.
*   **Safety Gateway:** Mandatory Enkrypt validation for every LLM-generated response.
*   **Rate Limiting:** Implemented at the Flask Gateway to prevent swarm abuse.
*   **Data Protection:** Isolation of student session logs and PII within the MySQL foundation.

## 12. Deployment & Infrastructure
*   **Containerization:** Python-based microservices.
*   **Orchestration:** Mastra DAG for complex multi-agent workflows.
*   **Memory:** Persistent Qdrant instance for long-term RAG.
*   **Foundation:** Integration with existing Mentra infrastructure (LMS/Coding Platform).

## 13. Success Metrics
*   **Accuracy Rate:** Percentage of responses passing Enkrypt validation (>95% target).
*   **Shortlist Probability:** Alignment with HiDevs × Mastra Hackathon "Top-30" quality standards.
*   **Twin Evolution:** Measurable delta in "Mastery Scores" stored in Learning DNA over 5+ sessions.
*   **Regeneration Index:** Reduction in the number of required regeneration loops over time.

## 14. Timeline & Milestones
*   **Phase 1:** Foundation Integration & Digital Twin Schema definition.
*   **Phase 2:** Mastra DAG Orchestrator setup with Assessment and Memory agents.
*   **Phase 3:** Enkrypt Safety Gateway integration and Regeneration Loop logic.
*   **Phase 4:** Background Agents (Weakness Intel/Insight) and Opportunity Intelligence.
*   **Phase 5:** UI/UX refinement and Hackathon submission packaging.

## 15. Open Questions & Risks
*   **Latency:** The impact of multi-agent fanning and mandatory safety checks on real-time chat response times.
*   **Concept Decay Accuracy:** Validating the mathematical formula (`mastery_score * 0.85`) against real-world student retention data.
*   **HITL Scaling:** Managing the expert review queue if a high volume of responses fall into the 0.75–0.89 confidence range.