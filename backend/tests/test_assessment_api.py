import unittest
from backend.app import app
from backend.models import db, User, QuizQuestion, QuestionMetadata, StudentTwinRecord, Quiz, Course
from backend.tests.test_support import SQLiteFixtureMixin
import uuid

class TestAssessmentAPI(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()
        cls.create_base_fixture()
        
        with app.app_context():
            # Ensure quiz exists for foreign key safely
            course = Course.query.first()
            if not course:
                course = Course(title="Test Course API", description="Test")
                db.session.add(course)
                db.session.flush()
                
            quiz = Quiz(title=f"Mathematics Certification {uuid.uuid4().hex[:7]}", course_id=course.id, time_limit_minutes=30)
            db.session.add(quiz)
            db.session.flush()
            
            # Seed questions
            for i in range(1, 4):
                q = QuizQuestion(quiz_id=quiz.id, question_text=f"Math Q{i}", correct_answer=f"{i}")
                db.session.add(q)
                db.session.flush()
                db.session.add(QuestionMetadata(question_id=q.id, concept="math.api", difficulty_tier=i, exam_track="JEE"))
            
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixture()

    def login_as_student(self):
        with app.app_context():
            user = User.query.filter_by(role='student').first()
            user_id = user.id
            twin = StudentTwinRecord.query.filter_by(user_id=user_id).first()
            if not twin:
                twin = StudentTwinRecord(user_id=user_id, learning_dna="{}", twin_version=1)
                db.session.add(twin)
                db.session.commit()
        
        with self.client.session_transaction() as session:
            session['user_id'] = user_id
            session['user_role'] = 'student'
            
        return user_id

    def test_auth_required(self):
        # Ensure we are logged out
        self.clear_session(self.client)
        response = self.client.post('/api/v1/assessment/start', json={'exam_track': 'JEE'})
        self.assertEqual(response.status_code, 401)

    def test_assessment_lifecycle_and_twin_update(self):
        user_id = self.login_as_student()
        
        # 1. Start session
        res_start = self.client.post('/api/v1/assessment/start', json={'exam_track': 'JEE'})
        self.assertEqual(res_start.status_code, 201)
        data_start = res_start.get_json()
        self.assertEqual(data_start['status'], 'success')
        self.assertIn('session_id', data_start)
        
        session_id = data_start['session_id']
        question_id = data_start['question']['id']
        
        # 2. Check session status
        res_status = self.client.get(f'/api/v1/assessment/session/{session_id}')
        self.assertEqual(res_status.status_code, 200)
        self.assertEqual(res_status.get_json()['session_status'], 'active')
        
        # 3. Answer correctly
        res_ans = self.client.post('/api/v1/assessment/answer', json={
            'session_id': session_id,
            'question_id': question_id,
            'submitted_answer': "2", # Might be correct or wrong based on random fetch
            'current_difficulty': data_start['current_difficulty']
        })
        self.assertEqual(res_ans.status_code, 200)
        res_ans.get_json()
        
        # 4. Complete assessment
        res_complete = self.client.post('/api/v1/assessment/complete', json={'session_id': session_id})
        self.assertEqual(res_complete.status_code, 200)
        data_complete = res_complete.get_json()
        self.assertEqual(data_complete['status'], 'success')
        
        # 5. Verify Twin Update
        with app.app_context():
            twin = StudentTwinRecord.query.filter_by(user_id=user_id).first()
            self.assertIsNotNone(twin)
            self.assertIsNotNone(twin.learning_dna)
            
            # Check mutation logs
            from backend.models import TwinMutationLogRecord
            logs = TwinMutationLogRecord.query.filter_by(user_id=user_id).all()
            self.assertTrue(any(log.mutation_type == "Assessment Pipeline Estimation" for log in logs))

if __name__ == '__main__':
    unittest.main()
