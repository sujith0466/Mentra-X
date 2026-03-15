# Phase 3 Guide

## Overview

Phase 3 focused on career readiness by adding resume feedback, skill-gap analysis, and portfolio generation for students.

## Features Implemented

- resume analyzer
- skill gap detector
- portfolio builder
- AI career tools section on the student dashboard

## Services Used

- `services/ai/career/resume_service.py`
- `services/ai/career/skill_gap_service.py`
- `services/ai/career/portfolio_service.py`
- `services/ai/career_service.py`

## Models Added

No new Phase 3-specific models were added. The services compose results from existing learning data and later include completed student projects.

## Routes Added

- `/student/career/resume-analyzer`
- `/student/career/skill-gap`
- `/student/career/portfolio`

## Notes

The portfolio builder was later extended in Phase 11 so completed projects can appear in student portfolios automatically.
