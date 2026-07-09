"""
Mentra X — Daily Mission Generator (Phase 9 Milestone 2)

Transforms autonomous brain decisions into structured, gamified Daily Missions,
Weekly Focus goals, and Monthly Career Milestones.
"""

import uuid
from datetime import datetime, timezone
from typing import List
from backend.services.autonomous.dto import (
    DailyMissionDTO, MissionTaskDTO, AutonomousDecisionDTO
)
from backend.services.autonomous.brain_engine import AutonomousBrainEngine


class DailyMissionGenerator:
    """
    Synthesizes actionable daily missions from AI Brain decisions.
    """

    def __init__(self, brain_engine: AutonomousBrainEngine = None):
        self.brain_engine = brain_engine or AutonomousBrainEngine()

    def generate_mission(self, user_id: int) -> DailyMissionDTO:
        decisions = self.brain_engine.make_decisions(user_id)
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        tasks: List[MissionTaskDTO] = []
        total_duration = 0
        total_xp = 0

        for i, dec in enumerate(decisions, 1):
            category_map = {
                "REMEDIATE_WEAKNESS": "REMEDIATION",
                "REVISE_CONCEPT": "REVISION",
                "SOLVE_CODING": "PROBLEM_SOLVING",
                "LEARN_NEW": "NEW_CONCEPT",
                "WATCH_LECTURE": "LECTURE"
            }
            category = category_map.get(dec.action_type, "NEW_CONCEPT")

            # Assign XP reward based on priority & duration
            xp = 100 if dec.priority == "HIGH" else 60

            action_url = "/student/my-courses"
            if category == "PROBLEM_SOLVING":
                action_url = "/student/coding-arena"
            elif category == "REMEDIATION":
                action_url = "/student/weakness-intelligence"
            elif category == "REVISION":
                action_url = "/student/notes"

            task = MissionTaskDTO(
                task_id=f"mission-{today_str}-{i}",
                title=f"{dec.action_type.replace('_', ' ').title()}: {dec.target_concept}",
                category=category,
                concept=dec.target_concept,
                duration_mins=dec.estimated_duration_mins,
                xp_reward=xp,
                completed=False,
                action_url=action_url
            )
            tasks.append(task)
            total_duration += dec.estimated_duration_mins
            total_xp += xp

        weekly_mission = "Complete 15 Core AI & Algorithms Missions with >85% Quiz Retention"
        monthly_goal = "Reach Advanced Student Level & Verify Technical Placement Readiness"

        return DailyMissionDTO(
            user_id=user_id,
            mission_date=today_str,
            daily_tasks=tasks,
            weekly_mission=weekly_mission,
            monthly_goal=monthly_goal,
            completion_percentage=0.0,
            total_duration_mins=total_duration,
            total_xp=total_xp
        )
