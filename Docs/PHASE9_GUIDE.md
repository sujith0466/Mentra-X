# Phase 9 Guide

## Overview

Phase 9 introduced the coding sandbox and challenge platform so students can solve programming problems directly inside Mentra.

## Features Implemented

- coding challenge listing and filtering
- coding challenge detail page with starter code and test cases
- Python code execution service
- automatic grading against test cases
- AI-style code feedback
- coding submission storage
- skill progress updates from solved challenges

## Services Used

- `services/ai/coding/coding_challenge_service.py`
- `services/ai/coding/code_execution_service.py`
- `services/ai/coding/code_feedback_service.py`
- `scripts/seed_coding_challenges.py`

## Models Added

- `CodingChallenge`
- `CodingSubmission`

## Routes Added

- `/student/coding/challenges`
- `/student/coding/challenge/<id>`
- `/student/coding/submit/<id>`
- `/student/coding/results/<submission_id>`

## Notes

Coding challenge completions integrate with `SkillProgress`, the learning feed, and the assistant system.
## Documentation Refresh (May 20, 2026)

- `/student/referral` now uses a startup-style layout with cleaner sections, better spacing, copy/share actions, and readable reward history.
- Resume Analyzer UI was rebuilt to use space more efficiently with a two-panel workflow and clearer insights blocks.
- Resume Analyzer now auto-loads saved resume text from uploaded files (TXT/PDF/DOCX) when available.
- Resume analysis now powers targeted course recommendations by matching detected/missing skills against published courses while skipping already enrolled courses.
- If a new upload cannot be parsed, the system safely falls back to stored structured resume data instead of breaking the user flow.
