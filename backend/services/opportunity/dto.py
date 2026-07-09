"""
Mentra X — Opportunity Intelligence DTOs (Phase 10)

Defines clean, serializable Data Transfer Objects for:
- Opportunities across 9 categories
- Multi-factor Match Explainability
- Skill Gap & Readiness Bridge
- ATS Resume Alignment
- 9-Stage Opportunity Lifecycle Tracking
- Proactive Opportunity Notifications
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class OpportunityItemDTO:
    opportunity_id: str
    title: str
    organization: str
    category: str  # INTERNSHIP, HACKATHON, JOB, SCHOLARSHIP, CERTIFICATION, FELLOWSHIP, RESEARCH, WORKSHOP, COMPETITION
    location: str
    stipend_or_reward: str
    deadline: str
    required_skills: List[str] = field(default_factory=list)
    description: str = ""
    external_url: str = ""
    source_provider: str = "InternalCuratedProvider"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "opportunity_id": self.opportunity_id,
            "title": self.title,
            "organization": self.organization,
            "category": self.category,
            "location": self.location,
            "stipend_or_reward": self.stipend_or_reward,
            "deadline": self.deadline,
            "required_skills": self.required_skills,
            "description": self.description,
            "external_url": self.external_url,
            "source_provider": self.source_provider
        }


@dataclass
class MatchExplanationDTO:
    factor: str
    impact: str  # POSITIVE, NEGATIVE, NEUTRAL
    detail: str
    score_delta: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "factor": self.factor,
            "impact": self.impact,
            "detail": self.detail,
            "score_delta": self.score_delta
        }


@dataclass
class SkillGapDTO:
    opportunity_id: str
    current_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    learning_path_steps: List[str] = field(default_factory=list)
    estimated_readiness_days: int = 0
    current_match_pct: float = 0.0
    expected_match_after_remediation_pct: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "opportunity_id": self.opportunity_id,
            "current_skills": self.current_skills,
            "missing_skills": self.missing_skills,
            "learning_path_steps": self.learning_path_steps,
            "estimated_readiness_days": self.estimated_readiness_days,
            "current_match_pct": self.current_match_pct,
            "expected_match_after_remediation_pct": self.expected_match_after_remediation_pct
        }


@dataclass
class ResumeReadinessDTO:
    opportunity_id: str
    ats_score: float  # 0 to 100
    matched_keywords: List[str] = field(default_factory=list)
    missing_keywords: List[str] = field(default_factory=list)
    suggested_improvements: List[str] = field(default_factory=list)
    missing_projects_note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "opportunity_id": self.opportunity_id,
            "ats_score": self.ats_score,
            "matched_keywords": self.matched_keywords,
            "missing_keywords": self.missing_keywords,
            "suggested_improvements": self.suggested_improvements,
            "missing_projects_note": self.missing_projects_note
        }


@dataclass
class MatchedOpportunityDTO:
    opportunity: OpportunityItemDTO
    match_percentage: float  # 0 to 100
    readiness_level: str     # IMMEDIATE_READY, NEAR_READY, TARGET_GOAL
    explanations: List[MatchExplanationDTO] = field(default_factory=list)
    skill_gap: Optional[SkillGapDTO] = None
    resume_readiness: Optional[ResumeReadinessDTO] = None
    lifecycle_status: str = "RECOMMENDED"  # RECOMMENDED, SAVED, INTERESTED, APPLIED, INTERVIEW, ACCEPTED, REJECTED, COMPLETED, EXPIRED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "opportunity": self.opportunity.to_dict(),
            "match_percentage": self.match_percentage,
            "readiness_level": self.readiness_level,
            "explanations": [e.to_dict() for e in self.explanations],
            "skill_gap": self.skill_gap.to_dict() if self.skill_gap else None,
            "resume_readiness": self.resume_readiness.to_dict() if self.resume_readiness else None,
            "lifecycle_status": self.lifecycle_status
        }


@dataclass
class TimelineEntryDTO:
    entry_id: str
    user_id: int
    opportunity_id: str
    opportunity_title: str
    organization: str
    status: str  # RECOMMENDED, SAVED, INTERESTED, APPLIED, INTERVIEW, ACCEPTED, REJECTED, COMPLETED, EXPIRED
    updated_at: str
    reminder_note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "user_id": self.user_id,
            "opportunity_id": self.opportunity_id,
            "opportunity_title": self.opportunity_title,
            "organization": self.organization,
            "status": self.status,
            "updated_at": self.updated_at,
            "reminder_note": self.reminder_note
        }


@dataclass
class OpportunityNotificationDTO:
    notification_id: str
    title: str
    message: str
    category: str  # NEW_MATCH, DEADLINE_URGENT, RESUME_TIP, SKILL_GAP_CLOSED
    action_url: str
    created_at: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "notification_id": self.notification_id,
            "title": self.title,
            "message": self.message,
            "category": self.category,
            "action_url": self.action_url,
            "created_at": self.created_at
        }


@dataclass
class OpportunityOverviewDTO:
    user_id: int
    recommended_feed: List[MatchedOpportunityDTO] = field(default_factory=list)
    timeline: List[TimelineEntryDTO] = field(default_factory=list)
    notifications: List[OpportunityNotificationDTO] = field(default_factory=list)
    summary_counts: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "recommended_feed": [m.to_dict() for m in self.recommended_feed],
            "timeline": [t.to_dict() for t in self.timeline],
            "notifications": [n.to_dict() for n in self.notifications],
            "summary_counts": self.summary_counts
        }
