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
