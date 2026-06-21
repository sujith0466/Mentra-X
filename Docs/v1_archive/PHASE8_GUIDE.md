# Phase 8 Guide

## Overview

Phase 8 added the AI learning experience layer: skill graph tracking, learning feed generation, and adaptive insights on the student dashboard.

## Features Implemented

- skill graph and knowledge map
- learning feed generation
- weak-topic and next-skill insights on the dashboard
- adaptive learning support tied to progress and performance

## Services Used

- `services/ai/skills/skill_mapping.py`
- `services/ai/skills/skill_graph_service.py`
- `services/ai/learning_feed_service.py`
- `services/ai/learning/study_planner_service.py`
- `services/ai/ml/learning_difficulty_model.py`
- `services/ai/ml/skill_prediction_model.py`

## Models Added

- `SkillProgress`

## Routes Added

- `/student/skills`

## Notes

The student dashboard uses Phase 8 outputs to render learning feed items, skill progress, weak topics, and suggested skills.
## Documentation Refresh (May 20, 2026)

- `/student/referral` now uses a startup-style layout with cleaner sections, better spacing, copy/share actions, and readable reward history.
- Resume Analyzer UI was rebuilt to use space more efficiently with a two-panel workflow and clearer insights blocks.
- Resume Analyzer now auto-loads saved resume text from uploaded files (TXT/PDF/DOCX) when available.
- Resume analysis now powers targeted course recommendations by matching detected/missing skills against published courses while skipping already enrolled courses.
- If a new upload cannot be parsed, the system safely falls back to stored structured resume data instead of breaking the user flow.
