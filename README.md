# Mentra X
**Built By: Sujith Kumar AI**

**HiDevs × Mastra Hackathon 2026**
- **Project:** Mentra X
- **Track:** Student Doubt-Solving & Learning Agent
- **Round-1 Deliverables:** `Docs/Round-1/`

Mentra X is an AI-powered student learning ecosystem built with Flask and SQLite. It combines a full LMS with layered AI systems for learning support, career growth, coding practice, mock interviews, project building, community engagement, and multi-agent assistance.

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

## Current Architecture

Layer 1
Core LMS

Layer 2
Digital Twin

Layer 3
Semantic Memory

Layer 4
Mastra Cognitive Swarm

Layer 5
Enterprise AI Platform

Future

Layer 6
Adaptive Learning Intelligence

## Architecture Overview

Mentra follows a modular Flask architecture:

- `app.py` configures the application, SQLite database, and blueprints
- route modules define LMS, AI, and community user flows
- `services/ai/` contains AI-focused feature modules grouped by domain
- `services/community/` contains community and gamification logic
- `models.py` stores all SQLAlchemy models
- Jinja templates render student, admin, public, coding, interview, project, and community pages

## Phase Development Timeline

### Completed
- **Phase 0:** Foundation
- **Phase 1:** Digital Twin
- **Phase 2:** Assessment Intelligence
- **Phase 3:** Semantic Memory (Qdrant)
- **Phase 4:** Mastra Cognitive Swarm
- **Phase 5:** Enterprise AI Platform

### Upcoming

**Phase 6 — Adaptive Learning Intelligence**
- TutorDecisionEngine
- LearningStyleDetector
- DynamicPromptBuilder
- AdaptiveDifficultyController
- PersonalizationEngine
- Opportunity Intelligence
- Predictive Intervention

**Future**
- **Phase 7:** Enkrypt Safety Layer

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
- pip

### Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Running the Project

Start the Flask app from the workspace root:

```powershell
python run.py

```

The application uses SQLite and stores data in `portal.db` under the instance directory.

## Running Tests

Run the complete test suite with:

```powershell
python .\run_all_tests.py
```

You can also run direct unittest discovery:

```powershell
python -m unittest discover tests -v
```

## Project Structure

- `frontend/`: contains all `static/` assets and Jinja `templates/`
- `backend/`: contains `app.py`, models, routes, tests, and AI services
- `Docs/`: phase guides, system architecture, and Round-1 Hackathon deliverables

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
