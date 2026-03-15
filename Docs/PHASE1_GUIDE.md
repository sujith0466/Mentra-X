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
