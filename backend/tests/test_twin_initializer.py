import unittest
from backend.app import app
from backend.models import db, StudentTwinRecord
from backend.services.twin.twin_initializer import TwinInitializationService
from backend.tests.test_support import SQLiteFixtureMixin

class TestTwinInitializer(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixture()

    def setUp(self):
        # Clear any existing twin for this user before each test to ensure isolation
        with app.app_context():
            twin = StudentTwinRecord.query.filter_by(user_id=self.fixture_ids["student_id"]).first()
            if twin:
                db.session.delete(twin)
                db.session.commit()

    def test_ensure_twin_creates_new(self):
        with app.app_context():
            user_id = self.fixture_ids["student_id"]
            
            # Initial verification
            twin = StudentTwinRecord.query.filter_by(user_id=user_id).first()
            self.assertIsNone(twin)
            
            # Ensure twin creates it
            created_twin = TwinInitializationService.ensure_twin(user_id, "JEE")
            self.assertIsNotNone(created_twin)
            self.assertEqual(created_twin.user_id, user_id)
            self.assertEqual(created_twin.twin_status, 'ACTIVE')

    def test_ensure_twin_returns_existing(self):
        with app.app_context():
            user_id = self.fixture_ids["student_id"]
            
            # Create first time
            first_twin = TwinInitializationService.ensure_twin(user_id, "JEE")
            self.assertIsNotNone(first_twin)
            
            # Call again
            second_twin = TwinInitializationService.ensure_twin(user_id, "JEE")
            self.assertEqual(first_twin.id, second_twin.id)

if __name__ == '__main__':
    unittest.main()
