# Mentra AI Student Platform

Mentra is an AI-powered student learning ecosystem built with Flask and SQLite. It combines a full LMS with layered AI systems for learning support, career growth, coding practice, mock interviews, project building, community engagement, and multi-agent assistance.

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

## Architecture Overview

Mentra follows a modular Flask architecture:

- `app.py` configures the application, SQLite database, and blueprints
- route modules define LMS, AI, and community user flows
- `services/ai/` contains AI-focused feature modules grouped by domain
- `services/community/` contains community and gamification logic
- `models.py` stores all SQLAlchemy models
- Jinja templates render student, admin, public, coding, interview, project, and community pages

## Phase Development Timeline

- Phase 1: AI Mentor Chatbot
- Phase 2: Learning Intelligence
- Phase 3: Career Tools
- Phase 4: Developer Tools
- Phase 5: ML Personalization
- Phase 6: AI Assistant Router
- Phase 7: Course Ecosystem Expansion
- Phase 8: AI Learning Experience
- Phase 9: Coding Sandbox
- Phase 10: AI Interview Preparation
- Phase 11: AI Project Builder
- Phase 12: Community + Gamification
- Phase 13: Multi-Agent AI System

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
python .\app.py
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

- `app.py`: application setup and blueprint registration
- `models.py`: SQLAlchemy models
- `services/ai/`: AI service modules grouped by feature area
- `services/community/`: community and gamification services
- `templates/`: public, auth, admin, student, coding, interview, project, and community pages
- `scripts/`: data seed and setup helpers
- `Docs/`: phase guides and architecture documentation
- `tests/`: automated test coverage for all major systems

## Future Improvements

- add background jobs for heavier AI workflows and grading tasks
- add pagination and caching for dashboard-heavy data views
- expand analytics for learning outcomes and community engagement
- add richer code-editor UX for coding and interview practice
- extend multi-agent collaboration between agents for compound student requests

## Database Note

Mentra uses SQLite. The current project keeps SQLite unchanged and does not require PostgreSQL.
