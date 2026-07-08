"""
Mentra X — Weakness & Strength Intelligence DTOs (Phase 8 Milestone 1)

Enforces strict type safety, explainability, multi-source evidence tracking,
and JSON serialization contracts for Weakness & Strength Intelligence profiles.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import json
from datetime import datetime, timezone


@dataclass
class ConfidenceScoreDTO:
    percentage: str
    score: float
    evidence_count: int
    evidence_sources: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConfidenceScoreDTO":
        if not data:
            return cls(percentage="0.0%", score=0.0, evidence_count=0, evidence_sources=[])
        return cls(
            percentage=str(data.get("percentage", f"{round(float(data.get('score', 0.0)) * 100, 1)}%")),
            score=float(data.get("score", 0.0)),
            evidence_count=int(data.get("evidence_count", 0)),
            evidence_sources=list(data.get("evidence_sources", []))
        )


@dataclass
class ExplainabilityDTO:
    why_detected: str
    evidence_used: str
    prerequisite_caused: str
    how_to_fix: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExplainabilityDTO":
        if not data:
            return cls(why_detected="", evidence_used="", prerequisite_caused="", how_to_fix="")
        return cls(
            why_detected=str(data.get("why_detected", "")),
            evidence_used=str(data.get("evidence_used", "")),
            prerequisite_caused=str(data.get("prerequisite_caused", "")),
            how_to_fix=str(data.get("how_to_fix", ""))
        )


@dataclass
class OpportunityHooksDTO:
    lessons: List[str] = field(default_factory=list)
    videos: List[str] = field(default_factory=list)
    quizzes: List[str] = field(default_factory=list)
    coding_problems: List[str] = field(default_factory=list)
    projects: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OpportunityHooksDTO":
        if not data:
            return cls()
        return cls(
            lessons=list(data.get("lessons", [])),
            videos=list(data.get("videos", [])),
            quizzes=list(data.get("quizzes", [])),
            coding_problems=list(data.get("coding_problems", [])),
            projects=list(data.get("projects", []))
        )


@dataclass
class ProgressTimelineEntryDTO:
    timestamp: str
    state: str  # "Weakness", "Practice", "Recovery", "Mastery"
    mastery_score: float
    trigger_event: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProgressTimelineEntryDTO":
        return cls(
            timestamp=str(data.get("timestamp", "")),
            state=str(data.get("state", "Weakness")),
            mastery_score=float(data.get("mastery_score", 0.0)),
            trigger_event=str(data.get("trigger_event", ""))
        )


@dataclass
class DiagnosedConceptDTO:
    concept_id: str
    title: str
    subject: str
    course: str
    topic: str
    semester: str
    severity: str  # "Mastered", "Learning", "Needs Practice", "At Risk", "Critical"
    mastery_score: float
    decay_coefficient: float
    confidence: ConfidenceScoreDTO
    explainability: ExplainabilityDTO
    opportunity_hooks: OpportunityHooksDTO
    progress_timeline: List[ProgressTimelineEntryDTO] = field(default_factory=list)
    last_updated_date: str = ""
    misconception_type: str = "CONCEPTUAL_GAP"

    def to_dict(self) -> Dict[str, Any]:
        res = asdict(self)
        res["confidence"] = self.confidence.to_dict() if isinstance(self.confidence, ConfidenceScoreDTO) else self.confidence
        res["explainability"] = self.explainability.to_dict() if isinstance(self.explainability, ExplainabilityDTO) else self.explainability
        res["opportunity_hooks"] = self.opportunity_hooks.to_dict() if isinstance(self.opportunity_hooks, OpportunityHooksDTO) else self.opportunity_hooks
        res["progress_timeline"] = [
            t.to_dict() if isinstance(t, ProgressTimelineEntryDTO) else t
            for t in self.progress_timeline
        ]
        return res

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DiagnosedConceptDTO":
        conf = ConfidenceScoreDTO.from_dict(data.get("confidence", {})) if isinstance(data.get("confidence"), dict) else data.get("confidence", ConfidenceScoreDTO.from_dict({}))
        exp = ExplainabilityDTO.from_dict(data.get("explainability", {})) if isinstance(data.get("explainability"), dict) else data.get("explainability", ExplainabilityDTO.from_dict({}))
        hooks = OpportunityHooksDTO.from_dict(data.get("opportunity_hooks", {})) if isinstance(data.get("opportunity_hooks"), dict) else data.get("opportunity_hooks", OpportunityHooksDTO.from_dict({}))
        
        timeline_raw = data.get("progress_timeline", [])
        timeline = [
            ProgressTimelineEntryDTO.from_dict(item) if isinstance(item, dict) else item
            for item in timeline_raw
        ]

        return cls(
            concept_id=str(data.get("concept_id", "")),
            title=str(data.get("title", "")),
            subject=str(data.get("subject", "General")),
            course=str(data.get("course", "General Course")),
            topic=str(data.get("topic", "General Topic")),
            semester=str(data.get("semester", "Semester 1")),
            severity=str(data.get("severity", "Learning")),
            mastery_score=float(data.get("mastery_score", 0.0)),
            decay_coefficient=float(data.get("decay_coefficient", 1.0)),
            confidence=conf,
            explainability=exp,
            opportunity_hooks=hooks,
            progress_timeline=timeline,
            last_updated_date=str(data.get("last_updated_date", "")),
            misconception_type=str(data.get("misconception_type", "CONCEPTUAL_GAP"))
        )


@dataclass
class StrengthConceptDTO:
    concept_id: str
    title: str
    mastery_score: float
    domain: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StrengthConceptDTO":
        return cls(
            concept_id=str(data.get("concept_id", "")),
            title=str(data.get("title", "")),
            mastery_score=float(data.get("mastery_score", 0.0)),
            domain=str(data.get("domain", "General"))
        )


@dataclass
class ImprovingSkillDTO:
    skill_name: str
    improvement_rate: str
    current_mastery: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ImprovingSkillDTO":
        return cls(
            skill_name=str(data.get("skill_name", "")),
            improvement_rate=str(data.get("improvement_rate", "")),
            current_mastery=float(data.get("current_mastery", 0.0))
        )


@dataclass
class MasteredDomainDTO:
    domain_name: str
    average_mastery: float
    concepts_mastered_count: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MasteredDomainDTO":
        return cls(
            domain_name=str(data.get("domain_name", "")),
            average_mastery=float(data.get("average_mastery", 0.0)),
            concepts_mastered_count=int(data.get("concepts_mastered_count", 0))
        )


@dataclass
class StrengthIntelligenceDTO:
    last_analyzed_at: str
    strongest_concepts: List[StrengthConceptDTO] = field(default_factory=list)
    fastest_improving_skills: List[ImprovingSkillDTO] = field(default_factory=list)
    mastered_domains: List[MasteredDomainDTO] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "last_analyzed_at": self.last_analyzed_at,
            "strongest_concepts": [c.to_dict() if isinstance(c, StrengthConceptDTO) else c for c in self.strongest_concepts],
            "fastest_improving_skills": [s.to_dict() if isinstance(s, ImprovingSkillDTO) else s for s in self.fastest_improving_skills],
            "mastered_domains": [d.to_dict() if isinstance(d, MasteredDomainDTO) else d for d in self.mastered_domains]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StrengthIntelligenceDTO":
        if not data:
            return cls(last_analyzed_at=datetime.now(timezone.utc).isoformat())
        return cls(
            last_analyzed_at=str(data.get("last_analyzed_at", "")),
            strongest_concepts=[
                StrengthConceptDTO.from_dict(c) if isinstance(c, dict) else c
                for c in data.get("strongest_concepts", [])
            ],
            fastest_improving_skills=[
                ImprovingSkillDTO.from_dict(s) if isinstance(s, dict) else s
                for s in data.get("fastest_improving_skills", [])
            ],
            mastered_domains=[
                MasteredDomainDTO.from_dict(d) if isinstance(d, dict) else d
                for d in data.get("mastered_domains", [])
            ]
        )


@dataclass
class WeaknessIntelligenceProfileDTO:
    user_id: int
    last_diagnosed_at: str
    weaknesses: Dict[str, DiagnosedConceptDTO] = field(default_factory=dict)
    strengths: StrengthIntelligenceDTO = field(default_factory=lambda: StrengthIntelligenceDTO(last_analyzed_at=""))
    summary_metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "last_diagnosed_at": self.last_diagnosed_at,
            "weaknesses": {
                k: v.to_dict() if isinstance(v, DiagnosedConceptDTO) else v
                for k, v in self.weaknesses.items()
            },
            "strengths": self.strengths.to_dict() if isinstance(self.strengths, StrengthIntelligenceDTO) else self.strengths,
            "summary_metrics": self.summary_metrics
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WeaknessIntelligenceProfileDTO":
        if not data:
            return cls(user_id=0, last_diagnosed_at="")
        
        weaknesses_raw = data.get("weaknesses", {})
        weaknesses = {
            k: DiagnosedConceptDTO.from_dict(v) if isinstance(v, dict) else v
            for k, v in weaknesses_raw.items()
        }
        
        strengths_raw = data.get("strengths", {})
        strengths = StrengthIntelligenceDTO.from_dict(strengths_raw) if isinstance(strengths_raw, dict) else strengths_raw

        return cls(
            user_id=int(data.get("user_id", 0)),
            last_diagnosed_at=str(data.get("last_diagnosed_at", "")),
            weaknesses=weaknesses,
            strengths=strengths,
            summary_metrics=data.get("summary_metrics", {})
        )

    @classmethod
    def from_json(cls, json_str: str) -> "WeaknessIntelligenceProfileDTO":
        if not json_str:
            return cls(user_id=0, last_diagnosed_at="")
        try:
            data = json.loads(json_str)
            return cls.from_dict(data)
        except Exception:
            return cls(user_id=0, last_diagnosed_at="")
