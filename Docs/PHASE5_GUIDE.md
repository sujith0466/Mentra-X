# Phase 5 Guide

## Overview

Phase 5 added personalization logic to Mentra using ML-style recommendation and prediction services with safe fallback behavior.

## Features Implemented

- personalized course recommendation model
- next-skill prediction model
- learning difficulty detection model
- adaptive study planning inputs

## Services Used

- `services/ai/ml/recommendation_model.py`
- `services/ai/ml/skill_prediction_model.py`
- `services/ai/ml/learning_difficulty_model.py`
- `services/ai/recommendation_service.py`
- `services/ai/learning/study_planner_service.py`

## Models Added

No new database tables were introduced. Phase 5 operates on existing learning and progress data.

## Routes Added

No new standalone routes were required. Phase 5 powers recommendation, dashboard, assistant, and adaptive-learning routes introduced earlier and later.

## Notes

Phase 5 is the personalization layer behind recommendations, weak-topic detection, and next-skill suggestions across the platform.
