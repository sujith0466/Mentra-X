"""
Mentra X — Autonomous Learning Intelligence DTOs (Phase 9)

Defines clean, serializable Data Transfer Objects for all Phase 9 milestones:
- Autonomous Learning Brain Decisions
- Daily, Weekly & Monthly Missions
- Adaptive Schedule Rebalancing
- Spaced Repetition Revision Queues
- Habit Intelligence & Streak Analytics
- Proactive AI Mentor Interventions
- Predictive Success Forecasts
"""

import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone


@dataclass
class AutonomousDecisionDTO:
    user_id: int
    action_type: str  # LEARN_NEW, REVISE_CONCEPT, SOLVE_CODING, WATCH_LECTURE, REMEDIATE_WEAKNESS, REST_RECOVERY
    target_concept: str
    rationale: str
    confidence_score: float
    estimated_duration_mins: int
    priority: str  # HIGH, MEDIUM, LOW
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "action_type": self.action_type,
            "target_concept": self.target_concept,
            "rationale": self.rationale,
            "confidence_score": self.confidence_score,
            "estimated_duration_mins": self.estimated_duration_mins,
            "priority": self.priority,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AutonomousDecisionDTO":
        return cls(
            user_id=data.get("user_id", 0),
            action_type=data.get("action_type", "LEARN_NEW"),
            target_concept=data.get("target_concept", ""),
            rationale=data.get("rationale", ""),
            confidence_score=float(data.get("confidence_score", 0.0)),
            estimated_duration_mins=int(data.get("estimated_duration_mins", 30)),
            priority=data.get("priority", "MEDIUM"),
            metadata=data.get("metadata", {})
        )


@dataclass
class MissionTaskDTO:
    task_id: str
    title: str
    category: str  # REVISION, PROBLEM_SOLVING, NEW_CONCEPT, LECTURE, REMEDIATION
    concept: str
    duration_mins: int
    xp_reward: int
    completed: bool = False
    action_url: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "category": self.category,
            "concept": self.concept,
            "duration_mins": self.duration_mins,
            "xp_reward": self.xp_reward,
            "completed": self.completed,
            "action_url": self.action_url
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MissionTaskDTO":
        return cls(
            task_id=str(data.get("task_id", "")),
            title=data.get("title", ""),
            category=data.get("category", "NEW_CONCEPT"),
            concept=data.get("concept", ""),
            duration_mins=int(data.get("duration_mins", 30)),
            xp_reward=int(data.get("xp_reward", 50)),
            completed=bool(data.get("completed", False)),
            action_url=data.get("action_url", "")
        )


@dataclass
class DailyMissionDTO:
    user_id: int
    mission_date: str
    daily_tasks: List[MissionTaskDTO] = field(default_factory=list)
    weekly_mission: str = ""
    monthly_goal: str = ""
    completion_percentage: float = 0.0
    total_duration_mins: int = 0
    total_xp: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "mission_date": self.mission_date,
            "daily_tasks": [t.to_dict() if isinstance(t, MissionTaskDTO) else t for t in self.daily_tasks],
            "weekly_mission": self.weekly_mission,
            "monthly_goal": self.monthly_goal,
            "completion_percentage": self.completion_percentage,
            "total_duration_mins": self.total_duration_mins,
            "total_xp": self.total_xp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DailyMissionDTO":
        tasks_raw = data.get("daily_tasks", [])
        tasks = [MissionTaskDTO.from_dict(t) if isinstance(t, dict) else t for t in tasks_raw]
        return cls(
            user_id=int(data.get("user_id", 0)),
            mission_date=data.get("mission_date", ""),
            daily_tasks=tasks,
            weekly_mission=data.get("weekly_mission", ""),
            monthly_goal=data.get("monthly_goal", ""),
            completion_percentage=float(data.get("completion_percentage", 0.0)),
            total_duration_mins=int(data.get("total_duration_mins", 0)),
            total_xp=int(data.get("total_xp", 0))
        )


@dataclass
class ScheduleBlockDTO:
    time_slot: str  # e.g., "18:00 - 18:45"
    activity_name: str
    category: str
    duration_mins: int
    priority: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "time_slot": self.time_slot,
            "activity_name": self.activity_name,
            "category": self.category,
            "duration_mins": self.duration_mins,
            "priority": self.priority
        }


@dataclass
class AdaptiveScheduleDTO:
    user_id: int
    date: str
    blocks: List[ScheduleBlockDTO] = field(default_factory=list)
    workload_score: float = 0.0  # 0 to 10
    fatigue_index: float = 0.0   # 0 to 1
    rebalance_rationale: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "date": self.date,
            "blocks": [b.to_dict() if isinstance(b, ScheduleBlockDTO) else b for b in self.blocks],
            "workload_score": self.workload_score,
            "fatigue_index": self.fatigue_index,
            "rebalance_rationale": self.rebalance_rationale
        }


@dataclass
class RevisionItemDTO:
    concept: str
    domain: str
    days_since_last_review: int
    recommended_interval_days: int
    retention_estimate: float  # 0 to 1
    urgency: str  # CRITICAL, OVERDUE, SCHEDULED, UPCOMING
    sm2_ease_factor: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "concept": self.concept,
            "domain": self.domain,
            "days_since_last_review": self.days_since_last_review,
            "recommended_interval_days": self.recommended_interval_days,
            "retention_estimate": self.retention_estimate,
            "urgency": self.urgency,
            "sm2_ease_factor": self.sm2_ease_factor
        }


@dataclass
class HabitInsightDTO:
    user_id: int
    habit_score: float  # 0 to 100
    study_streak_days: int
    avg_daily_minutes: float
    peak_focus_window: str
    consistency_rating: str  # EXCELLENT, STEADY, INCONSISTENT, NEEDS_ATTENTION
    key_insight: str
    recommendation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "habit_score": self.habit_score,
            "study_streak_days": self.study_streak_days,
            "avg_daily_minutes": self.avg_daily_minutes,
            "peak_focus_window": self.peak_focus_window,
            "consistency_rating": self.consistency_rating,
            "key_insight": self.key_insight,
            "recommendation": self.recommendation
        }


@dataclass
class MentorInterventionDTO:
    intervention_id: str
    user_id: int
    trigger_type: str  # WEAKNESS_SPIKE, DROP_OFF_WARNING, EXAM_URGENCY, CODING_STAGNATION
    severity: str      # INFO, NOTICE, WARNING, ACTION_REQUIRED
    title: str
    message: str
    suggested_action: str
    action_route: str
    created_at: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intervention_id": self.intervention_id,
            "user_id": self.user_id,
            "trigger_type": self.trigger_type,
            "severity": self.severity,
            "title": self.title,
            "message": self.message,
            "suggested_action": self.suggested_action,
            "action_route": self.action_route,
            "created_at": self.created_at
        }


@dataclass
class PredictiveSuccessDTO:
    user_id: int
    course_completion_prob: float  # 0.0 to 100.0
    exam_readiness_score: float    # 0.0 to 100.0
    interview_readiness_score: float
    certification_prob: float
    top_readiness_factor: str
    primary_bottleneck: str
    predicted_at: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "course_completion_prob": self.course_completion_prob,
            "exam_readiness_score": self.exam_readiness_score,
            "interview_readiness_score": self.interview_readiness_score,
            "certification_prob": self.certification_prob,
            "top_readiness_factor": self.top_readiness_factor,
            "primary_bottleneck": self.primary_bottleneck,
            "predicted_at": self.predicted_at
        }


@dataclass
class AutonomousOverviewDTO:
    user_id: int
    brain_decisions: List[AutonomousDecisionDTO] = field(default_factory=list)
    daily_mission: Optional[DailyMissionDTO] = None
    adaptive_schedule: Optional[AdaptiveScheduleDTO] = None
    revision_queue: List[RevisionItemDTO] = field(default_factory=list)
    habit_insight: Optional[HabitInsightDTO] = None
    active_interventions: List[MentorInterventionDTO] = field(default_factory=list)
    success_forecast: Optional[PredictiveSuccessDTO] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "brain_decisions": [d.to_dict() for d in self.brain_decisions],
            "daily_mission": self.daily_mission.to_dict() if self.daily_mission else None,
            "adaptive_schedule": self.adaptive_schedule.to_dict() if self.adaptive_schedule else None,
            "revision_queue": [r.to_dict() for r in self.revision_queue],
            "habit_insight": self.habit_insight.to_dict() if self.habit_insight else None,
            "active_interventions": [i.to_dict() for i in self.active_interventions],
            "success_forecast": self.success_forecast.to_dict() if self.success_forecast else None
        }
