# Phase 6 Guide

## Overview

Phase 6 unified the growing AI feature set by introducing an assistant router that directs user questions to the right AI workflow.

## Features Implemented

- intent-aware assistant routing
- compatibility wrapper for chatbot integrations
- personalized assistant responses using student context
- preserved chatbot API contract for existing entry points

## Services Used

- `services/ai/assistant_service.py`
- `services/ai/mentor_service.py`
- `chatbot_service.py`
- `chatbot_service_hardcoded.py`

## Models Added

No new Phase 6 models were added.

## Routes Added

Phase 6 preserved chatbot entry points and continued to use:

- `/api/chatbot/ask`

## Notes

Phase 6 becomes the foundation for the Phase 13 multi-agent upgrade.
## Documentation Refresh (May 20, 2026)

- `/student/referral` now uses a startup-style layout with cleaner sections, better spacing, copy/share actions, and readable reward history.
- Resume Analyzer UI was rebuilt to use space more efficiently with a two-panel workflow and clearer insights blocks.
- Resume Analyzer now auto-loads saved resume text from uploaded files (TXT/PDF/DOCX) when available.
- Resume analysis now powers targeted course recommendations by matching detected/missing skills against published courses while skipping already enrolled courses.
- If a new upload cannot be parsed, the system safely falls back to stored structured resume data instead of breaking the user flow.
