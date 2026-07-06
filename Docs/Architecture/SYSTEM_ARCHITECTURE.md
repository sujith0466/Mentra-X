# System Architecture

## Project Overview

Mentra AI Student Platform is a modern enterprise SaaS application combining a high-performance **React 18 + TypeScript + Vite Enterprise SPA** frontend with a backend Flask REST API monolith and modular AI services. The primary frontend is served via an `@app.before_request` SPA catch-all interceptor, while legacy server-side Jinja templates are preserved intact inside `frontend/templates/` and `frontend/static/` as an instant restorable rollback layer.

## Architecture

Client Web Application (`frontend/`)
• React 18 + TypeScript + Vite + Tailwind CSS + Framer Motion
• State Management: Zustand + TanStack Query (React Query)
↓
Flask SPA Interceptor (`@app.before_request`) & REST API Layer (`/api/*`, `/auth/*`, `/student/api/*`, `/admin/api/*`)
↓
Mastra Cognitive Swarm
↓
Enterprise Runtime
↓
Enterprise Services
• Explainability
• Evaluation
• Observability
• Privacy
• Dashboard
↓
Digital Twin Graph
↓
Semantic Memory (Qdrant Swarm)
↓
Assessment Engine (DNA Seeder)
↓
Hybrid Database (MySQL Primary + MongoDB Additive Logs)

## Core Architecture

- Entry point: `app.py`
- SPA Interceptor: Serves React production bundle (`frontend/dist/index.html`) when `MENTRA_FRONTEND_MODE='react'`
- Rollback Layer: Preserves legacy Jinja templates in `frontend/templates/` and `frontend/static/` when `MENTRA_FRONTEND_MODE='legacy'`
- Route layer: dedicated JSON REST API blueprints for auth, public, student, admin, quiz, assignment, AI, career, and developer tools
- Service layer: `services/ai/`, `services/twin/`, `services/assessment/`, and `services/orchestration/`
- Data layer: SQLAlchemy models in `models.py` and MongoDB flexible schema logging

## Data Flow

1. Browser request reaches the Flask server; SPA UI navigation requests are served the compiled React Vite bundle (`dist/index.html`).
2. React client components make asynchronous HTTP JSON requests via TanStack Query and Zustand to REST API endpoints (`/api/*`, `/student/api/*`, etc.).
3. Route controllers validate JWT / HTTP-only session cookies and load user/course context.
4. Route controllers invoke LMS or AI service modules (Mastra swarms, Qdrant memory, Enkrypt safety validators).
5. Service modules interact with MySQL (primary structured storage) and MongoDB (additive AI telemetry).
6. Pure JSON payloads decorated with Enkrypt Layer 6 safety badges and metrics are returned to the React SPA for dynamic client-side rendering.

## Database Configuration

- Engine: MySQL (Primary for structured data including users, courses, enrollments, and digital twins)
- Hybrid setup: MongoDB (Secondary additive storage for AI interactions, flexible logs, and analytics)
- Semantic Memory: Qdrant Vector Database for knowledge embeddings and memory timelines
- No migration framework is active in this project.

## AI Layering & Phases

- **Phase 0:** Foundation (✅ Complete)
- **Phase 1:** Digital Twin (✅ Complete)
- **Phase 2:** Assessment Intelligence (✅ Complete)
- **Phase 3:** Semantic Memory (Qdrant) (✅ Complete)
- **Phase 4:** Mastra Cognitive Swarm (✅ Complete)
- **Phase 5:** Enterprise AI Platform (✅ Complete)
- **Phase 6:** Adaptive Learning Intelligence (✅ Complete & Certified)
- **Phase 7:** Enkrypt Safety Layer 6 Governance (✅ Complete & Certified)
- **Phase 8:** Weakness Intelligence (🔒 Locked & Frozen in Certified Production Baseline)

