# Phase 1 — Digital Twin Engine

---

## Phase Progress Dashboard

| Field | Value |
|---|---|
| **Status** | 🔴 NOT STARTED |
| **Phase Owner** | Sujith Kumar AI |
| **Phase** | 1 of 10 |
| **Depends On** | Phase 0 (Foundation) ✅ Complete |
| **Blocks** | Phase 2 (Assessment Engine) |
| **Estimated Duration** | 3–5 weeks (engineering time) |
| **Target Completion** | TBD |

### Completion

| Area | Status | % Done |
|---|---|---|
| `StudentTwin` model (7 states) | 🔴 Not started | 0% |
| Database tables (`student_twins`, `twin_mutation_log`) | 🔴 Not started | 0% |
| `TwinBuilder` service | 🔴 Not started | 0% |
| `TwinMutator` service | 🔴 Not started | 0% |
| `TwinHealthCalc` service | 🔴 Not started | 0% |
| `/api/v1/twin/*` endpoints | 🔴 Not started | 0% |
| Twin Health widget (frontend) | 🔴 Not started | 0% |
| `/twin/profile` page | 🔴 Not started | 0% |
| Unit tests | 🔴 Not started | 0% |
| Integration tests | 🔴 Not started | 0% |
| **TOTAL** | | **0%** |

### Known Issues
- None (not started)

### Technical Debt
- JSON storage of twin state in MySQL is a Phase 1 interim. Semantic/behavioral fields migrate to Qdrant in Phase 3.

### Blockers
- None. Phase 0 foundation is confirmed operational.

### Next Sprint
1. Define `StudentTwin` dataclass (all 7 states)
2. Create `student_twins` migration script
3. Implement `TwinBuilder.build_initial_twin()` reading existing MySQL data
4. Write unit tests for builder with edge cases (user with no quiz history)

### Notes
- Phase 1 deliberately avoids Qdrant. MySQL JSON is the interim storage to keep Phase 1 scope focused.
- Twin initialization should be triggered automatically on first student login if `ENABLE_DIGITAL_TWIN=true`.
- All mutations must use optimistic locking (check `twin_version` before write).

---


## Objective
Build the Student Digital Twin — the persistent, evolving cognitive model of every student. This is the architectural centerpiece of Mentra X. Every subsequent phase adds data to the twin or reads from it.

## Purpose
The Digital Twin transforms Mentra from a standard LMS into a personalized learning system. Without the twin, every AI interaction is stateless and generic. With the twin, every interaction is informed by a complete, permanent history of who the student is and how they learn.

## Scope
- `StudentTwin` data model (Python dataclass / SQLAlchemy model)
- All 7 twin state dimensions
- Twin initialization from existing MySQL data
- Twin mutation engine (write operations)
- Twin versioning system
- Twin Health Score calculator
- Twin Snapshot API
- Backend service layer for twin operations
- Basic frontend twin visualization (dashboard widget)

---

## Architecture Layer
**Layer 2 — Digital Twin Engine**

The Digital Twin Engine sits directly above the Foundation Layer. It reads from MySQL (academic ground truth) and will later write to Qdrant (semantic memory). In Phase 1, twin state is stored in MySQL until Qdrant is introduced in Phase 3.

---

## Components

### StudentTwin Model

```python
class StudentTwin:
    user_id: str                    # FK → users.id

    # State 1: Academic State (from MySQL)
    academic_state: AcademicState

    # State 2: Knowledge State
    knowledge_state: KnowledgeState

    # State 3: Skill State (from skill_progress)
    skill_state: SkillState

    # State 4: Learning Behavior State (Learning DNA)
    learning_dna: LearningDNA

    # State 5: Career State (from resumes, interview_sessions)
    career_state: CareerState

    # State 6: Project State (from student_projects)
    project_state: ProjectState

    # State 7: Opportunity State
    opportunity_state: OpportunityState

    # Metadata
    twin_version: int               # Increments on every mutation
    twin_health_score: float        # 0.0–1.0 composite
    created_at: datetime
    last_mutated_at: datetime
    exam_track: str                 # "JEE" | "NEET" | "UPSC" | "CAT"
```

### AcademicState

```python
class AcademicState:
    enrolled_courses: list[int]       # course IDs from MySQL
    subject_mastery: dict[str, float] # subject → 0.0–1.0
    xp_total: int                     # from user_xp
    completion_rate: float            # from lesson_progress
    streak_days: int                  # from learning_streaks
```

### KnowledgeState

```python
class KnowledgeState:
    concept_mastery: dict[str, float]      # concept_id → 0.0–1.0
    decay_coefficients: dict[str, float]   # concept_id → S-value (Ebbinghaus)
    last_reviewed: dict[str, datetime]     # concept_id → last interaction
    retention_health: dict[str, float]     # R = e^(-t/S) per concept
    mistake_count: dict[str, int]          # concept_id → total failures
```

### LearningDNA

```python
class LearningDNA:
    preferred_level: int                        # 1–5
    preferred_style: str                        # "Visual" | "Mathematical" | "Narrative"
    prefers_examples_before_rules: bool
    frustration_tolerance: float                # 0.0–1.0
    engagement_window_mins: int
    analogy_effectiveness: dict[str, float]     # analogy_type → success_rate
    verification_pass_rate: float               # rolling 10-session average
    mastery_per_concept: dict[str, float]       # behavioral mastery
```

### TwinHealthScore

```python
def compute_twin_health(twin: StudentTwin) -> float:
    """
    Composite score from 4 signals:
    - Knowledge coverage (% concepts with mastery > 0.6)         weight: 0.35
    - Retention health (% concepts above decay threshold)         weight: 0.30
    - Engagement consistency (session frequency, 30-day)          weight: 0.20
    - Verification pass rate (comprehension quiz success)         weight: 0.15
    """
    coverage  = breadth_score(twin.knowledge_state.concept_mastery)
    retention = retention_score(twin.knowledge_state.retention_health)
    engagement = engagement_score(twin.user_id)
    verification = twin.learning_dna.verification_pass_rate

    return (0.35 * coverage + 0.30 * retention +
            0.20 * engagement + 0.15 * verification)
```

---

## Folder Structure

```
backend/
├── services/
│   └── twin/
│       ├── __init__.py
│       ├── twin_model.py          — StudentTwin dataclass definitions
│       ├── twin_builder.py        — Builds twin from MySQL data on init
│       ├── twin_mutator.py        — Write operations: mutate(), version()
│       ├── twin_health.py         — TwinHealthScore calculator
│       └── twin_sync.py           — Sync MySQL → twin state
├── routes/
│   └── twin_routes.py             — /api/twin/* REST endpoints
└── models.py
    └── [ADD] StudentTwinRecord    — MySQL-backed twin persistence (Phase 1)
```

---

## Database Changes

### New Table: `student_twins`

```sql
CREATE TABLE student_twins (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    twin_version    INT NOT NULL DEFAULT 1,
    exam_track      VARCHAR(20) NOT NULL DEFAULT 'JEE',
    twin_health     FLOAT NOT NULL DEFAULT 0.0,
    academic_state  JSON,          -- AcademicState as JSON
    knowledge_state JSON,          -- KnowledgeState as JSON
    skill_state     JSON,          -- SkillState as JSON
    learning_dna    JSON,          -- LearningDNA as JSON
    career_state    JSON,          -- CareerState as JSON
    project_state   JSON,          -- ProjectState as JSON
    opportunity_state JSON,        -- OpportunityState as JSON
    last_mutated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_twin (user_id)
);
```

> **Note:** In Phase 1, twin state is stored as JSON in MySQL. In Phase 3, semantic/behavioral fields are migrated to Qdrant. MySQL retains the twin record as an anchor.

### New Table: `twin_mutation_log`

```sql
CREATE TABLE twin_mutation_log (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    twin_version    INT NOT NULL,
    mutation_type   VARCHAR(50) NOT NULL,  -- 'verification_pass', 'verification_fail', 'decay', 'cron'
    concept         VARCHAR(100),
    field_changed   VARCHAR(100),
    old_value       TEXT,
    new_value       TEXT,
    agent_name      VARCHAR(50),
    session_id      VARCHAR(100),
    mutated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## Backend Changes

### New Service: `backend/services/twin/twin_builder.py`

Responsible for **initializing** a new student's Digital Twin from existing MySQL data:

```python
def build_initial_twin(user_id: int, exam_track: str) -> StudentTwin:
    """
    Reads existing MySQL data to construct the initial twin state:
    - AcademicState: from courses, lesson_progress, user_xp, learning_streaks
    - KnowledgeState: from quiz_attempts (score → concept mastery mapping)
    - SkillState: from skill_progress
    - LearningDNA: default profile seeded from exam_track defaults
    - CareerState: from user_resumes, interview_sessions
    - ProjectState: from student_projects, project_tasks
    - OpportunityState: empty on init
    """
```

### New Service: `backend/services/twin/twin_mutator.py`

Handles all **write operations** to the twin:

```python
def mutate_knowledge(user_id, concept, delta, mutation_type, session_id): ...
def mutate_learning_dna(user_id, field, new_value, session_id): ...
def mutate_weakness_state(user_id, weaknesses): ...
def increment_version(user_id) -> int: ...
def log_mutation(user_id, twin_version, mutation_type, field, old, new): ...
```

### New Service: `backend/services/twin/twin_health.py`

```python
def compute_and_store_health(user_id: int) -> float:
    """Computes TwinHealthScore and writes to student_twins.twin_health"""
```

---

## Frontend Changes

### New Widget: Twin Health Score Card (Student Dashboard)

Add a `Twin Health` card to the existing student dashboard:

```html
<!-- Positioned alongside existing XP card -->
<div class="twin-health-card">
  <h3>Learning Twin Health</h3>
  <div class="health-ring">{{ twin_health * 100 }}%</div>
  <p>{{ knowledge_coverage }} concepts tracked</p>
  <p>{{ retention_health }} concepts above retention threshold</p>
  <a href="/twin/profile">View Full Twin Profile →</a>
</div>
```

### New Page: `/twin/profile`

- Twin state visualisation (7-state breakdown)
- Learning DNA summary (preferred level, style, frustration index)
- Knowledge map (concept mastery per subject)
- Twin version history

---

## APIs

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/api/twin/profile` | Returns full StudentTwin for authenticated student | Student |
| `GET` | `/api/twin/health` | Returns TwinHealthScore + contributing signals | Student |
| `POST` | `/api/twin/snapshot` | Saves a versioned twin snapshot | Internal |
| `POST` | `/api/twin/initialize` | Builds twin from MySQL data for new user | Internal |
| `GET` | `/api/twin/dna` | Returns Learning DNA only | Student |
| `GET` | `/api/twin/knowledge` | Returns KnowledgeState with decay info | Student |
| `GET` | `/api/twin/mutations` | Returns recent mutation log for debugging | Admin |

---

## Services

| Service | File | Responsibility |
|---|---|---|
| TwinBuilder | `twin_builder.py` | Initializes twin from MySQL data |
| TwinMutator | `twin_mutator.py` | All write operations + version increment |
| TwinHealthCalc | `twin_health.py` | Computes and stores health score |
| TwinSync | `twin_sync.py` | Periodically re-syncs MySQL data into twin |

---

## Agent Changes
None in Phase 1. Agent layer begins in Phase 4.

## Memory Changes
None in Phase 1. Qdrant introduced in Phase 3.

---

## Deliverables
- [ ] `student_twins` table created and migrated
- [ ] `twin_mutation_log` table created and migrated
- [ ] `StudentTwin` model fully defined (all 7 states)
- [ ] `TwinBuilder` service: builds initial twin from MySQL
- [ ] `TwinMutator` service: write operations with versioning
- [ ] `TwinHealthCalc` service: composite health score
- [ ] `/api/twin/*` REST endpoints implemented and tested
- [ ] Twin Health widget added to student dashboard
- [ ] `/twin/profile` page implemented
- [ ] Mutation log working on every state change

## Acceptance Criteria
- [ ] Every student account has exactly one `student_twins` record after initialization
- [ ] `twin_version` increments atomically on every mutation
- [ ] `TwinHealthScore` returns a value in [0.0, 1.0]
- [ ] Twin initialization correctly reads and maps all existing MySQL data
- [ ] `/api/twin/profile` returns a valid JSON twin for authenticated student
- [ ] Existing routes and functionality unchanged

## Testing Checklist
- [ ] Unit test: `build_initial_twin()` for user with quiz history
- [ ] Unit test: `compute_twin_health()` edge cases (0 concepts, full coverage)
- [ ] Unit test: `mutate_knowledge()` increments version and logs mutation
- [ ] Integration test: POST `/api/twin/initialize` → twin record created in DB
- [ ] Integration test: GET `/api/twin/health` → returns correct composite score
- [ ] Regression test: all existing `/api/*` routes still return 200
- [ ] Regression test: admin login, student login still functional

---

## Dependencies
- Phase 0: Foundation Layer ✅

## Risks
- JSON fields in MySQL may become unwieldy at scale → **Mitigation:** Semantic fields migrated to Qdrant in Phase 3. MySQL JSON is a Phase 1 interim solution only.
- Twin initialization logic may miss edge cases (users with no quiz history) → **Mitigation:** Cold-start defaults defined per exam track.
- Twin mutation race conditions (concurrent sessions) → **Mitigation:** Optimistic locking using `twin_version` check before write.

## Future Extensions
- Phase 3: Migrate `learning_dna` and `knowledge_state` fields to Qdrant vector storage.
- Phase 4: Mastra agents read and mutate the twin via standardized tool calls.
- Phase 7: Continuous decay engine runs as background job on the twin's `knowledge_state`.