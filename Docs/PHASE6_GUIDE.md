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
