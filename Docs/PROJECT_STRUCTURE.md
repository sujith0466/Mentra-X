# Project Structure

## Root

- `app.py`: Flask app setup, SQLite configuration, blueprint registration, table creation, and chatbot API endpoint wiring
- `models.py`: SQLAlchemy models for LMS, AI, coding, interview, projects, community, and gamification
- `student_routes.py`, `public_routes.py`, `auth_routes.py`, `admin_routes.py`: main LMS route modules
- `ai_routes.py`: AI, career, skill, coding, interview, and project feature blueprints
- `community_routes.py`: community and gamification routes
- `run_all_tests.py`: unified test runner
- `scripts/`: seed scripts for course ecosystem and coding challenges
- `Docs/`: phase guides and system documentation

## Services

### `services/ai/`

- `mentor_service.py`: rule-based mentor knowledge base and structured responses
- `assistant_service.py`: assistant router and multi-agent entry point
- `project_idea_service.py`, `recommendation_service.py`, `career_service.py`: shared AI services used across phases

### `services/ai/learning/`

- study planner
- notes generation
- practice quiz generation
- revision support

### `services/ai/career/`

- resume analysis
- skill gap detection
- portfolio generation

### `services/ai/devtools/`

- coding practice
- debugging help
- codebase explanation
- profile analysis

### `services/ai/ml/`

- recommendation model
- skill prediction model
- learning difficulty model

### `services/ai/skills/`

- skill mapping
- skill graph calculation
- per-student skill progress snapshots

### `services/ai/coding/`

- coding challenge retrieval
- code execution sandbox
- auto-grading
- AI-style code feedback
- coding submission and skill updates

### `services/ai/interview/`

- interview question generation
- interview sessions
- answer feedback and scoring
- recent interview history helpers

### `services/ai/projects/`

- project generation
- project blueprints
- project task creation
- student project progress tracking

### `services/ai/agents/`

- base agent contract
- mentor, learning, debug, career, project, interview, and community agents
- agent-oriented assistant routing support

### `services/community/`

- community posting and answering
- XP awards
- level and badge updates

## Templates

### `templates/student/`

- core LMS pages such as dashboard and courses
- `ai/`: study planner, notes, revision, recommendations, project ideas
- `career/`: resume analyzer, skill gap, portfolio
- `devtools/`: coding practice, debug assistant, codebase explainer
- `skills/`: skill graph
- `coding/`: challenge list, challenge detail, results
- `interview/`: interview dashboard, start page, live session, result page
- `projects/`: project home, generator, detail, progress
- `assignments/`, `quizzes/`: LMS assessment pages

### `templates/community/`

- community home
- question post page
- question detail page

## Static and Uploads

- `static/`: CSS, JS, images, and course/domain assets
- `uploads/`: assignment, resume, and developer-tool upload storage

## Tests

The `tests/` package contains coverage for:

- LMS core
- learning AI
- career AI
- developer AI tools
- ML models
- chatbot assistant
- coding platform
- interview system
- project system
- community system
- multi-agent system
## Documentation Refresh (May 20, 2026)

- `/student/referral` now uses a startup-style layout with cleaner sections, better spacing, copy/share actions, and readable reward history.
- Resume Analyzer UI was rebuilt to use space more efficiently with a two-panel workflow and clearer insights blocks.
- Resume Analyzer now auto-loads saved resume text from uploaded files (TXT/PDF/DOCX) when available.
- Resume analysis now powers targeted course recommendations by matching detected/missing skills against published courses while skipping already enrolled courses.
- If a new upload cannot be parsed, the system safely falls back to stored structured resume data instead of breaking the user flow.
