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
