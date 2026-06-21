# Phase 13 Guide

## Overview

Phase 13 transformed the single AI assistant into a multi-agent AI system with specialized agents coordinated through a central router.

## Features Implemented

- central multi-agent assistant router
- specialized learning, debug, career, project, interview, community, and mentor agents
- compatibility-safe chatbot responses for old integrations
- dashboard AI assistant panel
- agent insight integration in the learning feed

## Services Used

- `services/ai/assistant_service.py`
- `services/ai/agents/base_agent.py`
- `services/ai/agents/mentor_agent.py`
- `services/ai/agents/learning_agent.py`
- `services/ai/agents/debug_agent.py`
- `services/ai/agents/career_agent.py`
- `services/ai/agents/project_agent.py`
- `services/ai/agents/interview_agent.py`
- `services/ai/agents/community_agent.py`

## Models Added

No new database models were required for Phase 13.

## Routes Added

No new standalone routes were introduced. Phase 13 upgrades the behavior behind existing chatbot and dashboard integrations.

## Notes

The router returns both the new multi-agent response shape and the older `answer` and `options` fields so existing chatbot consumers continue to work.
## Documentation Refresh (May 20, 2026)

- `/student/referral` now uses a startup-style layout with cleaner sections, better spacing, copy/share actions, and readable reward history.
- Resume Analyzer UI was rebuilt to use space more efficiently with a two-panel workflow and clearer insights blocks.
- Resume Analyzer now auto-loads saved resume text from uploaded files (TXT/PDF/DOCX) when available.
- Resume analysis now powers targeted course recommendations by matching detected/missing skills against published courses while skipping already enrolled courses.
- If a new upload cannot be parsed, the system safely falls back to stored structured resume data instead of breaking the user flow.
