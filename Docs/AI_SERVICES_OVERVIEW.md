# AI Services Overview

## Service Hierarchy

- `services/ai/mentor_service.py`
  - Shared rule-based mentor knowledge base
- `services/ai/assistant_service.py`
  - Intent detection and module routing
- `services/ai/project_idea_service.py`
  - Domain-based project idea generation
- `services/ai/recommendation_service.py`
  - Backward-compatible recommendation wrapper with ML-first fallback handling
- `services/ai/career_service.py`
  - Career roadmap generation

## Learning Intelligence

- `services/ai/learning/study_planner_service.py`
- `services/ai/learning/notes_service.py`
- `services/ai/learning/revision_service.py`
- `services/ai/learning/quiz_generator_service.py`

## Career Intelligence

- `services/ai/career/resume_service.py`
- `services/ai/career/skill_gap_service.py`
- `services/ai/career/portfolio_service.py`

## Developer Intelligence

- `services/ai/devtools/coding_practice_service.py`
- `services/ai/devtools/debug_service.py`
- `services/ai/devtools/codebase_service.py`

## ML Personalization

- `services/ai/ml/recommendation_model.py`
- `services/ai/ml/skill_prediction_model.py`
- `services/ai/ml/learning_difficulty_model.py`

These modules support optional `scikit-learn`, `numpy`, and `pandas` usage while preserving fallback behavior if those libraries are unavailable.

