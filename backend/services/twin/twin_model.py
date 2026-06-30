from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class AcademicState:
    enrolled_courses: List[int] = field(default_factory=list)
    subject_mastery: Dict[str, float] = field(default_factory=dict)
    xp_total: int = 0
    completion_rate: float = 0.0
    streak_days: int = 0

@dataclass
class KnowledgeState:
    concept_mastery: Dict[str, float] = field(default_factory=dict)
    retention_health: Dict[str, float] = field(default_factory=dict)

@dataclass
class SkillState:
    skills: Dict[str, float] = field(default_factory=dict)

@dataclass
class LearningDNA:
    preferred_level: int = 1
    preferred_style: str = "Visual"
    prefers_examples_before_rules: bool = True
    frustration_tolerance: float = 0.8
    engagement_window_mins: int = 25
    verification_pass_rate: float = 0.0

@dataclass
class CareerState:
    skills_extracted: List[str] = field(default_factory=list)
    interview_score_avg: float = 0.0

@dataclass
class ProjectState:
    active_projects: Dict[int, float] = field(default_factory=dict)

@dataclass
class OpportunityState:
    recommended_jobs: List[int] = field(default_factory=list)

@dataclass
class StudentTwin:
    user_id: int
    twin_version: int
    twin_status: str
    twin_health: float
    exam_track: str
    academic_state: AcademicState = field(default_factory=AcademicState)
    knowledge_state: KnowledgeState = field(default_factory=KnowledgeState)
    skill_state: SkillState = field(default_factory=SkillState)
    learning_dna: LearningDNA = field(default_factory=LearningDNA)
    career_state: CareerState = field(default_factory=CareerState)
    project_state: ProjectState = field(default_factory=ProjectState)
    opportunity_state: OpportunityState = field(default_factory=OpportunityState)
