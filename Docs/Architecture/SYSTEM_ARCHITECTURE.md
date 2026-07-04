# System Architecture

## Project Overview

Mentra AI Student Platform is a Flask monolith that combines LMS workflows and modular AI services. The system is server-rendered with Jinja templates and uses SQLite for tests and MySQL for production persistence.

## Architecture

Frontend
↓
API Layer
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
Digital Twin
↓
Semantic Memory
↓
Assessment Engine
↓
Database

## Core Architecture

- Entry point: `app.py`
- Route layer: root Flask blueprints for auth, public, student, admin, quiz, assignment, AI, career, and developer tools
- Service layer: `services/ai/`, `services/twin/`, and `services/assessment/`
- Data layer: SQLAlchemy models in `models.py`
- Presentation layer: templates under `templates/` and assets under `static/`

## Data Flow

1. Browser request reaches a Flask blueprint route.
2. Route validates access and loads user or course context.
3. Route calls LMS or AI service modules.
4. Service modules use SQLAlchemy models and MySQL data.
5. Result is returned through Jinja templates or JSON responses.

## Database Configuration

- Engine: MySQL (Primary for structured data)
- Hybrid setup: MongoDB (Secondary for AI logs and analytics)
- No migration framework is active in this project.

## AI Layering & Phases

- **Phase 0:** Foundation (✅ Complete)
- **Phase 1:** Digital Twin (✅ Complete)
- **Phase 2:** Assessment Intelligence (✅ Complete)
- **Phase 3:** Semantic Memory (Qdrant) (✅ Complete)
- **Phase 4:** Mastra Cognitive Swarm (✅ Complete)
- **Phase 5:** Enterprise AI Platform (✅ Complete)
- **Phase 6:** Adaptive Learning Intelligence (Planned)
- **Phase 7:** Enkrypt Safety Layer (Planned)

