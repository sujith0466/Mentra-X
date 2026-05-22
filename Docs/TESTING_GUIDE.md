# Testing Guide

## Overview

The project includes a unittest-based verification suite under `tests/`.

## Test Modules

- `test_lms_core.py`: auth, browsing, enrollment, videos, quiz submission, assignment submission, progress, certificate flow
- `test_learning_ai.py`: Phase 1 and Phase 2 AI guidance and learning tools
- `test_career_ai.py`: Phase 3 career tools
- `test_devtools_ai.py`: Phase 4 developer intelligence tools
- `test_ml_models.py`: Phase 5 ML personalization and fallback behavior
- `test_chatbot_assistant.py`: Phase 6 assistant routing and chatbot compatibility

## Running the Full Suite

```powershell
.\.venv\Scripts\python.exe .\run_all_tests.py
```

## Running Discovery Directly

```powershell
.\.venv\Scripts\python.exe -m unittest discover tests -v
```

## Database Policy

This project uses SQLite as its database. No database migration to PostgreSQL is planned at this stage.

Tests are designed to keep using SQLite and clean up their temporary records after execution.
## Documentation Refresh (May 20, 2026)

- `/student/referral` now uses a startup-style layout with cleaner sections, better spacing, copy/share actions, and readable reward history.
- Resume Analyzer UI was rebuilt to use space more efficiently with a two-panel workflow and clearer insights blocks.
- Resume Analyzer now auto-loads saved resume text from uploaded files (TXT/PDF/DOCX) when available.
- Resume analysis now powers targeted course recommendations by matching detected/missing skills against published courses while skipping already enrolled courses.
- If a new upload cannot be parsed, the system safely falls back to stored structured resume data instead of breaking the user flow.
