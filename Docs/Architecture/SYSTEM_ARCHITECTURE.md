# System Architecture

## Project Overview

Mentra AI Student Platform is a Flask monolith that combines LMS workflows and modular AI services. The system is server-rendered with Jinja templates and uses SQLite for tests and MySQL for production persistence.

## Architecture

Reflecting the actual implementation, the architecture currently includes:

Existing Mentra LMS
↓
Digital Twin Engine
↓
Adaptive Assessment Engine
↓
REST API Facade

**Future Architecture (Phases 4-6):** Mastra and Enkrypt are not yet implemented and are planned for future phases.

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

- **Phase 0:** Architecture Freeze (✅ Complete)
- **Phase 1:** Digital Twin Foundation (✅ Complete)
- **Phase 2:** Adaptive Assessment Engine (✅ Complete)
- **Phase 2.5:** Production Stabilization (✅ Complete)
- **Phase 3:** Qdrant Memory Integration (✅ Complete)
- **Phase 4:** Mastra Learning Agent (Planned)
- **Phase 5:** Adaptive Teaching (Planned)
- **Phase 6:** Enkrypt Safety Layer (Planned)

