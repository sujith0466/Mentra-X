"""
Mentra X — Goal Planner & Velocity Calculator (Phase 6 Layer 6)

Calculates required study velocity (lessons/week, study hours/day) given a student's
target deadline and remaining course load. Provides realistic study planning without
hardcoded assumptions.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
import math


class GoalPlanner:
    DEFAULT_HOURS_PER_LESSON = 1.5  # Realistic average study time per lesson

    def calculate_study_velocity(
        self,
        remaining_lessons: int,
        target_deadline_iso: str,
        avg_hours_per_lesson: float = DEFAULT_HOURS_PER_LESSON
    ) -> Dict[str, Any]:
        """
        Computes required completion velocity to meet target deadline.
        Returns velocity metrics and feasibility assessment.
        """
        remaining_lessons = max(0, int(remaining_lessons))
        if remaining_lessons == 0:
            return {
                "status": "COMPLETED",
                "remaining_lessons": 0,
                "required_lessons_per_week": 0.0,
                "required_hours_per_week": 0.0,
                "required_hours_per_day": 0.0,
                "days_remaining": 0,
                "feasibility": "ACHIEVABLE",
                "message": "All lessons completed! You are ready for your assessment."
            }

        try:
            # Parse ISO date string
            cleaned_iso = str(target_deadline_iso).replace("Z", "+00:00")
            if "T" not in cleaned_iso:
                cleaned_iso += "T23:59:59+00:00"
            target_dt = datetime.fromisoformat(cleaned_iso)
            if target_dt.tzinfo is None:
                target_dt = target_dt.replace(tzinfo=timezone.utc)
            
            now_dt = datetime.now(timezone.utc)
            delta = target_dt - now_dt
            days_remaining = max(1, delta.days)
        except Exception:
            # Fallback if parsing fails: assume 30 days
            days_remaining = 30

        weeks_remaining = max(0.14, days_remaining / 7.0)
        lessons_per_week = remaining_lessons / weeks_remaining
        hours_per_week = lessons_per_week * avg_hours_per_lesson
        hours_per_day = (remaining_lessons * avg_hours_per_lesson) / days_remaining

        # Feasibility assessment
        if hours_per_day > 6.0:
            feasibility = "CRITICAL_OVERLOAD"
            msg = f"Target requires {hours_per_day:.1f} hours/day. Consider extending your deadline."
        elif hours_per_day > 3.0:
            feasibility = "CHALLENGING"
            msg = f"Intensive pace required: {lessons_per_week:.1f} lessons/week ({hours_per_day:.1f} hrs/day)."
        else:
            feasibility = "ACHIEVABLE"
            msg = f"Comfortable pace: {lessons_per_week:.1f} lessons/week (~{hours_per_day * 7:.1f} hrs/week)."

        return {
            "status": "ACTIVE",
            "remaining_lessons": remaining_lessons,
            "required_lessons_per_week": round(lessons_per_week, 2),
            "required_hours_per_week": round(hours_per_week, 2),
            "required_hours_per_day": round(hours_per_day, 2),
            "days_remaining": days_remaining,
            "feasibility": feasibility,
            "message": msg
        }
