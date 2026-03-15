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

This project uses SQLite as its database. No database migration to PostgreSQL is planned at this stage.

## Verification Before Deployment

1. Run the unittest suite.
2. Verify chatbot endpoints respond.
3. Verify student dashboard, AI routes, and uploads work.
4. Confirm no migration files or PostgreSQL configuration have been added.
