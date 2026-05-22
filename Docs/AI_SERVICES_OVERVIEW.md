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

## Phase-1 Enhancements — Resume Intelligence Upgrade

- Resume parsing now extracts skills, projects, education, and experience into `UserResume`.
- Skill gap detection includes resume skills plus enrolled/completed course signals.
- Recommendations and career roadmaps prioritize missing skills with safe fallbacks when resume data is unavailable.

## Phase-2 Enhancements — AI Learning Intelligence

- Smart revision uses quiz, assignment, lesson completion, and coding performance signals.
- Portfolio builder includes resume projects, completed courses, and coding challenge solutions.
- Project idea generation is personalized using resume skills and course history.
- Learning insights combine weak topics, suggested skills, and course recommendations with fallbacks.

## Phase-3 Enhancements - Developer Platform Upgrade

- Coding practice adds language-aware execution, run/submit actions, and clearer output summaries.
- Debugging assistant supports error text, stack traces, and code snippets with structured fixes.
- Codebase explainer covers project structures plus code snippet explanations with improvement suggestions.
- Developer tools UI aligns card layouts and code blocks across the coding and devtools pages.



## Phase-4 Enhancements - Platform UX & System Improvements

- Learning feed UI now supports structured cards with action links and safe fallbacks.
- Profile updates persist via lightweight JSON storage without schema changes.
- Wallet and reward helpers centralize referral reward history and balance display.
- Referral flow supports /ref/<code> links with session tracking and validation.
## Documentation Refresh (May 20, 2026)

- `/student/referral` now uses a startup-style layout with cleaner sections, better spacing, copy/share actions, and readable reward history.
- Resume Analyzer UI was rebuilt to use space more efficiently with a two-panel workflow and clearer insights blocks.
- Resume Analyzer now auto-loads saved resume text from uploaded files (TXT/PDF/DOCX) when available.
- Resume analysis now powers targeted course recommendations by matching detected/missing skills against published courses while skipping already enrolled courses.
- If a new upload cannot be parsed, the system safely falls back to stored structured resume data instead of breaking the user flow.
