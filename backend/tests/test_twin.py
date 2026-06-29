import sys
import unittest
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import app
from backend.models import db, User, StudentTwinRecord, TwinKnowledgeStateRecord
from backend.services.twin.concept_resolver import ConceptResolver
from backend.services.twin.twin_builder import build_initial_twin
from backend.services.twin.twin_health import compute_and_store_health
from backend.services.twin.twin_mutator import mutate_knowledge
from backend.tests.test_support import SQLiteFixtureMixin


class TestTwinCoreServices(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()
        
    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixture()
        
    def test_concept_resolver(self):
        concept = ConceptResolver.resolve_from_quiz("  Python Basics  ")
        self.assertEqual(concept, "python_basics")
        
    def test_twin_builder_and_health(self):
        with app.app_context():
            # Get the seed user for this fixture
            user_id = self.fixture_ids["student_id"]
            
            # 1. Test Builder
            twin = build_initial_twin(user_id, "JEE")
            self.assertIsNotNone(twin)
            self.assertEqual(twin.user_id, user_id)
            self.assertEqual(twin.twin_version, 1)
            self.assertEqual(twin.twin_status, 'ACTIVE')
            self.assertEqual(twin.exam_track, 'JEE')
            
            # Check JSON fields parsed properly
            academic = json.loads(twin.academic_state)
            self.assertIn('xp_total', academic)
            
            learning_dna = json.loads(twin.learning_dna)
            self.assertEqual(learning_dna.get('preferred_style'), 'Visual')
            
            # 2. Test Mutator (optimistic locking and log)
            success = mutate_knowledge(user_id, "python_basics", 0.85, "quiz_pass")
            self.assertTrue(success)
            
            # Verify version increment
            twin_updated = db.session.get(StudentTwinRecord, twin.id)
            self.assertEqual(twin_updated.twin_version, 2)
            
            # Verify knowledge state created
            ks = TwinKnowledgeStateRecord.query.filter_by(twin_id=twin.id, concept_id="python_basics").first()
            self.assertIsNotNone(ks)
            self.assertEqual(ks.mastery_score, 0.85)
            
            # 3. Test Health
            health = compute_and_store_health(twin.id)
            self.assertGreater(health, 0.0)
            twin_final = db.session.get(StudentTwinRecord, twin.id)
            self.assertEqual(twin_final.twin_health, health)
