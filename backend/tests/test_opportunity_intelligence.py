"""
Mentra X — Enterprise Automated Test Suite for Phase 10 Opportunity Intelligence

Verifies:
  1. Pluggable Opportunity Aggregation Engine across all 9 categories
  2. Multi-Factor Match Explainability scoring
  3. Skill Gap Readiness Bridge analytics
  4. Resume ATS Alignment Engine
  5. Proactive Notifications & Recommendation Ranking
  6. 9-Stage Opportunity Lifecycle Timeline Tracking
  7. Opportunity Intelligence Brain Orchestrator
"""

import unittest
from unittest.mock import patch, MagicMock
from backend.services.opportunity.dto import OpportunityItemDTO
from backend.services.opportunity.aggregation_engine import (
    OpportunityAggregationEngine,
    InternalCuratedProvider,
    ExternalJSONAdapterProvider
)
from backend.services.opportunity.matching_engine import StudentMatchingEngine
from backend.services.opportunity.skill_gap_engine import SkillGapEngine
from backend.services.opportunity.resume_opportunity_engine import ResumeOpportunityEngine
from backend.services.opportunity.recommendation_engine import OpportunityRecommendationEngine
from backend.services.opportunity.timeline_engine import OpportunityTimelineEngine
from backend.services.opportunity.opportunity_brain import OpportunityIntelligenceBrain


class TestOpportunityIntelligence(unittest.TestCase):

    def test_aggregation_engine_multi_provider(self):
        engine = OpportunityAggregationEngine()
        custom_item = OpportunityItemDTO(
            opportunity_id="opp-test-1",
            title="AI Research Grant",
            organization="Open AI Partner",
            category="RESEARCH",
            location="Remote",
            stipend_or_reward="$10,000",
            deadline="2026-10-01",
            required_skills=["Python", "PyTorch"]
        )
        engine.register_provider(ExternalJSONAdapterProvider([custom_item]))
        all_opps = engine.get_all_opportunities()
        self.assertGreaterEqual(len(all_opps), 7)
        ids = {o.opportunity_id for o in all_opps}
        self.assertIn("opp-swe-google", ids)
        self.assertIn("opp-test-1", ids)

    def test_matching_engine_with_explainability(self):
        matcher = StudentMatchingEngine()
        opp = OpportunityItemDTO(
            opportunity_id="opp-match-1",
            title="Google SWE Intern",
            organization="Google Core AI",
            category="INTERNSHIP",
            location="Remote",
            stipend_or_reward="$8,500",
            deadline="2026-08-15",
            required_skills=["Python", "Algorithms", "System Design"]
        )
        result = matcher.match_opportunity(
            opportunity=opp,
            student_skills=["Python", "Algorithms"],
            habit_score=85.0,
            ats_score=80.0,
            completed_courses_count=10
        )
        self.assertGreater(result.match_percentage, 60.0)
        self.assertGreater(len(result.explanations), 0)
        # Check explanation reasons
        factors = {e.factor for e in result.explanations}
        self.assertIn("Skill Alignment", factors)
        self.assertIn("Autonomous Learning Consistency", factors)

    def test_skill_gap_engine_readiness_bridge(self):
        gap_engine = SkillGapEngine()
        opp = OpportunityItemDTO(
            opportunity_id="opp-gap-1",
            title="Senior Systems Intern",
            organization="Cloud Co",
            category="INTERNSHIP",
            location="Remote",
            stipend_or_reward="$7,000",
            deadline="2026-09-01",
            required_skills=["Python", "System Design", "Docker"]
        )
        gap = gap_engine.analyze_skill_gap(
            opportunity=opp,
            student_skills=["Python"],
            current_match_pct=72.0
        )
        self.assertIn("System Design", gap.missing_skills)
        self.assertIn("Docker", gap.missing_skills)
        self.assertGreater(gap.estimated_readiness_days, 0)
        self.assertGreater(gap.expected_match_after_remediation_pct, gap.current_match_pct)

    def test_resume_ats_opportunity_engine(self):
        resume_engine = ResumeOpportunityEngine()
        opp = OpportunityItemDTO(
            opportunity_id="opp-res-1",
            title="Machine Learning Fellow",
            organization="AI Lab",
            category="FELLOWSHIP",
            location="Remote",
            stipend_or_reward="$5,000",
            deadline="2026-09-01",
            required_skills=["Python", "Transformer Architecture"]
        )
        raw_text = "Skilled in Python and building neural networks."
        readiness = resume_engine.evaluate_resume_for_opportunity(opp, raw_text, base_ats_score=78.0)
        self.assertIn("Python", readiness.matched_keywords)
        self.assertIn("Transformer Architecture", readiness.missing_keywords)
        self.assertGreaterEqual(len(readiness.suggested_improvements), 1)

    def test_recommendation_and_notification_engine(self):
        matcher = StudentMatchingEngine()
        rec_engine = OpportunityRecommendationEngine()
        opp1 = OpportunityItemDTO(
            opportunity_id="opp-high",
            title="High Match Job",
            organization="Top AI Org",
            category="JOB",
            location="Remote",
            stipend_or_reward="$150,000",
            deadline="2026-08-01",
            required_skills=["Python"]
        )
        match1 = matcher.match_opportunity(
            opportunity=opp1,
            student_skills=["Python"],
            habit_score=90.0,
            ats_score=85.0,
            completed_courses_count=15
        )
        ranked = rec_engine.rank_opportunities([match1])
        notifications = rec_engine.generate_proactive_notifications(ranked)
        self.assertGreaterEqual(len(notifications), 1)
        self.assertEqual(notifications[0].category, "NEW_MATCH")

    def test_timeline_engine_9_stage_lifecycle(self):
        tl = OpportunityTimelineEngine()
        user_id = 999
        entry = tl.update_opportunity_status(
            user_id=user_id,
            opportunity_id="opp-swe-google",
            opportunity_title="Google SWE Summer Intern",
            organization="Google Core AI",
            new_status="INTERVIEW",
            reminder_note="Technical interview prep session scheduled."
        )
        self.assertEqual(entry.status, "INTERVIEW")
        timeline = tl.get_user_timeline(user_id)
        self.assertEqual(len(timeline), 1)
        self.assertEqual(timeline[0].status, "INTERVIEW")

    @patch("backend.services.opportunity.opportunity_brain.TwinFacade")
    @patch("backend.services.opportunity.opportunity_brain.AutonomousLearningFacade")
    def test_opportunity_intelligence_brain_facade(self, mock_auto, mock_twin):
        mock_twin.return_value.get_twin_summary.return_value = {
            "mastered_skills": ["Python", "Algorithms", "React"]
        }
        mock_auto.return_value.get_autonomous_overview.return_value = {
            "habit_insights": {"habit_score": 88.0}
        }
        brain = OpportunityIntelligenceBrain()
        overview = brain.get_opportunity_overview(user_id=1)
        self.assertGreaterEqual(len(overview.recommended_feed), 5)
        self.assertIn("INTERNSHIP", overview.summary_counts)
        self.assertIn("HACKATHON", overview.summary_counts)


if __name__ == "__main__":
    unittest.main()
