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
