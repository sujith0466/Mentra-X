# Mentra X — Shared Data Transfer Objects (DTOs)

**Version:** 1.0  
**Owner:** Sujith Kumar AI  
**Location:** `backend/dto/`

---

## Overview

DTOs (Data Transfer Objects) are the typed contracts between API routes and service layers. They enforce structure, enable validation, and prevent raw dict passing between layers.

**Rules:**
- Routes receive/return DTOs (never raw dicts from services)
- Services accept/return DTOs (never parse request objects directly)
- DTOs use `dataclass` with `__post_init__` validation
- DTOs are serializable to/from JSON

---

## `backend/dto/__init__.py`

```python
"""
Mentra X Shared DTO Registry.

All DTOs are defined here and exported.
Import pattern: from backend.dto import TwinDTO, LearningDNADTO
"""

from .twin_dto import TwinDTO, TwinHealthDTO, TwinMutationDTO
from .learning_dna_dto import LearningDNADTO
from .memory_dto import HydratedContextDTO, MemoryQueryDTO
from .assessment_dto import AssessmentSessionDTO, AssessmentResultDTO
from .explanation_dto import ExplanationDTO, ValidationResultDTO
from .verification_dto import VerificationDTO
from .insight_dto import WeeklyReportDTO, WeaknessReportDTO
from .opportunity_dto import OpportunityMatchDTO

__all__ = [
    "TwinDTO", "TwinHealthDTO", "TwinMutationDTO",
    "LearningDNADTO",
    "HydratedContextDTO", "MemoryQueryDTO",
    "AssessmentSessionDTO", "AssessmentResultDTO",
    "ExplanationDTO", "ValidationResultDTO",
    "VerificationDTO",
    "WeeklyReportDTO", "WeaknessReportDTO",
    "OpportunityMatchDTO",
]
```

---

## `backend/dto/twin_dto.py`

```python
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any


@dataclass
class TwinHealthDTO:
    """
    Twin Health Score with contributing signals.
    Returned by GET /api/v1/twin/health
    """
    user_id: str
    health_score: float                     # 0.0–1.0 composite
    knowledge_coverage: float               # % concepts with mastery > 0.6
    retention_health: float                 # % concepts above decay threshold
    engagement_score: float                 # Session frequency score
    verification_pass_rate: float           # Rolling 10-session average
    total_concepts_tracked: int
    concepts_in_decay: int
    computed_at: datetime

    def __post_init__(self):
        assert 0.0 <= self.health_score <= 1.0, "health_score must be in [0, 1]"
        assert 0.0 <= self.verification_pass_rate <= 1.0

    def to_dict(self) -> dict:
        d = asdict(self)
        d["computed_at"] = self.computed_at.isoformat()
        return d


@dataclass
class TwinDTO:
    """
    Full Digital Twin representation.
    Returned by GET /api/v1/twin/profile
    """
    user_id: str
    exam_track: str
    twin_version: int
    twin_health: float

    # State summaries (not full nested objects — those are separate endpoints)
    academic_state: dict                    # enrolled_courses, xp_total, completion_rate
    knowledge_state: dict                   # concept_mastery per subject
    skill_state: dict                       # domain scores
    learning_dna: dict                      # preferred_level, style, frustration
    career_state: dict                      # resume status, interview count
    project_state: dict                     # active projects, completion rates
    opportunity_state: dict                 # match count, top match score

    last_mutated_at: datetime
    created_at: datetime

    def to_dict(self) -> dict:
        d = asdict(self)
        d["last_mutated_at"] = self.last_mutated_at.isoformat()
        d["created_at"] = self.created_at.isoformat()
        return d

    @classmethod
    def from_db_record(cls, record: Any, dna: LearningDNADTO) -> TwinDTO:
        """Factory method: build TwinDTO from MySQL student_twins record."""
        ...


@dataclass
class TwinMutationDTO:
    """
    Represents a single twin mutation for logging and response.
    Returned in mutation log responses.
    """
    user_id: str
    twin_version: int
    mutation_type: str          # "verification_pass" | "decay" | "assessment" | "cron"
    concept: str | None
    field_changed: str
    old_value: Any
    new_value: Any
    agent_name: str | None
    session_id: str | None
    mutated_at: datetime

    def to_dict(self) -> dict:
        d = asdict(self)
        d["mutated_at"] = self.mutated_at.isoformat()
        return d
```

---

## `backend/dto/learning_dna_dto.py`

```python
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class LearningDNADTO:
    """
    Student Learning DNA.
    The behavioral fingerprint used by all Tutor Agent decisions.
    """
    user_id: str
    exam_track: str

    # Teaching preferences
    preferred_level: int                            # 1–5
    preferred_style: str                            # "Visual" | "Mathematical" | "Narrative"
    prefers_examples_before_rules: bool

    # Frustration & engagement
    frustration_tolerance: float                    # 0.0–1.0
    engagement_window_mins: int
    verification_pass_rate: float                   # 0.0–1.0 rolling 10-session

    # Concept mastery (behavioral, not academic)
    mastery_per_concept: dict[str, float]           # concept_id → 0.0–1.0

    # Analogy effectiveness
    analogy_effectiveness: dict[str, float]         # analogy_type → success_rate

    # Ebbinghaus decay
    decay_coefficients: dict[str, float]            # concept_id → S-value
    last_reviewed: dict[str, str]                   # concept_id → ISO datetime string

    twin_version: int
    last_mutated_at: datetime

    def __post_init__(self):
        assert 1 <= self.preferred_level <= 5, "preferred_level must be 1–5"
        assert self.preferred_style in ("Visual", "Mathematical", "Narrative")
        assert 0.0 <= self.frustration_tolerance <= 1.0
        assert 0.0 <= self.verification_pass_rate <= 1.0

    def to_dict(self) -> dict:
        d = asdict(self)
        d["last_mutated_at"] = self.last_mutated_at.isoformat()
        return d

    def get_mastery(self, concept: str, default: float = 0.0) -> float:
        return self.mastery_per_concept.get(concept, default)

    def get_analogy_success(self, analogy_type: str) -> float:
        return self.analogy_effectiveness.get(analogy_type, 0.5)
```

---

## `backend/dto/memory_dto.py`

```python
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MemoryQueryDTO:
    """Input to MemoryService.retrieve_full_context()"""
    user_id: str
    query_text: str
    concept_tag: str | None = None
    top_k: int = 3


@dataclass
class TeachingConstraints:
    """Assembled constraints for the Tutor Agent."""
    preferred_level: int
    avoid_levels: list[int]              # Levels that failed for this concept
    avoid_analogies: list[str]           # Analogies that failed
    use_analogies: list[str]             # Analogies that worked
    max_formula_density: str             # "none" | "low" | "medium" | "high"


@dataclass
class StudentHistoryContext:
    """History signals for this specific concept."""
    asked_before: bool
    resolved_before: bool
    times_asked: int
    days_since_last_asked: int | None
    last_teaching_level: int | None


@dataclass
class WeaknessContext:
    """Active weakness signals for this concept."""
    flagged: bool
    severity: str | None                  # "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | None
    macro_weakness: str | None
    occurrence_count: int


@dataclass
class HydratedContextDTO:
    """
    The assembled context bundle passed to the Tutor Agent.
    Output of MemoryService.retrieve_full_context().
    """
    user_id: str
    query: str
    learning_dna: LearningDNADTO
    past_doubts: list[dict]              # Raw Qdrant payload dicts
    explanation_history: list[dict]      # Raw Qdrant payload dicts
    weak_concepts: list[dict]            # Raw Qdrant payload dicts

    # Assembled from raw data
    teaching_constraints: TeachingConstraints
    student_history: StudentHistoryContext
    weakness_context: WeaknessContext

    # Timing
    retrieval_duration_ms: int
    cache_hit: bool
```

---

## `backend/dto/assessment_dto.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AssessmentSessionDTO:
    """Represents an active assessment session."""
    session_id: str
    user_id: int
    exam_track: str
    status: str                    # "active" | "completed" | "abandoned"
    questions_served: int
    current_difficulty: int        # 1–5
    concepts_covered: list[str]
    started_at: datetime


@dataclass
class KnowledgeStateDTO:
    """Per-concept mastery estimates from assessment."""
    concept_mastery: dict[str, float]   # concept_cluster → 0.0–1.0
    coverage: int                        # Number of concepts assessed
    confidence: float                    # Overall estimator confidence


@dataclass
class AssessmentResultDTO:
    """Result of a completed assessment. Written to Digital Twin."""
    session_id: str
    user_id: int
    exam_track: str
    knowledge_state: KnowledgeStateDTO
    inferred_style: str             # "Visual" | "Mathematical" | "Narrative"
    inferred_level: int             # Initial preferred teaching level
    questions_served: int
    completed_at: datetime
    twin_version_after: int         # Twin version after assessment mutation
```

---

## `backend/dto/explanation_dto.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ValidationResultDTO:
    """Enkrypt validation result for a single explanation."""
    math_score: float
    science_score: float
    hallucination_score: float
    pedagogy_score: float
    composite_confidence: float
    flagged_claims: list[str]
    recommended_action: str         # "APPROVE" | "REGENERATE" | "HARD_FAIL"
    failure_context: str            # Attached to regeneration prompt if REGENERATE
    validation_duration_ms: int


@dataclass
class ExplanationDTO:
    """A complete explanation: generated text + validation result."""
    explanation_id: str
    user_id: str
    session_id: str
    concept: str
    teaching_level: int
    teaching_level_name: str        # "Direct" | "Worked Example" | etc.
    analogy_type: str | None
    explanation_text: str           # The actual explanation delivered to student
    validation: ValidationResultDTO
    is_fallback: bool               # True if textbook fallback was served
    fallback_source: str | None     # e.g., "NCERT Physics XI, Chapter 12"
    prompt_id: str
    prompt_version: str
    generated_at: datetime
```

---

## `backend/dto/verification_dto.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class VerificationDTO:
    """Result of a comprehension micro-quiz."""
    session_id: str
    user_id: str
    concept: str
    quiz_question: str
    student_answer: str
    correct_answer: str
    semantic_score: float           # 0.0–1.0 cosine similarity
    passed: bool                    # score >= 0.75
    mastery_delta: float            # Change applied to twin mastery
    twin_version_after: int
    verified_at: datetime
```

---

## `backend/dto/insight_dto.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class WeaknessClusterDTO:
    macro_weakness: str
    sub_topics: list[str]
    severity: str                   # "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
    severity_score: float
    occurrence_count: int
    recommended_revision_level: int


@dataclass
class WeaknessReportDTO:
    user_id: str
    sessions_analyzed: int
    macro_weaknesses: list[WeaknessClusterDTO]
    recurring_doubts: list[str]
    generated_at: datetime


@dataclass
class MasteryGainDTO:
    concept: str
    mastery_before: float
    mastery_after: float
    delta: float
    sessions_count: int


@dataclass
class WeeklyReportDTO:
    user_id: str
    week_start: date
    week_end: date
    sessions_completed: int
    xp_earned: int
    doubts_asked: int
    doubts_resolved: int
    mastery_gains: list[MasteryGainDTO]
    critical_weaknesses: list[WeaknessClusterDTO]
    revision_plan: list[dict]       # [{concept, day, duration_mins, urgency}]
    twin_health_score: float
    twin_health_delta: float        # Change vs. last week
    learning_velocity: str          # e.g., "+12% concept mastery in 7 days"
    generated_at: datetime
```

---

## `backend/dto/opportunity_dto.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from datetime import date


@dataclass
class OpportunityMatchDTO:
    opportunity_id: int
    type: str                       # "internship" | "hackathon" | "scholarship"
    title: str
    description: str
    match_score: float              # 0.0–1.0 cosine similarity
    matching_skills: list[str]      # Student has these + opportunity requires these
    gap_skills: list[str]           # Opportunity requires, student doesn't have yet
    deadline: date | None
    apply_url: str
    days_until_deadline: int | None

    def __post_init__(self):
        assert 0.0 <= self.match_score <= 1.0
        assert self.type in ("internship", "hackathon", "scholarship")
```

---

## DTO Validation Policy

All DTOs use `__post_init__` for invariant checks. Failed assertions raise `ValueError` which routes catch and return as `400 Bad Request` with the appropriate error code.

## DTO Versioning

When a DTO must change in a backward-incompatible way:
1. Create `TwinDTO_v2` (keep `TwinDTO` for backward compat)
2. New endpoint `/api/v2/twin/profile` uses `TwinDTO_v2`
3. Old endpoint `/api/v1/twin/profile` continues using `TwinDTO`
4. After 90-day deprecation window: `/api/v1/` route removed
