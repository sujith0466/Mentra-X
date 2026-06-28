# Mentra X — Prompt Versioning System

**Version:** 1.0  
**Owner:** Sujith Kumar AI  
**Location:** `backend/prompts/`

---

## Overview

Every LLM prompt in Mentra X is a versioned, documented artifact — not an inline string. This prevents silent prompt regressions, enables A/B testing between versions, and creates an audit trail of teaching strategy evolution.

---

## Prompt Lifecycle

```
Draft → Review → Active → Deprecated → Archived

Draft:       Written by engineer. Not used in production.
Review:      Peer-reviewed. Tested against Enkrypt validation score.
Active:      In production. All LLM calls use this version.
Deprecated:  Replaced by newer version. Still used by sessions in-flight.
Archived:    No longer used. Retained for audit trail.
```

---

## Directory Structure

```
backend/prompts/
├── __init__.py                   — Prompt loader utility
├── assessment/
│   ├── question_selection_v1.0.0.md
│   └── knowledge_estimation_v1.0.0.md
├── tutor/
│   ├── level_1_direct_v1.0.0.md
│   ├── level_2_worked_example_v1.0.0.md
│   ├── level_3_mistake_analysis_v1.0.0.md
│   ├── level_4_visual_analogy_v1.0.0.md
│   └── level_5_alternative_v1.0.0.md
├── verification/
│   ├── quiz_generation_v1.0.0.md
│   └── answer_evaluation_v1.0.0.md
├── enkrypt/
│   ├── regeneration_v1.0.0.md
│   └── fallback_notification_v1.0.0.md
└── insight/
    ├── weekly_report_v1.0.0.md
    └── opportunity_match_v1.0.0.md
```

---

## Prompt File Format

Every prompt file is a structured Markdown document with YAML frontmatter:

```yaml
---
prompt_id: TUTOR_LEVEL_4_VISUAL
version: 1.2.0
status: active
author: Sujith Kumar AI
owner: Sujith Kumar AI
created_at: 2026-06-28
updated_at: 2026-06-28
description: >
  Level 4 teaching prompt: Real-world visual analogy approach.
  Used when mastery is low and Level 2/3 have previously failed.
  Prioritises tangible, physical analogies before introducing formulas.

variables:
  - name: concept
    type: str
    description: "Concept identifier e.g. 'thermodynamics.entropy'"
    required: true
  - name: concept_label
    type: str
    description: "Human-readable concept label e.g. 'Entropy (Second Law)'"
    required: true
  - name: exam_track
    type: str
    description: "JEE | NEET | UPSC | CAT"
    required: true
  - name: student_name
    type: str
    description: "Student's first name for personalisation"
    required: false
    default: "the student"
  - name: avoided_analogies
    type: list[str]
    description: "Analogies that have previously failed for this student"
    required: false
    default: []
  - name: worked_analogies
    type: list[str]
    description: "Analogies that have previously succeeded for this student"
    required: false
    default: []
  - name: frustration_index
    type: float
    description: "Student frustration 0.0–1.0. High = gentler tone"
    required: false
    default: 0.3

expected_output:
  format: "prose explanation in 200–350 words"
  must_include:
    - "Real-world physical analogy (not mathematical)"
    - "Transition from analogy to concept"
    - "One concrete example relevant to exam_track"
    - "No formula until analogy is established"

safety_notes:
  - "Do NOT introduce formulas in the first paragraph"
  - "Do NOT use analogies listed in avoided_analogies"
  - "If frustration_index > 0.7, use especially gentle and encouraging tone"
  - "Output must pass Enkrypt Science Validator (score >= 0.90)"

enkrypt_target_score: 0.90
avg_enkrypt_score: 0.963      # Measured over last 1000 uses
avg_input_tokens: 284
avg_output_tokens: 421
approval_rate: 0.97           # % of uses that passed Enkrypt without regeneration

deprecation_policy: >
  This version is deprecated when a new version achieves avg_enkrypt_score > 0.980
  over 500+ uses. Old version retired after 7-day overlap window.

changelog:
  - version: "1.0.0"
    date: 2026-06-01
    changes: "Initial version"
  - version: "1.1.0"
    date: 2026-06-15
    changes: "Added avoided_analogies variable to prevent repetition"
  - version: "1.2.0"
    date: 2026-06-28
    changes: "Added frustration_index variable for tone adaptation"
---

# TUTOR_LEVEL_4_VISUAL — Prompt Body

## System Prompt

You are an expert tutor specializing in {exam_track} preparation. Your teaching philosophy prioritizes understanding over memorization. You always explain concepts through real-world analogies before introducing any mathematical framework.

**Student profile:**
- Concept: {concept_label}
- Teaching approach: Visual analogy first (Level 4)
- Frustration level: {frustration_index} (0=calm, 1=very frustrated)
- Avoid these analogies: {avoided_analogies}
- Analogies that worked before: {worked_analogies}

## Instructions

1. Start with a concrete, physical, everyday analogy that a non-scientist could understand.
2. Build the conceptual bridge from the analogy to the actual concept.
3. Do NOT introduce any formula until the analogy is fully explained (minimum 2 paragraphs).
4. Provide one worked example relevant to {exam_track} preparation.
5. End with a single, clear conceptual statement the student can remember.

## Tone Guidelines

{% if frustration_index > 0.7 %}
The student is frustrated. Use an especially warm, encouraging tone.
Avoid any language that implies the concept is "simple" or "obvious."
Validate that this concept is genuinely challenging.
{% else %}
Use a clear, confident, and engaging tone.
{% endif %}

## Output Format

Return the explanation as clean prose. Do not use bullet points or headers in your response to the student.
```

---

## Prompt Loader

```python
# backend/prompts/__init__.py

import yaml
from pathlib import Path
from functools import lru_cache
from string import Template

PROMPTS_DIR = Path(__file__).parent


@lru_cache(maxsize=50)
def load_prompt(prompt_id: str, version: str = "latest") -> dict:
    """
    Load a prompt definition by ID and version.
    Returns the full prompt metadata dict including body.
    """
    # Find all files matching prompt_id
    matches = list(PROMPTS_DIR.rglob(f"*{prompt_id.lower()}*.md"))
    if not matches:
        raise PromptNotFoundError(f"Prompt '{prompt_id}' not found")

    if version == "latest":
        # Sort by version number, return highest
        file = max(matches, key=_parse_version_from_filename)
    else:
        file = next((f for f in matches if version in f.name), None)
        if not file:
            raise PromptNotFoundError(f"Prompt '{prompt_id}' version '{version}' not found")

    content = file.read_text(encoding="utf-8")
    frontmatter, body = _parse_frontmatter(content)

    return {
        **frontmatter,
        "body": body,
        "file_path": str(file)
    }


def render_prompt(prompt_id: str, variables: dict, version: str = "latest") -> str:
    """
    Load prompt and substitute variables.
    Returns the rendered system prompt string.
    """
    prompt = load_prompt(prompt_id, version)
    body = prompt["body"]

    # Simple variable substitution (Jinja2 for complex logic)
    for key, value in variables.items():
        body = body.replace(f"{{{key}}}", str(value))

    return body
```

---

## Active Prompts Registry

| Prompt ID | Domain | Status | Version | Avg Enkrypt | Approval Rate |
|---|---|---|---|---|---|
| `ASSESSMENT_QUESTION_SELECT` | Assessment | active | 1.0.0 | N/A | N/A |
| `TUTOR_LEVEL_1_DIRECT` | Tutor | active | 1.0.0 | 0.94 | 0.98 |
| `TUTOR_LEVEL_2_WORKED` | Tutor | active | 1.1.0 | 0.95 | 0.97 |
| `TUTOR_LEVEL_3_MISTAKE` | Tutor | active | 1.0.0 | 0.92 | 0.95 |
| `TUTOR_LEVEL_4_VISUAL` | Tutor | active | 1.2.0 | 0.963 | 0.97 |
| `TUTOR_LEVEL_5_ALTERNATIVE` | Tutor | active | 1.0.0 | 0.91 | 0.94 |
| `VERIFICATION_QUIZ_GEN` | Verification | active | 1.0.0 | N/A | N/A |
| `ENKRYPT_REGENERATION` | Enkrypt | active | 1.0.0 | N/A | N/A |
| `INSIGHT_WEEKLY_REPORT` | Insight | active | 1.0.0 | N/A | N/A |

---

## Adding a New Prompt

1. Create file: `backend/prompts/{domain}/{prompt_id_lower}_v1.0.0.md`
2. Add YAML frontmatter with all required fields (see template above)
3. Write system prompt body with `{variable}` placeholders
4. Test: run 10 sample completions, measure Enkrypt score
5. Update Active Prompts Registry in this document
6. Register in relevant agent tool (`render_prompt("NEW_PROMPT_ID", variables)`)

---

## Deprecation Policy

1. New version developed → tested against 100+ sample interactions
2. New version avg Enkrypt score exceeds current by > 0.01 → candidate for promotion
3. Engineer sets old version to `status: deprecated`
4. 7-day overlap window: both versions active (old for in-flight sessions, new for new sessions)
5. After 7 days: old version set to `status: archived` (file retained, not deleted)
6. `lru_cache` cleared to force prompt loader to pick up new version
