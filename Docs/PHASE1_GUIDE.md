# Phase 1 Guide

## Overview

Phase 1 introduced the first AI layer in Mentra: a mentor-style chatbot experience and foundational student guidance utilities.

## Features Implemented

- rule-based AI mentor chatbot
- project idea suggestions
- AI-assisted course recommendations
- career roadmap generation
- chatbot integration for student-facing help requests

## Services Used

- `services/ai/mentor_service.py`
- `services/ai/project_idea_service.py`
- `services/ai/recommendation_service.py`
- `services/ai/career_service.py`
- `chatbot_service.py`
- `chatbot_service_hardcoded.py`

## Models Added

No new database models were introduced in Phase 1. The phase reused existing LMS models such as `User`, `Course`, `Domain`, and `Enrollment`.

## Routes Added

- `/student/ai/project-ideas`
- `/student/ai/recommendations`
- `/student/ai/career-roadmap`
- `/api/chatbot/ask`

## Notes

Phase 1 established the AI service pattern later reused by all later phases.

## Phase-1 Enhancements — Resume Intelligence Upgrade

- Resume Analyzer now supports PDF/DOCX/TXT extraction with structured skills, projects, education, and experience storage.
- Skill Gap Detector compares resume skills with enrolled and completed course skills, and surfaces missing plus suggested skills.
- Resume-based course recommendations prioritize missing skills while avoiding completed courses.
- Career roadmap now renders phased guidance (Core Skills, Intermediate Skills, Projects, Interview Preparation) and adapts to resume skills, completed courses, and coding performance.
- Testing Results: `run_all_tests.py` (40 tests) passed
## Documentation Refresh (May 20, 2026)

- `/student/referral` now uses a startup-style layout with cleaner sections, better spacing, copy/share actions, and readable reward history.
- Resume Analyzer UI was rebuilt to use space more efficiently with a two-panel workflow and clearer insights blocks.
- Resume Analyzer now auto-loads saved resume text from uploaded files (TXT/PDF/DOCX) when available.
- Resume analysis now powers targeted course recommendations by matching detected/missing skills against published courses while skipping already enrolled courses.
- If a new upload cannot be parsed, the system safely falls back to stored structured resume data instead of breaking the user flow.
