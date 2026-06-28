# Mentra X — Engineering Standards

**Version:** 1.0  
**Owner:** Sujith Kumar AI  
**Applies to:** All backend, frontend, and documentation work in the Mentra X repository.

---

## Table of Contents

1. Naming Conventions
2. Folder Standards
3. Python Standards
4. Git Branch Naming
5. Commit Message Format
6. PR Checklist
7. Code Review Checklist
8. Documentation Checklist
9. Testing Standards
10. API Design Standards

---

## 1. Naming Conventions

### Python Files & Modules

| Element | Convention | Example |
|---|---|---|
| Python files | `snake_case` | `twin_mutator.py`, `memory_service.py` |
| Classes | `PascalCase` | `TwinMutator`, `MemoryService` |
| Functions / methods | `snake_case` | `compute_retention()`, `build_context()` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRY_ATTEMPTS`, `RETENTION_THRESHOLD` |
| Private methods | `_snake_case` | `_process_user_decay()`, `_build_prompt()` |
| Type aliases | `PascalCase` | `ConceptId`, `UserIdStr` |
| Dataclass fields | `snake_case` | `preferred_level`, `twin_version` |
| Config variables | `UPPER_SNAKE_CASE` | `QDRANT_HOST`, `OPENAI_API_KEY` |

### Database

| Element | Convention | Example |
|---|---|---|
| Tables | `snake_case` (plural) | `student_twins`, `revision_tasks` |
| Columns | `snake_case` | `user_id`, `concept_tag`, `mastery_score` |
| Foreign keys | `{table_singular}_id` | `user_id`, `opportunity_id` |
| Indexes | `idx_{table}_{columns}` | `idx_twins_user`, `idx_sessions_date` |
| JSON columns | `snake_case` | `knowledge_state`, `learning_dna` |

### Qdrant Collections

| Convention | Format | Example |
|---|---|---|
| Collection names | `snake_case` | `learning_dna`, `past_doubts` |
| Payload fields | `snake_case` | `user_id`, `concept_tag`, `twin_version` |
| Test collections | `test_{collection}` | `test_learning_dna` |

### API Endpoints

| Convention | Format | Example |
|---|---|---|
| Base path | `/api/v1/` | `/api/v1/` |
| Resources | `kebab-case` (plural) | `/api/v1/twin-profiles` |
| Sub-resources | `{resource}/{id}/{sub}` | `/api/v1/twins/123/knowledge` |
| Actions | `{resource}/{action}` | `/api/v1/assessment/complete` |
| Query params | `snake_case` | `?user_id=...&top_k=3` |

### Feature Flags

| Convention | Format | Example |
|---|---|---|
| Flag names | `ENABLE_{FEATURE}` (bool) | `ENABLE_DIGITAL_TWIN` |
| Tier flags | `TIER_{FEATURE}` (string) | `TIER_ENKRYPT` |

### Error Codes

| Convention | Format | Example |
|---|---|---|
| Domain prefix | `{DOMAIN}_{NNN}` | `TWIN_001`, `MEMORY_003` |
| Domain codes | `TWIN`, `MEMORY`, `MASTRA`, `ENKRYPT`, `ASSESSMENT`, `AUTH`, `SYS` | |

---

## 2. Folder Standards

### Backend Structure

```
backend/
├── app.py                      — Flask factory (ONLY: app init, blueprint registration, DB init)
├── models.py                   — ALL SQLAlchemy models (single file for discoverability)
├── run.py                      — Production entry point (import app, run waitress)
│
├── routes/                     — Flask blueprints (HTTP layer ONLY — no business logic)
│   ├── auth_routes.py
│   ├── student_routes.py
│   ├── admin_routes.py
│   ├── ai_routes.py            — Phase 0: existing chatbot (preserved)
│   ├── twin_routes.py          — Phase 1+: /api/v1/twin/*
│   ├── assessment_routes.py    — Phase 2+: /api/v1/assessment/*
│   ├── memory_routes.py        — Phase 3+: /api/v1/memory/*
│   ├── swarm_routes.py         — Phase 4+: /api/v1/swarm/*
│   ├── intelligence_routes.py  — Phase 8+: /api/v1/intelligence/*
│   └── ui_routes.py            — Phase 9+: /api/v1/ui/*
│
├── services/                   — Business logic (pure Python, no Flask dependencies)
│   ├── twin/                   — Phase 1: Digital Twin services
│   ├── assessment/             — Phase 2: Assessment services
│   ├── memory/                 — Phase 3: Qdrant memory services
│   ├── adaptive/               — Phase 5: Adaptive intelligence
│   ├── enkrypt/                — Phase 6: Safety validation
│   ├── learning/               — Phase 7: Continuous learning
│   └── intelligence/           — Phase 8: Intelligence layer
│
├── mastra/                     — Phase 4+: Agent definitions and tools
│   ├── agents/                 — One file per agent
│   ├── tools/                  — Mastra tool implementations
│   ├── workflows/              — DAG + cron workflow definitions
│   └── swarm.py                — Agent registry
│
├── dto/                        — Data Transfer Objects (shared types)
│   ├── __init__.py
│   ├── twin_dto.py
│   ├── memory_dto.py
│   ├── assessment_dto.py
│   ├── explanation_dto.py
│   ├── insight_dto.py
│   └── opportunity_dto.py
│
├── prompts/                    — Versioned prompt templates
│   ├── assessment/
│   ├── tutor/
│   ├── verification/
│   ├── enkrypt/
│   └── insight/
│
├── scheduler/                  — Phase 7+: Background job scheduler
│   ├── __init__.py
│   └── jobs.py
│
├── events/                     — Event bus system
│   ├── __init__.py
│   ├── event_bus.py
│   └── handlers/
│
├── monitoring/                 — Health checks + metrics
│   ├── health_check.py
│   └── metrics.py
│
├── security/                   — Rate limiting, input validation
│   ├── rate_limiter.py
│   └── validators.py
│
└── tests/                      — All tests
    ├── unit/
    ├── integration/
    ├── e2e/
    └── conftest.py
```

### Rules

1. **Routes contain NO business logic.** They parse requests, call services, return responses.
2. **Services contain NO Flask imports.** They are pure Python functions and classes.
3. **DTOs are the contract** between routes and services. Never pass raw dicts across layers.
4. **One agent per file** in `mastra/agents/`.
5. **No circular imports.** Route → Service → DTO (never in reverse).

---

## 3. Python Standards

### Version & Environment

- Python: **3.10+** (use `match` statements, `|` union types, structural pattern matching)
- Virtual environment: `venv` (always activate before working)
- Package management: `pip` with `requirements.txt` (pinned versions)

### Code Style

- Formatter: **Black** (line length 100)
- Linter: **Flake8** + **pylint**
- Type checker: **mypy** (strict mode on service layer)
- Import order: `isort` (stdlib → third-party → local)

### Type Hints

All functions in `services/` MUST have complete type hints:

```python
# CORRECT
def compute_retention(
    mastery_score: float,
    last_reviewed: datetime,
    stability_s: float = 7.0
) -> float:
    ...

# INCORRECT — no type hints
def compute_retention(mastery, last_reviewed, s):
    ...
```

### Docstrings

All public classes and functions must have docstrings:

```python
def select_explanation_level(
    concept: str,
    dna: LearningDNA,
    explanation_history: list[ExplanationRecord]
) -> int:
    """
    Select the optimal teaching level (1–5) for a concept given the student's
    Learning DNA and prior explanation history.

    Args:
        concept: Concept identifier (e.g., "thermodynamics.entropy")
        dna: Student's Learning DNA from Qdrant learning_dna collection
        explanation_history: Past explanation records for this concept

    Returns:
        Teaching level 1–5 (see TEACHING_LEVELS for definitions)

    Raises:
        ValueError: If concept is empty or dna.preferred_level is out of range
    """
```

### Error Handling

Never use bare `except`. Always specify exception types:

```python
# CORRECT
try:
    result = qdrant_client.get(collection="learning_dna", user_id=user_id)
except QdrantConnectionError as e:
    logger.error("MEMORY_010: Qdrant unavailable", extra={"user_id": user_id, "error": str(e)})
    return fallback_from_mysql(user_id)
except QdrantNotFoundError:
    logger.warning("MEMORY_001: Collection not found", extra={"collection": "learning_dna"})
    raise MemoryError("MEMORY_001")

# INCORRECT
try:
    result = qdrant_client.get(...)
except:
    pass
```

### Logging

Use structured logging everywhere in services:

```python
import logging
logger = logging.getLogger(__name__)

# Use extra= for structured fields (searchable in log aggregation)
logger.info(
    "Twin mutation complete",
    extra={
        "user_id": user_id,
        "concept": concept,
        "old_mastery": old_value,
        "new_mastery": new_value,
        "twin_version": twin_version,
        "mutation_type": "verification_pass"
    }
)
```

### Constants

All magic numbers must be named constants:

```python
# backend/services/learning/constants.py
DEFAULT_STABILITY_S = 7.0           # Ebbinghaus stability (days) for new concepts
RETENTION_THRESHOLD = 0.50          # Below this → trigger revision
CRITICAL_RETENTION_THRESHOLD = 0.30 # Below this → urgent alert
ENKRYPT_PASS_THRESHOLD = 0.90       # Minimum Enkrypt confidence to approve
ENKRYPT_REGEN_THRESHOLD = 0.70      # Below this → hard fail
MAX_REGEN_ATTEMPTS = 2              # Maximum regeneration attempts
VERIFICATION_PASS_THRESHOLD = 0.75  # Semantic similarity threshold for quiz pass
```

---

## 4. Git Branch Naming

| Branch Type | Format | Example |
|---|---|---|
| Feature | `feature/phase-N-description` | `feature/phase-1-twin-model` |
| Bug fix | `fix/description` | `fix/qdrant-cache-invalidation` |
| Documentation | `docs/description` | `docs/phase-3-memory-guide` |
| Hotfix (production) | `hotfix/description` | `hotfix/admin-login-csrf` |
| Experiment | `experiment/description` | `experiment/irt-bayesian-v2` |
| Release | `release/vN.N` | `release/v1.0` |

**Rules:**
- Branch from `main` always.
- Never commit directly to `main`.
- Phase branches are named after the phase they implement.
- Branch names are lowercase, hyphen-separated, < 50 characters.

---

## 5. Commit Message Format

```
[Phase-N] type: short description (max 72 chars)

Optional longer description explaining WHY (not WHAT).
What was the problem? Why this approach?

Refs: TWIN_001, #issue-number
```

### Commit Types

| Type | When to Use |
|---|---|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code change that neither adds feature nor fixes bug |
| `test` | Adding or modifying tests |
| `docs` | Documentation only |
| `chore` | Dependency updates, config changes |
| `perf` | Performance improvement |
| `security` | Security fix |

### Examples

```
[Phase-1] feat: add StudentTwin model with 7-state architecture

[Phase-3] feat: implement parallel Qdrant retrieval in MemoryService

[Phase-6] fix: Enkrypt hard fail now correctly serves textbook fallback

[Phase-7] perf: batch Qdrant upserts in nightly decay job (100 users/batch)

docs: add ADR-003 for Qdrant vector memory decision

security: replace hardcoded admin password with env var DEFAULT_ADMIN_PASSWORD
```

---

## 6. PR Checklist

Every pull request must satisfy all of the following before review:

### Code Quality
- [ ] All new functions have type hints
- [ ] All public functions have docstrings
- [ ] No bare `except` clauses
- [ ] No hardcoded credentials, API keys, or passwords
- [ ] No `print()` statements (use `logger`)
- [ ] All magic numbers replaced with named constants
- [ ] Black formatting applied (`black backend/ --line-length 100`)
- [ ] isort applied (`isort backend/`)

### Testing
- [ ] Unit tests written for all new service functions
- [ ] Integration test updated if new API endpoint added
- [ ] All existing tests still pass (`pytest backend/tests/ -v`)
- [ ] Coverage not decreased below 80%

### Architecture
- [ ] No business logic in routes
- [ ] No Flask imports in services
- [ ] DTOs used for cross-layer communication
- [ ] Feature flag added for any significant new capability
- [ ] Event emitted if action should trigger downstream processes

### Documentation
- [ ] Relevant phase document updated
- [ ] New errors added to `Docs/Errors/ERROR_CATALOG.md`
- [ ] New env vars added to environment variables reference
- [ ] GOVERNANCE.md progress table updated if milestone completed

### Security
- [ ] No new secrets in source code
- [ ] New endpoints have rate limiting applied
- [ ] New endpoints have input validation (Marshmallow schema)
- [ ] New admin endpoints check for admin role

---

## 7. Code Review Checklist

Reviewers must check:

### Logic
- [ ] Does the implementation match the phase document specification?
- [ ] Are edge cases handled (empty input, user not found, Qdrant unavailable)?
- [ ] Is error handling correct (right error code, right recovery strategy)?

### Performance
- [ ] Are Qdrant queries filtered by `user_id` (no full-collection scans)?
- [ ] Are expensive operations async where possible?
- [ ] Is caching applied for hot-path reads (learning_dna → Redis)?

### Security
- [ ] No cross-user data leakage possible?
- [ ] Are all user inputs validated before use?
- [ ] Are admin-only routes protected?

### Maintainability
- [ ] Is the code easy to understand without running it?
- [ ] Are there comments explaining non-obvious decisions?
- [ ] Is the code modular (testable in isolation)?

---

## 8. Documentation Checklist

Before closing any phase:

- [ ] All phase deliverables checked off in the phase document
- [ ] All acceptance criteria met and verified
- [ ] Test checklist completed
- [ ] `GOVERNANCE.md` progress table updated (phase status → COMPLETE)
- [ ] Any new architectural decisions recorded as ADRs
- [ ] Error catalog updated with any new error codes

---

## 9. Testing Standards

| Layer | Minimum Coverage | Runner |
|---|---|---|
| Unit | 80% line coverage | `pytest backend/tests/unit/` |
| Integration | All critical paths covered | `pytest backend/tests/integration/` |
| E2E | Student journey test passes | `pytest backend/tests/e2e/` |

### Naming Convention for Tests

```python
# Pattern: test_{unit}_{condition}_{expected_result}

def test_decay_engine_14_days_returns_near_zero_retention():
def test_twin_mutator_version_increments_on_every_write():
def test_enkrypt_validator_wrong_formula_returns_low_score():
def test_memory_service_user_isolation_prevents_cross_user_read():
```

### Test Data Management

- Unit tests: use fixtures and mocks only (no real DB)
- Integration tests: use `test_` prefixed Qdrant collections; cleanup in `teardown`
- E2E tests: use dedicated test user account (`test_aryan@mentrax.dev`)

---

## 10. API Design Standards

### Version Prefix

All new API endpoints use `/api/v1/` prefix:

```
CORRECT:   /api/v1/twin/profile
INCORRECT: /api/twin/profile
```

Existing pre-AI routes (`/api/courses`, `/api/quiz`, etc.) retain their original paths for backward compatibility until a formal v1 migration is planned.

### Response Format

All API responses follow this standard envelope:

```json
{
    "success": true,
    "data": { ... },
    "meta": {
        "timestamp": "2026-06-28T12:00:00Z",
        "version": "1.0",
        "request_id": "req_abc123"
    }
}
```

Error responses:

```json
{
    "success": false,
    "error": {
        "code": "TWIN_001",
        "message": "Digital Twin not initialized for this user.",
        "recovery": "Call POST /api/v1/twin/initialize first.",
        "severity": "HIGH"
    },
    "meta": {
        "timestamp": "2026-06-28T12:00:00Z",
        "request_id": "req_abc123"
    }
}
```

### HTTP Methods

| Operation | Method | Example |
|---|---|---|
| Read resource | `GET` | `GET /api/v1/twin/profile` |
| Create resource | `POST` | `POST /api/v1/twin/initialize` |
| Full update | `PUT` | `PUT /api/v1/twin/dna` |
| Partial update | `PATCH` | `PATCH /api/v1/twin/knowledge` |
| Delete | `DELETE` | `DELETE /api/v1/assessment/session/:id` |
| Action/trigger | `POST` | `POST /api/v1/intelligence/analyze` |
