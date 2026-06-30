import unittest
from backend.app import app
from backend.models import db, StudentTwinRecord
from backend.tests.test_support import SQLiteFixtureMixin

class TestTwinAPI(SQLiteFixtureMixin, unittest.TestCase):
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

    def test_unauthorized_access(self):
        # API requires login
        fresh_client = app.test_client()
        response = fresh_client.get('/api/v1/twin/profile')
        self.assertEqual(response.status_code, 401)
        
        response = fresh_client.get('/api/v1/twin/health')
        self.assertEqual(response.status_code, 401)
        
        response = fresh_client.post('/api/v1/twin/initialize')
        self.assertEqual(response.status_code, 401)

    def test_initialize_and_profile_api(self):
        self.login_student(self.client)
        
        # 1. Profile before initialization should return 404
        response = self.client.get('/api/v1/twin/profile')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Twin not initialized", response.json['message'])
        
        # 2. Initialize twin
        response = self.client.post('/api/v1/twin/initialize')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertEqual(response.json['twin_status'], 'ACTIVE')
        self.assertEqual(response.json['twin_version'], 1)
        
        # 3. Fetch profile after initialization
        response = self.client.get('/api/v1/twin/profile')
        self.assertEqual(response.status_code, 200)
        profile = response.json
        self.assertEqual(profile['twin_version'], 1)
        self.assertEqual(profile['exam_track'], 'JEE')
        
        # 4. Fetch health after initialization
        response = self.client.get('/api/v1/twin/health')
        self.assertEqual(response.status_code, 200)
        health = response.json
        self.assertIn('twin_health', health)
        
    def test_route_registration_regression(self):
        # Ensure that twin routes are properly registered and prefixed
        rules = [str(p) for p in app.url_map.iter_rules()]
        self.assertIn('/api/v1/twin/profile', rules)
        self.assertIn('/api/v1/twin/health', rules)
        self.assertIn('/api/v1/twin/initialize', rules)

if __name__ == '__main__':
    unittest.main()
