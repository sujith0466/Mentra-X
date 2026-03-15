# Phase 7 Guide

## Overview

Phase 7 expanded Mentra from a small LMS catalog into a structured course ecosystem with domains, seeded learning paths, modules, videos, quizzes, assignments, and final projects.

## Features Implemented

- large seeded course ecosystem across multiple domains
- structured course modules using `CourseModule`
- syllabus topic generation
- lesson video population
- module-level quizzes and quiz questions
- practical assignments and final project assignments
- published course catalog expansion for students

## Domains Created

The Phase 7 seed script ensures domains for:

- Web Development
- Artificial Intelligence
- Data Science
- Machine Learning
- Cybersecurity
- Cloud Computing
- DevOps
- Mobile Development
- Blockchain
- Software Engineering

## Courses Seeded

The seed catalog populates multiple courses per domain, including examples such as:

- `HTML & CSS Fundamentals`
- `Introduction to Artificial Intelligence`
- `Data Science with Python`
- `Machine Learning Fundamentals`
- `AWS Basics`
- `DevOps Fundamentals`
- `Flutter Mobile Development`
- `Smart Contracts with Solidity`
- `System Design Fundamentals`

## Module Structure

Each domain uses a consistent module pattern with domain-specific titles and a final capstone module. Typical structure includes:

- foundational concepts
- core practical skills
- hands-on labs
- evaluation and best practices
- final project or capstone delivery

## Video Lessons

Each module is populated with guided videos using embedded learning content URLs defined per domain in the seed script.

## Quizzes

Each module receives a quiz with generated question records under `Quiz` and `QuizQuestion`.

## Assignments

Each module receives a practical assignment, and the final module receives a final project style assignment.

## Final Projects

The `Final Project` module in each seeded course includes a project-oriented assignment that acts as a capstone for the course.

## Services and Scripts Used

- `scripts/seed_courses_phase7.py`

## Models Used

Phase 7 relies on existing LMS models:

- `Domain`
- `Course`
- `CourseModule`
- `Syllabus`
- `Video`
- `Quiz`
- `QuizQuestion`
- `Assignment`

## Routes Added

No new Phase 7-specific routes were required. The seeded data powers existing course browsing and student learning routes.

## How to Run the Seed Script

Run the course ecosystem seed script from the project root:

```powershell
python .\scripts\seed_courses_phase7.py
```

The script is idempotent and updates existing records when they already exist.
