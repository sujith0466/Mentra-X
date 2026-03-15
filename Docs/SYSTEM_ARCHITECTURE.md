# System Architecture

## Project Overview

Mentra AI Student Platform is a Flask monolith that combines LMS workflows and modular AI services. The system is server-rendered with Jinja templates and uses SQLite for persistence.

## Core Architecture

- Entry point: `app.py`
- Route layer: root Flask blueprints for auth, public, student, admin, quiz, assignment, AI, career, and developer tools
- Service layer: `services/ai/` plus utility modules for learning and audit logic
- Data layer: SQLAlchemy models in `models.py`
- Presentation layer: templates under `templates/` and assets under `static/`

## Data Flow

1. Browser request reaches a Flask blueprint route.
2. Route validates access and loads user or course context.
3. Route calls LMS or AI service modules.
4. Service modules use SQLAlchemy models and SQLite data.
5. Result is returned through Jinja templates or JSON responses.

## Database Configuration

- Engine: SQLite
- Database file: `instance/portal.db`
- SQLAlchemy URI: `sqlite:///portal.db`
- No migration framework is active in this project.

This project uses SQLite as its database. No database migration to PostgreSQL is planned at this stage.

## AI Layering

- Phase 1: guidance and discovery services
- Phase 2: learning assistance services
- Phase 3: career services
- Phase 4: developer intelligence tools
- Phase 5: ML personalization services
- Phase 6: AI assistant intent router
