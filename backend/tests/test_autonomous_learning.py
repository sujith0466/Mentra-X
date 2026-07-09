"""
Mentra X — Phase 9 Autonomous Learning Intelligence Test Suite

Verifies:
- Autonomous Learning Brain Engine
- Daily Mission Generator
- Adaptive Schedule Planner
- Spaced Repetition Revision Engine
- Habit Intelligence Engine
- Proactive Intervention Engine
- Predictive Success Engine
- Autonomous Learning Facade & API contract
"""

import unittest
from backend.services.autonomous.brain_engine import AutonomousBrainEngine
from backend.services.autonomous.mission_generator import DailyMissionGenerator
from backend.services.autonomous.schedule_planner import AdaptiveSchedulePlanner
from backend.services.autonomous.revision_engine import AutonomousRevisionEngine
from backend.services.autonomous.habit_engine import HabitIntelligenceEngine
from backend.services.autonomous.intervention_engine import ProactiveInterventionEngine
from backend.services.autonomous.predictive_engine import PredictiveSuccessEngine
from backend.services.autonomous.autonomous_facade import AutonomousLearningFacade


class TestAutonomousLearningIntelligence(unittest.TestCase):

    def setUp(self):
        self.brain = AutonomousBrainEngine()
        self.mission_gen = DailyMissionGenerator(self.brain)
        self.schedule_planner = AdaptiveSchedulePlanner(self.mission_gen)
        self.revision_engine = AutonomousRevisionEngine()
        self.habit_engine = HabitIntelligenceEngine()
        self.intervention_engine = ProactiveInterventionEngine()
        self.predictive_engine = PredictiveSuccessEngine()
        self.facade = AutonomousLearningFacade()
        self.user_id = 101

    def test_01_brain_engine_decisions(self):
        decisions = self.brain.make_decisions(self.user_id)
        self.assertIsInstance(decisions, list)
        self.assertGreater(len(decisions), 0)
        for dec in decisions:
            self.assertEqual(dec.user_id, self.user_id)
            self.assertIn(dec.action_type, [
                "LEARN_NEW", "REVISE_CONCEPT", "SOLVE_CODING",
                "WATCH_LECTURE", "REMEDIATE_WEAKNESS", "REST_RECOVERY"
            ])

    def test_02_daily_mission_generator(self):
        mission = self.mission_gen.generate_mission(self.user_id)
        self.assertEqual(mission.user_id, self.user_id)
        self.assertGreater(len(mission.daily_tasks), 0)
        self.assertGreater(mission.total_xp, 0)
        self.assertIn("Missions", mission.weekly_mission)

    def test_03_adaptive_schedule_planner(self):
        schedule = self.schedule_planner.generate_schedule(self.user_id)
        self.assertEqual(schedule.user_id, self.user_id)
        self.assertGreater(len(schedule.blocks), 0)
        self.assertGreaterEqual(schedule.workload_score, 0.0)
        self.assertLessEqual(schedule.fatigue_index, 1.0)

    def test_04_revision_engine(self):
        revisions = self.revision_engine.get_revision_queue(self.user_id)
        self.assertIsInstance(revisions, list)
        self.assertGreater(len(revisions), 0)
        for item in revisions:
            self.assertIn(item.urgency, ["CRITICAL", "OVERDUE", "SCHEDULED", "UPCOMING"])

    def test_05_habit_engine(self):
        habit = self.habit_engine.analyze_habits(self.user_id)
        self.assertEqual(habit.user_id, self.user_id)
        self.assertGreaterEqual(habit.habit_score, 0.0)
        self.assertLessEqual(habit.habit_score, 100.0)
        self.assertIn(habit.consistency_rating, ["EXCELLENT", "STEADY", "INCONSISTENT", "NEEDS_ATTENTION"])

    def test_06_intervention_engine(self):
        interventions = self.intervention_engine.check_interventions(self.user_id)
        self.assertIsInstance(interventions, list)
        self.assertGreater(len(interventions), 0)
        for alert in interventions:
            self.assertIn(alert.trigger_type, ["WEAKNESS_SPIKE", "DROP_OFF_WARNING", "EXAM_URGENCY", "CODING_STAGNATION"])

    def test_07_predictive_success_engine(self):
        pred = self.predictive_engine.forecast_success(self.user_id)
        self.assertEqual(pred.user_id, self.user_id)
        self.assertGreaterEqual(pred.course_completion_prob, 0.0)
        self.assertLessEqual(pred.course_completion_prob, 100.0)

    def test_08_autonomous_facade_overview(self):
        res = self.facade.get_autonomous_overview(self.user_id)
        self.assertTrue(res["success"])
        data = res["data"]
        self.assertIn("brain_decisions", data)
        self.assertIn("daily_mission", data)
        self.assertIn("adaptive_schedule", data)
        self.assertIn("revision_queue", data)
        self.assertIn("habit_insight", data)
        self.assertIn("active_interventions", data)
        self.assertIn("success_forecast", data)


if __name__ == "__main__":
    unittest.main()
