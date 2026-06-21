# Phase 2 Guide

## Overview

Phase 2 expanded Mentra from simple AI guidance into learning workflow support, helping students plan, review, and practice more effectively.

## Features Implemented

- AI study planner
- adaptive notes generation for lesson pages
- AI practice quiz generation
- smart revision recommendations
- learning support integrated into course video flow

## Services Used

- `services/ai/learning/study_planner_service.py`
- `services/ai/learning/notes_service.py`
- `services/ai/learning/quiz_generator_service.py`
- `services/ai/learning/revision_service.py`

## Models Added

No new Phase 2-specific models were added. The phase reused `Video`, `Course`, `Quiz`, `QuizQuestion`, `LessonProgress`, and related LMS data.

## Routes Added

- `/student/ai/study-planner`
- `/student/ai/notes/<video_id>`
- `/student/ai/practice-quiz/<video_id>`
- `/student/ai/revision`

## Notes

Phase 2 established the `services/ai/learning/` package, which later phases extend for adaptive learning and personalization.

## Phase-2 Enhancements — AI Learning Intelligence

- Smart Revision now evaluates quiz scores, repeated failures, assignment marks, incomplete lessons, and coding performance.
- Portfolio Builder now includes resume projects, course projects, coding challenges, and starter project fallbacks.
- AI Project Idea Generator now personalizes ideas from resume skills and course history, with difficulty labels.
- AI Learning Insights now combines resume skills, performance signals, and skill gaps for guidance.
- Testing Results: `run_all_tests.py` (40 tests) passed
## Documentation Refresh (May 20, 2026)

- `/student/referral` now uses a startup-style layout with cleaner sections, better spacing, copy/share actions, and readable reward history.
- Resume Analyzer UI was rebuilt to use space more efficiently with a two-panel workflow and clearer insights blocks.
- Resume Analyzer now auto-loads saved resume text from uploaded files (TXT/PDF/DOCX) when available.
- Resume analysis now powers targeted course recommendations by matching detected/missing skills against published courses while skipping already enrolled courses.
- If a new upload cannot be parsed, the system safely falls back to stored structured resume data instead of breaking the user flow.
