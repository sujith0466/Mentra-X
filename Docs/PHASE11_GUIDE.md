# Phase 11 Guide

## Overview

Phase 11 introduced the AI project builder so students can generate guided projects, follow a task roadmap, and convert finished work into portfolio-ready experience.

## Features Implemented

- project idea generation by domain and difficulty
- project blueprint generation
- automatic project task creation
- student project progress tracking
- project completion integration with portfolio and skill progress

## Services Used

- `services/ai/projects/project_generator_service.py`
- `services/ai/projects/project_blueprint_service.py`
- `services/ai/projects/project_progress_service.py`
- `services/ai/career/portfolio_service.py`

## Models Added

- `ProjectIdea`
- `StudentProject`
- `ProjectTask`

## Routes Added

- `/student/projects`
- `/student/projects/generate`
- `/student/projects/<id>`
- `/student/projects/start/<id>`
- `/student/projects/progress/<id>`

## Notes

Completed projects contribute to the portfolio builder and award skill progress and gamification XP.
## Documentation Refresh (May 20, 2026)

- `/student/referral` now uses a startup-style layout with cleaner sections, better spacing, copy/share actions, and readable reward history.
- Resume Analyzer UI was rebuilt to use space more efficiently with a two-panel workflow and clearer insights blocks.
- Resume Analyzer now auto-loads saved resume text from uploaded files (TXT/PDF/DOCX) when available.
- Resume analysis now powers targeted course recommendations by matching detected/missing skills against published courses while skipping already enrolled courses.
- If a new upload cannot be parsed, the system safely falls back to stored structured resume data instead of breaking the user flow.
