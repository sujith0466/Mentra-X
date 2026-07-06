"""
Mentra X — Adaptive Pacing & Review Engines (Phase 6 Layer 6)

Contains:
1. FatigueDetector: Monitors real-time session duration, error velocity, and latency degradation
   to identify cognitive burnout and trigger break recommendations or low-intensity review modes.
2. SpacedRepetitionScheduler: Evaluates Ebbinghaus retention decay curves to automate
   spaced repetition review scheduling for previously learned concepts.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import math
from datetime import datetime, timezone, timedelta


@dataclass
class FatigueStatusDTO:
    is_fatigued: bool
    fatigue_level: str  # "NONE" | "MODERATE" | "HIGH" | "CRITICAL"
    recommended_action: str  # "CONTINUE" | "SHORT_BREAK" | "MANDATORY_BREAK" | "SWITCH_TO_LIGHT_REVIEW"
    session_duration_mins: float
    error_velocity: float
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ReviewScheduleDTO:
    concept: str
    current_retention: float
    needs_immediate_review: bool
    recommended_review_in_hours: float
    urgency: str  # "LOW" | "MEDIUM" | "HIGH" | "OVERDUE"
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FatigueDetector:
    def evaluate_fatigue(
        self,
        session_duration_mins: float,
        recent_errors: int = 0,
        response_time_degradation_pct: float = 0.0
    ) -> FatigueStatusDTO:
        """
        Evaluates cognitive fatigue and burnout indicators.
        """
        duration = float(session_duration_mins)
        errors = int(recent_errors)
        deg = float(response_time_degradation_pct)

        error_velocity = errors / max(1.0, duration / 10.0)  # errors per 10 mins

        if duration >= 120.0 or (duration >= 60.0 and errors >= 5) or deg >= 75.0:
            level = "CRITICAL"
            action = "MANDATORY_BREAK"
            rationale = f"Critical cognitive burnout indicators detected (duration: {duration:.0f}m, errors: {errors}, latency +{deg:.0f}%). Mandatory 15-minute break required."
            is_fatigued = True
        elif duration >= 75.0 or (duration >= 45.0 and errors >= 3) or deg >= 40.0:
            level = "HIGH"
            action = "SWITCH_TO_LIGHT_REVIEW"
            rationale = f"High fatigue detected. We recommend pausing challenging new material and switching to light flashcard review."
            is_fatigued = True
        elif duration >= 50.0 or errors >= 2 or deg >= 20.0:
            level = "MODERATE"
            action = "SHORT_BREAK"
            rationale = "Moderate fatigue accumulating. A quick 5-minute stretch break is recommended."
            is_fatigued = True
        else:
            level = "NONE"
            action = "CONTINUE"
            rationale = "Optimal cognitive alertness maintained."
            is_fatigued = False

        return FatigueStatusDTO(
            is_fatigued=is_fatigued,
            fatigue_level=level,
            recommended_action=action,
            session_duration_mins=round(duration, 1),
            error_velocity=round(error_velocity, 2),
            rationale=rationale
        )


class SpacedRepetitionScheduler:
    def calculate_review_schedule(
        self,
        concept: str,
        hours_since_last_review: float,
        initial_mastery: float = 0.80,
        retention_threshold: float = 0.70
    ) -> ReviewScheduleDTO:
        """
        Computes Ebbinghaus retention curve: R = exp(-t / S), where stability S scales with mastery.
        """
        t = max(0.0, float(hours_since_last_review))
        m = max(0.1, min(1.0, float(initial_mastery)))

        # Memory stability S in hours (higher mastery = longer retention stability)
        # E.g. mastery 0.80 -> stability ~ 160 hours (~6.6 days)
        stability_hours = m * 200.0

        retention = math.exp(-t / stability_hours)

        needs_review = retention <= retention_threshold

        if retention < 0.50:
            urgency = "OVERDUE"
            rec_hours = 0.0
            rationale = f"Retention has decayed severely to {retention*100:.0f}%. Immediate review required."
        elif retention <= retention_threshold:
            urgency = "HIGH"
            rec_hours = 0.0
            rationale = f"Retention dropped below threshold ({retention*100:.0f}% <= {retention_threshold*100:.0f}%). Schedule review session now."
        elif retention <= retention_threshold + 0.10:
            urgency = "MEDIUM"
            # Solve for hours remaining until retention hits threshold: t_target = -S * ln(threshold)
            target_t = -stability_hours * math.log(retention_threshold)
            rec_hours = max(0.5, target_t - t)
            rationale = f"Retention is currently {retention*100:.0f}%. Review recommended within {rec_hours:.1f} hours."
        else:
            urgency = "LOW"
            target_t = -stability_hours * math.log(retention_threshold)
            rec_hours = max(1.0, target_t - t)
            rationale = f"Concept memory is stable ({retention*100:.0f}%). Next automated review scheduled in {rec_hours:.0f} hours."

        return ReviewScheduleDTO(
            concept=concept,
            current_retention=round(retention, 3),
            needs_immediate_review=needs_review,
            recommended_review_in_hours=round(rec_hours, 1),
            urgency=urgency,
            rationale=rationale
        )
