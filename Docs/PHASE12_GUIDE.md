# Phase 12 Guide

## Overview

Phase 12 added peer community features and a gamification layer to encourage engagement and visible progression.

## Features Implemented

- community question posting
- answering and upvoting community discussions
- XP and level tracking
- badge awards
- dashboard integration for community and gamification

## Services Used

- `services/community/community_service.py`
- `services/community/gamification_service.py`

## Models Added

- `CommunityPost`
- `CommunityAnswer`
- `UserXP`
- `UserBadge`

## Routes Added

- `/community`
- `/community/post`
- `/community/question/<id>`
- `/community/answer`
- `/community/upvote/<answer_id>`

## Notes

Phase 12 also surfaces XP, badges, and community activity on the student dashboard.
## Documentation Refresh (May 20, 2026)

- `/student/referral` now uses a startup-style layout with cleaner sections, better spacing, copy/share actions, and readable reward history.
- Resume Analyzer UI was rebuilt to use space more efficiently with a two-panel workflow and clearer insights blocks.
- Resume Analyzer now auto-loads saved resume text from uploaded files (TXT/PDF/DOCX) when available.
- Resume analysis now powers targeted course recommendations by matching detected/missing skills against published courses while skipping already enrolled courses.
- If a new upload cannot be parsed, the system safely falls back to stored structured resume data instead of breaking the user flow.
