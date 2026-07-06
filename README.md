# Mentra X
**Built By: Sujith Kumar AI**

**HiDevs × Mastra Hackathon 2026**
- **Project:** Mentra X
- **Track:** Student Doubt-Solving & Learning Agent
- **Round-1 Deliverables:** `Docs/Round-1/`

Mentra X is an AI-powered enterprise student learning ecosystem built with a React 18 + TypeScript + Vite Single Page Application (SPA) frontend, backed by a Flask REST API monolith and hybrid database persistence (MySQL primary + MongoDB additive logs). It combines a full LMS with layered cognitive AI swarms for learning support, career growth, coding practice, mock interviews, project building, community engagement, and Enkrypt Layer 6 safety governance.

## Project Overview

Mentra is designed as a single platform where students can:

- discover and enroll in courses
- learn through videos, quizzes, assignments, and project work
- receive AI-assisted study guidance
- practice coding and debugging
- prepare for interviews
- build portfolio-ready projects
- engage with a community and earn XP
- interact with specialized AI agents for different needs

## Key Features

- LMS core with authentication, enrollment, progress tracking, referrals, and certificates
- AI mentor chatbot and assistant router
- study planner, revision support, lesson notes, and AI practice quizzes
- resume analysis, skill gap detection, and portfolio generation
- debugging help and codebase explanation tools
- ML-style personalization for recommendations and skill prediction
- skill graph and AI learning feed
- coding sandbox with automatic grading and AI feedback
- mock interviews with scoring and feedback
- AI project builder with progress tracking
- community, badges, XP, and levels
- multi-agent AI system with learning, debug, career, project, interview, and community specialists

## Phase-1 Enhancements - Resume Intelligence Upgrade

- Resume Analyzer: stable PDF/DOCX/TXT parsing with structured extraction saved to `UserResume`
- Skill Gap Detector: compares resume skills, enrolled course skills, completed course skills, and activity signals
- Resume-Based Course Recommendations: prioritize missing skills, skip completed courses, fallback to popular courses when resume data is missing
- AI Career Roadmap: phased roadmap (Core Skills, Intermediate Skills, Projects, Interview Prep) using resume skills, course completion, and coding performance
- Testing Results: `run_all_tests.py` (40 tests) passed

## Phase-2 Enhancements - AI Learning Intelligence

- Smart Revision: combines quiz scores, repeated misses, assignment performance, incomplete lessons, and coding results with safe fallbacks
- Portfolio Builder: includes resume skills, completed courses, projects, and coding challenge solutions with starter project fallbacks
- AI Project Idea Generator: personalized ideas based on resume skills, course history, and learning focus, with difficulty labels
- AI Learning Insights: improved weak-topic detection and skill/course guidance using resume + performance signals
- Testing Results: `run_all_tests.py` (40 tests) passed

## Phase-3 Enhancements - Developer Platform Upgrade

- Coding Practice Platform: language selection, run/submit actions, and clearer result panels with sandboxed execution
- Debugging Assistant: accepts error text, stack trace, and code snippets for structured explanations and fixes
- Codebase Explainer: supports project structure plus code snippets with purpose, logic flow, and improvement suggestions
- Developer Tools UI: refreshed cards, code blocks, output panels, and spacing across coding, debugging, and explainer pages
- Testing Results: `run_all_tests.py` (40 tests) passed

## Phase-4 Enhancements - Platform UX & System Improvements

- AI Learning Feed UI: card layout with tags, action buttons, and safe empty-state messaging
- Edit Profile: prefilled profile editor with validation, confirmation prompt, and persistent profile metadata
- Wallet and Rewards: verified wallet balance + reward history rendering with friendly fallbacks
- Referral System: new /ref/<code> flow with session tracking, bonus protection, and self-referral checks
- Testing Results: `run_all_tests.py` (40 tests) passed

## MySQL Migration & UI Upgrade

- Global UI theme refresh with modern purple/gold palette and improved card spacing
- Dark mode / light mode toggle with localStorage persistence
- Navbar updates with Sign In + Register buttons
- Learning feed and learning insights UI redesign with card layouts and indicators
- MySQL configuration support via `MENTRA_USE_MYSQL` and `MENTRA_MYSQL_URL` (SQLite remains default for tests)
- Data migration guide: export SQLite data, import into MySQL, and verify tables

### MySQL Migration Steps

1. Install the driver: `pip install pymysql`
2. Create the database: `mentra_db`
3. Set environment variables:
   - `MENTRA_USE_MYSQL=true`
   - `MENTRA_MYSQL_URL=mysql+pymysql://username:password@localhost/mentra_db`
4. Run the app once to create tables.
5. Export SQLite data using `sqlite3 portal.db`, then `.mode insert`, `.output mentra_export.sql`, `.dump`.
6. Import into MySQL with `USE mentra_db;` then `SOURCE mentra_export.sql;`.

### MySQL Migration Steps


## Hybrid Database Architecture (MySQL + MongoDB)

Mentra uses a production-level hybrid database architecture to separate structured LMS data from flexible AI logs.
- **MySQL (Primary)**: Stores all core structured data including users, courses, domains, and enrollments.
- **MongoDB (Secondary)**: Stores AI interactions, flexible logs, and analytics (e.g., `chat_logs`, `learning_insights`, `project_ideas`, `coding_logs`).

MongoDB integration is strictly additive. If MongoDB goes offline or fails to connect, the application's core functionality will continue to work seamlessly.

## Environment Configuration (.env)

Create a `.env` file in the project root with:

- `MENTRA_USE_MYSQL=true`
- `MENTRA_MYSQL_HOST=localhost`
- `MENTRA_MYSQL_PORT=3306`
- `MENTRA_MYSQL_DB=mentra_db`
- `MENTRA_MYSQL_USER=root`
- `MENTRA_MYSQL_PASSWORD=yourpassword`
- `MENTRA_USE_MONGO=true`
- `MENTRA_MONGO_URI=mongodb://localhost:27017`
- `MENTRA_MONGO_DB=mentra_ai`
- `SECRET_KEY=mentra-secret-key`
- `FLASK_ENV=development`

If `.env` is missing, Mentra falls back to SQLite and default-safe settings.

## Current Enterprise Architecture

Layer 1: Core LMS (Auth, Courses, Video Player, RBAC)
Layer 2: Digital Twin Graph (Cognitive Student Knowledge State)
Layer 3: Semantic Memory (Qdrant Vector Database Swarm)
Layer 4: Mastra Cognitive Swarm (Specialized AI Agents)
Layer 5: Enterprise AI Platform (Explainability, Telemetry, Observability)
Layer 6: Adaptive Learning Intelligence (TutorDecisionEngine, Opportunity Intelligence)
Layer 7: Enkrypt Safety Layer 6 Governance (Real-Time Safety Verification & Audit)
Layer 8: Weakness Intelligence (🔒 Locked & Frozen in Certified Production Baseline)

## Architecture Overview

Mentra follows a decoupled client-server enterprise architecture:

- `frontend/` houses the production React 18 + TypeScript + Vite SPA, styled with Tailwind CSS and Framer Motion, utilizing Zustand and TanStack Query for state management.
- `app.py` configures the backend WSGI server, SPA catch-all interceptor (`@app.before_request`), database sessions, and REST API blueprints.
- Route modules under `backend/routes/` define dedicated JSON REST APIs (`/api/*`, `/auth/*`, `/student/api/*`, `/admin/api/*`).
- `backend/services/` contains modular AI swarms (`services/ai/`), Digital Twin engines (`services/twin/`), Assessment seeders (`services/assessment/`), and Orchestration loops.
- `backend/models.py` stores SQLAlchemy models for MySQL, while MongoDB handles additive AI telemetry logging.
- Rollback Layer: Legacy Jinja templates and static assets are preserved inside `frontend/templates/` and `frontend/static/`. Setting `MENTRA_FRONTEND_MODE='legacy'` restores instant server-side rendering without code deploys.

## Phase Development Timeline

### Certified & Completed
- **Phase 0:** Foundation (✅ Complete)
- **Phase 1:** Digital Twin (✅ Complete)
- **Phase 2:** Assessment Intelligence (✅ Complete)
- **Phase 3:** Semantic Memory (Qdrant) (✅ Complete)
- **Phase 4:** Mastra Cognitive Swarm (✅ Complete)
- **Phase 5:** Enterprise AI Platform (✅ Complete)
- **Phase 6:** Adaptive Learning Intelligence (✅ Complete & Certified)
- **Phase 7:** Enkrypt Safety Layer 6 Governance (✅ Complete & Certified)
- **Phase 9:** Production Readiness & React Cutover (✅ Complete & Certified)

### Locked Baseline
- **Phase 8:** Weakness Intelligence (🔒 Locked pending explicit executive authorization)

## System Modules

### LMS Core

- authentication and authorization
- course catalog and enrollment
- course videos, quizzes, assignments, certificates
- admin and student dashboards

### AI Learning Stack

- mentor services
- learning planner, notes, revision, quizzes
- recommendation and prediction models
- skill graph and learning feed

### Practice and Career Stack

- coding sandbox
- interview system
- project builder
- career tools and portfolio builder

### Community Stack

- discussion posting and answering
- XP, levels, and badges
- dashboard gamification widgets

### Multi-Agent Stack

- mentor agent
- learning agent
- debug agent
- career agent
- project agent
- interview agent
- community agent

## Installation Guide

### Requirements

- Python 3.11+ or compatible recent Python version
- Node.js 18+ and npm
- MySQL 8.0+ and MongoDB 6.0+ (optional for local dev; SQLite fallback supported)

### Install Dependencies

```powershell
# 1. Install Backend Dependencies
python -m pip install -r requirements.txt

# 2. Install Frontend SPA Dependencies
cd frontend
npm install
```

## Running the Project

### Production Mode (Serving React SPA via Flask Interceptor)
```powershell
# Build the production React bundle
cd frontend
npm run build
cd ..

# Start Flask WSGI server (defaults to MENTRA_FRONTEND_MODE="react")
python run.py
```
* Access SPA Application: `http://localhost:5000/`
* Access REST API: `http://localhost:5000/api/v1/...`

### Local Development Mode (Vite Dev Server + Flask API)
```powershell
# Terminal 1: Start Flask REST API Backend on port 5000
python run.py

# Terminal 2: Start Vite Dev Server on port 5173 (proxies API requests to 5000)
cd frontend
npm run dev
```

## Running Tests

Run the enterprise regression test suite (196 tests) with:

```powershell
python -m pytest
```

Run frontend unit and component tests:

```powershell
cd frontend
npx vitest run
```

## Project Structure

- `frontend/`: contains the modern React 18 + TS + Vite SPA (`src/`, `dist/`), alongside restorable legacy assets (`static/`, `templates/`)
- `backend/`: contains `app.py`, models, REST API controllers, regression tests (`tests/`), and modular AI/twin/assessment services
- `Docs/`: architecture guides, engineering reports, phase certifications, and baseline freeze documents

## Startup Catalog Seeding

Use this command to clean QA/test noise, remove duplicate catalog entries, and seed a full startup-style course catalog:

`python scripts/seed_startup_catalog.py`

What it does:
- removes noisy sample/test catalog rows (for example, `QA Domain ...`, `QA Course ...`)
- de-duplicates domains/courses/modules/syllabus/videos/quizzes/assignments
- seeds full course data with modules, syllabus topics, lesson videos, quizzes, quiz questions, and assignments

Guardrails now applied at model level:
- random/test-like names are blocked
- duplicate titles are blocked within the same catalog scope (domain or course)

## Future Improvements

- add background jobs for heavier AI workflows and grading tasks
- add pagination and caching for dashboard-heavy data views
- expand analytics for learning outcomes and community engagement
- add richer code-editor UX for coding and interview practice
- extend multi-agent collaboration between agents for compound student requests

## Database Note

Mentra defaults to SQLite for local and test runs. MySQL is supported via environment variables, with SQLite kept as a backup.


## MySQL Verification

To verify MySQL is active when running `python app.py`:

- Confirm startup logs show `MENTRA_USE_MYSQL = true` and a MySQL URI.
- Look for `MySQL connection successful` and `Connected to database: mentra_db`.
- Visit `/db-check` to confirm JSON response includes `{"database": "mentra_db"}`.
- Inspect tables via MySQL: `SHOW TABLES;` and validate rows with `SELECT COUNT(*) FROM users;`.

If you see `Unknown database 'mentra_db'`, create the database in MySQL before running the app.

## Final MySQL Migration Completion

- MySQL database created: `mentra_db`.
- `.env` provides MySQL credentials; SQLite (`instance/portal.db`) remains as fallback.
- SQLite data exported and imported into MySQL using insert-only SQL.
- Verification steps:
  - Run `python app.py` and confirm `MySQL connection successful` and `Connected to database: mentra_db`.
  - Call `/db-check` to confirm active database.
  - Check table counts (e.g., `SELECT COUNT(*) FROM users;`).
- Tests executed with MySQL enabled: `python run_all_tests.py`.
## Documentation Refresh (May 20, 2026)

- `/student/referral` now uses a startup-style layout with cleaner sections, better spacing, copy/share actions, and readable reward history.
- Resume Analyzer UI was rebuilt to use space more efficiently with a two-panel workflow and clearer insights blocks.
- Resume Analyzer now auto-loads saved resume text from uploaded files (TXT/PDF/DOCX) when available.
- Resume analysis now powers targeted course recommendations by matching detected/missing skills against published courses while skipping already enrolled courses.
- If a new upload cannot be parsed, the system safely falls back to stored structured resume data instead of breaking the user flow.
