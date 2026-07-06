"""
Mentra X — Adaptive Learning Intelligence DTOs (Data Transfer Objects)

Enforces strict type safety and JSON serialization contracts between Phase 6
intelligence engines, Mastra swarm tools, and enterprise observability logging.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import json


@dataclass
class AvoidanceConstraintsDTO:
    levels_to_avoid: List[int] = field(default_factory=list)
    analogies_to_avoid: List[str] = field(default_factory=list)
    analogies_that_worked: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AvoidanceConstraintsDTO":
        if not data:
            return cls()
        return cls(
            levels_to_avoid=data.get("levels_to_avoid", []),
            analogies_to_avoid=data.get("analogies_to_avoid", []),
            analogies_that_worked=data.get("analogies_that_worked", [])
        )


@dataclass
class TutorDecisionDTO:
    level: int
    level_name: str
    strategy: str
    rationale: str
    constraints: AvoidanceConstraintsDTO
    adjusted_mastery: float = 0.0

    def __post_init__(self):
        if not (1 <= self.level <= 5):
            raise ValueError(f"Teaching level must be between 1 and 5, got {self.level}")

    def to_dict(self) -> Dict[str, Any]:
        res = asdict(self)
        res["constraints"] = self.constraints.to_dict() if isinstance(self.constraints, AvoidanceConstraintsDTO) else self.constraints
        return res

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TutorDecisionDTO":
        constraints_data = data.get("constraints", {})
        constraints = AvoidanceConstraintsDTO.from_dict(constraints_data) if isinstance(constraints_data, dict) else constraints_data
        return cls(
            level=int(data.get("level", 1)),
            level_name=data.get("level_name", "Direct"),
            strategy=data.get("strategy", "Concise, precise"),
            rationale=data.get("rationale", ""),
            constraints=constraints,
            adjusted_mastery=float(data.get("adjusted_mastery", 0.0))
        )


@dataclass
class PersonalizationBundleDTO:
    selected_level: int
    selected_style: str
    system_prompt: str
    avoidance_constraints: Dict[str, Any]
    teaching_rationale: str
    level_name: str

    def __post_init__(self):
        if not (1 <= self.selected_level <= 5):
            raise ValueError(f"selected_level must be between 1 and 5, got {self.selected_level}")
        valid_styles = {"Visual", "Mathematical", "Narrative", "Default"}
        if self.selected_style not in valid_styles:
            # Normalize unknown styles to Default without failing
            self.selected_style = "Default"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PersonalizationBundleDTO":
        return cls(
            selected_level=int(data.get("selected_level", 1)),
            selected_style=data.get("selected_style", "Default"),
            system_prompt=data.get("system_prompt", ""),
            avoidance_constraints=data.get("avoidance_constraints", {}),
            teaching_rationale=data.get("teaching_rationale", ""),
            level_name=data.get("level_name", "Direct")
        )
