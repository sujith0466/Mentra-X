# Phase 10 Guide

## Overview

Phase 10 added AI-assisted interview preparation, including mock interview sessions, coding interview prompts, and answer feedback.

## Features Implemented

- role-based mock interviews
- technical, coding, and behavioral questions
- interview session creation and completion
- AI feedback for each answer
- final interview scoring
- skill progress updates from interview performance

## Services Used

- `services/ai/interview/interview_question_service.py`
- `services/ai/interview/interview_session_service.py`
- `services/ai/interview/interview_feedback_service.py`

## Models Added

- `InterviewSession`
- `InterviewQuestion`
- `InterviewResponse`

## Routes Added

- `/student/interview`
- `/student/interview/start`
- `/student/interview/session/<id>`
- `/student/interview/submit`
- `/student/interview/result/<id>`

## Notes

Interview sessions reuse coding challenges for coding interview mode and update the learning feed and skill graph after completion.
