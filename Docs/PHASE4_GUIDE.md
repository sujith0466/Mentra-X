# Phase 4 Guide

## Overview

Phase 4 introduced developer-focused AI tooling so students can practice coding, debug issues, and understand project structure.

## Features Implemented

- coding practice generator
- debugging assistant for tracebacks and errors
- codebase explainer

## Services Used

- `services/ai/devtools/coding_practice_service.py`
- `services/ai/devtools/debug_service.py`
- `services/ai/devtools/codebase_service.py`

## Models Added

No new Phase 4-specific models were added.

## Routes Added

- `/student/devtools/coding-practice`
- `/student/devtools/debug`
- `/student/devtools/codebase-explainer`

## Notes

The debug tooling introduced here is later reused by the Phase 13 `DebugAgent`.
