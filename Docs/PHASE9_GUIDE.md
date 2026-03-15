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
