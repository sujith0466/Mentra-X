"""
Mentra X — Unit & Integration Tests for Phase 8 Milestone 1 (Weakness Diagnostic Engine)

Tests DTO serialization, severity thresholds, multi-source evidence aggregation,
explainability generation, confidence calculation, strength intelligence tracking,
and database persistence in StudentTwinRecord.metadata_json.
"""

import sys
import unittest
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import app
from backend.models import db, StudentTwinRecord, TwinKnowledgeStateRecord, TwinMutationLogRecord
from backend.services.adaptive.weakness_dto import (
    WeaknessIntelligenceProfileDTO, DiagnosedConceptDTO, StrengthIntelligenceDTO,
    ConfidenceScoreDTO, ExplainabilityDTO, OpportunityHooksDTO, ProgressTimelineEntryDTO
)
from backend.services.adaptive.weakness_diagnostic_engine import WeaknessDiagnosticEngine
from backend.services.twin.twin_builder import build_initial_twin
from backend.tests.test_support import SQLiteFixtureMixin


class TestWeaknessDiagnosticDTOs(unittest.TestCase):
    def test_dto_roundtrip(self):
        conf = ConfidenceScoreDTO(percentage="88.0%", score=0.88, evidence_count=5, evidence_sources=["QUIZ", "CODING"])
        exp = ExplainabilityDTO(
            why_detected="Low quiz scores",
            evidence_used="3 failed quizzes",
            prerequisite_caused="algebra_basics",
            how_to_fix="Review algebra"
        )
        hooks = OpportunityHooksDTO(lessons=["Lesson 1"], videos=["Video 1"])
        timeline = [ProgressTimelineEntryDTO(timestamp="2026-07-07T10:00:00Z", state="Weakness", mastery_score=0.45, trigger_event="Quiz failure")]
        
        concept = DiagnosedConceptDTO(
            concept_id="calculus_integration",
            title="Calculus Integration",
            subject="Mathematics",
            course="JEE Calculus",
            topic="Integration",
            semester="Semester 2",
            severity="At Risk",
            mastery_score=0.45,
            decay_coefficient=1.2,
            confidence=conf,
            explainability=exp,
            opportunity_hooks=hooks,
            progress_timeline=timeline,
            last_updated_date="2026-07-07",
            misconception_type="CONCEPTUAL_GAP"
        )
        
        data = concept.to_dict()
        self.assertEqual(data["concept_id"], "calculus_integration")
        self.assertEqual(data["confidence"]["percentage"], "88.0%")
        self.assertEqual(data["progress_timeline"][0]["state"], "Weakness")
        
        restored = DiagnosedConceptDTO.from_dict(data)
        self.assertEqual(restored.concept_id, "calculus_integration")
        self.assertEqual(restored.confidence.score, 0.88)
        self.assertEqual(restored.progress_timeline[0].trigger_event, "Quiz failure")

    def test_profile_json_serialization(self):
        profile = WeaknessIntelligenceProfileDTO(
            user_id=101,
            last_diagnosed_at="2026-07-07T10:00:00Z",
            weaknesses={},
            strengths=StrengthIntelligenceDTO(last_analyzed_at="2026-07-07T10:00:00Z"),
            summary_metrics={"total_weaknesses_count": 0}
        )
        json_str = profile.to_json()
        self.assertIn("user_id", json_str)
        
        restored = WeaknessIntelligenceProfileDTO.from_json(json_str)
        self.assertEqual(restored.user_id, 101)


class TestWeaknessDiagnosticEngine(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()
        
    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixture()

    def setUp(self):
        self.engine = WeaknessDiagnosticEngine()

    def test_severity_classification(self):
        self.assertEqual(self.engine._get_severity(0.90), "Mastered")
        self.assertEqual(self.engine._get_severity(0.85), "Mastered")
        self.assertEqual(self.engine._get_severity(0.75), "Learning")
        self.assertEqual(self.engine._get_severity(0.60), "Needs Practice")
        self.assertEqual(self.engine._get_severity(0.45), "At Risk")
        self.assertEqual(self.engine._get_severity(0.20), "Critical")

    def test_domain_mapping(self):
        self.assertEqual(self.engine._map_domain("python_syntax"), "Computer Science")
        self.assertEqual(self.engine._map_domain("calculus_integration"), "Mathematics")
        self.assertEqual(self.engine._map_domain("quantum_physics"), "Physics")
        self.assertEqual(self.engine._map_domain("organic_chemistry"), "Chemistry")

    def test_opportunity_hooks_generation(self):
        hooks = self.engine._generate_hooks("recursion", "Computer Science")
        self.assertGreater(len(hooks.lessons), 0)
        self.assertGreater(len(hooks.videos), 0)
        self.assertIn("Recursion", hooks.lessons[0])

    def test_diagnose_student_with_fixture(self):
        with app.app_context():
            user_id = self.fixture_ids["student_id"]
            
            # Ensure twin exists
            twin = build_initial_twin(user_id, "JEE")
            self.assertIsNotNone(twin)
            
            # Add a knowledge state with low mastery to simulate weakness
            ks = TwinKnowledgeStateRecord.query.filter_by(twin_id=twin.id, concept_id="calculus_integration").first()
            if not ks:
                ks = TwinKnowledgeStateRecord(
                    twin_id=twin.id,
                    concept_id="calculus_integration",
                    mastery_score=0.35,
                    decay_coefficient=1.3,
                    mistake_count=4
                )
                db.session.add(ks)
            else:
                ks.mastery_score = 0.35
                ks.mistake_count = 4
            db.session.commit()

            # Execute diagnosis
            profile = self.engine.diagnose_student(user_id)
            self.assertIsNotNone(profile)
            self.assertEqual(profile.user_id, user_id)
            self.assertIn("calculus_integration", profile.weaknesses)
            
            weakness = profile.weaknesses["calculus_integration"]
            self.assertEqual(weakness.severity, "Critical")
            self.assertGreaterEqual(weakness.confidence.score, 0.65)
            self.assertIn("TWIN_HISTORY", weakness.confidence.evidence_sources)
            self.assertGreater(len(weakness.opportunity_hooks.lessons), 0)
            self.assertGreaterEqual(len(weakness.progress_timeline), 1)
            self.assertEqual(weakness.progress_timeline[-1].state, "Weakness")
            
            # Verify saved into metadata_json
            twin_updated = StudentTwinRecord.query.filter_by(user_id=user_id).first()
            self.assertIsNotNone(twin_updated.metadata_json)
            meta = json.loads(twin_updated.metadata_json)
            self.assertIn("weakness_intelligence_profile", meta)
            self.assertEqual(meta["weakness_intelligence_profile"]["user_id"], user_id)

            # Verify audit log recorded
            log = TwinMutationLogRecord.query.filter_by(user_id=user_id, mutation_type="WEAKNESS_DIAGNOSED").first()
            self.assertIsNotNone(log)
            self.assertEqual(log.agent_name, "WeaknessDiagnosticEngine")


if __name__ == "__main__":
    unittest.main()
