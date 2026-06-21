# Deployment Guide

## Current Deployment Assumptions

- Flask application served from `app.py`
- SQLite database stored as `portal.db`
- Server-rendered templates with local static assets
- No external AI API dependency required for current feature phases

## Environment Notes

- Install Python dependencies from `requirements.txt`
- Keep write access for `instance/` and `uploads/`
- Preserve SQLite file backups before production updates

## Database Note

This project uses SQLite by default for local and test workflows. MySQL is supported via environment variables for production deployments.

### MySQL Migration Steps

1. Install the driver: `pip install pymysql`
2. Create the database: `mentra_db`
3. Set environment variables:
   - `MENTRA_USE_MYSQL=true`
   - `MENTRA_MYSQL_URL=mysql+pymysql://username:password@localhost/mentra_db`
4. Run the app to create tables (or use your preferred migration tool).


## MySQL Migration & UI Upgrade

- Keep `portal.db` as a backup before any migration.
- Export SQLite data (`sqlite3 portal.db`, then `.mode insert`, `.output mentra_export.sql`, `.dump`).
- Import into MySQL (`USE mentra_db;` then `SOURCE mentra_export.sql;`).
- Verify key tables: `users`, `courses`, `course_modules`, `coding_submissions`, `wallet`, `rewards`.
- UI upgrades include the refreshed color palette, dark/light mode toggle, redesigned learning feed and insights cards, and updated course layouts.


## Hybrid Database Architecture (MySQL + MongoDB)

Mentra uses a production-level hybrid database architecture to separate structured LMS data from flexible AI logs.
- **MySQL (Primary)**: Stores all core structured data including users, courses, domains, and enrollments.
- **MongoDB (Secondary)**: Stores AI interactions, flexible logs, and analytics (e.g., `chat_logs`, `learning_insights`, `project_ideas`, `coding_logs`).

MongoDB integration is safely wrapped. If MongoDB goes offline or fails to connect, core application operations will continue to work securely.

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


## MySQL Verification

- Run `python app.py` and check logs for `MySQL connection successful`.
- Confirm the active database: `Connected to database: mentra_db`.
- Use `/db-check` to return the connected database name.
- In MySQL, run `SHOW TABLES;` and `SELECT COUNT(*) FROM users;` to confirm data is present.

If you see `Unknown database 'mentra_db'`, create the database before starting the app.

## Verification Before Deployment

1. Run the unittest suite.
2. Verify chatbot endpoints respond.
3. Verify student dashboard, AI routes, and uploads work.
4. Confirm no migration files or PostgreSQL configuration have been added.


## Final MySQL Migration Completion

- Create `mentra_db` and confirm it exists.
- Keep SQLite backup at `instance/portal.db`.
- Export SQLite data and import into MySQL using insert-only SQL.
- Validate with `/db-check` and table counts.
- Run `python run_all_tests.py` to ensure stability on MySQL.
## Documentation Refresh (May 20, 2026)

- `/student/referral` now uses a startup-style layout with cleaner sections, better spacing, copy/share actions, and readable reward history.
- Resume Analyzer UI was rebuilt to use space more efficiently with a two-panel workflow and clearer insights blocks.
- Resume Analyzer now auto-loads saved resume text from uploaded files (TXT/PDF/DOCX) when available.
- Resume analysis now powers targeted course recommendations by matching detected/missing skills against published courses while skipping already enrolled courses.
- If a new upload cannot be parsed, the system safely falls back to stored structured resume data instead of breaking the user flow.
