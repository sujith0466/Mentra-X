import unittest
from backend.app import app
from backend.models import db, User, QuizQuestion, QuestionMetadata, AssessmentSession, AssessmentResponse, AssessmentResult
from backend.services.assessment.difficulty_policy import DifficultyPolicy
from backend.services.assessment.knowledge_estimator import KnowledgeEstimator
from backend.services.assessment.dna_seeder import DNASeeder
from backend.services.assessment.assessment_pipeline import AssessmentPipeline
from backend.tests.test_support import SQLiteFixtureMixin

class TestAssessmentCore(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()
        cls.create_base_fixture()
        
        with app.app_context():
            from backend.models import Quiz, Course
            import uuid
            # Ensure quiz exists for foreign key safely
            course = Course.query.first()
            if not course:
                course = Course(title="Test Course", description="Test")
                db.session.add(course)
                db.session.flush()
            quiz = Quiz(title=f"Math Baseline {uuid.uuid4().hex[:7]}", course_id=course.id, time_limit_minutes=30)
            db.session.add(quiz)
            db.session.flush()
            
            # Seed some assessment questions
            q1 = QuizQuestion(quiz_id=quiz.id, question_text="Easy Math", correct_answer="4")
            db.session.add(q1)
            db.session.flush()
            db.session.add(QuestionMetadata(question_id=q1.id, concept="math.addition", difficulty_tier=1, exam_track="JEE"))
            
            q2 = QuizQuestion(quiz_id=quiz.id, question_text="Med Math", correct_answer="2")
            db.session.add(q2)
            db.session.flush()
            db.session.add(QuestionMetadata(question_id=q2.id, concept="math.algebra", difficulty_tier=2, exam_track="JEE"))
            
            q3 = QuizQuestion(quiz_id=quiz.id, question_text="Hard Math", correct_answer="1")
            db.session.add(q3)
            db.session.flush()
            db.session.add(QuestionMetadata(question_id=q3.id, concept="math.calculus", difficulty_tier=3, exam_track="JEE"))
            
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixture()

    def test_difficulty_policy(self):
        policy = DifficultyPolicy(min_difficulty=1, max_difficulty=5)
        # Escalate on correct
        self.assertEqual(policy.get_next_difficulty(2, True), 3)
        self.assertEqual(policy.get_next_difficulty(5, True), 5)
        # Decay on incorrect
        self.assertEqual(policy.get_next_difficulty(2, False), 1)
        self.assertEqual(policy.get_next_difficulty(1, False), 1)

    def test_knowledge_estimator_and_dna_seeder(self):
        with app.app_context():
            user = User.query.first()
            
            # Self-heal leftover state from prior runs
            existing = AssessmentSession.query.filter_by(session_id="test-session-123").first()
            if existing:
                AssessmentResponse.query.filter_by(session_id=existing.id).delete()
                AssessmentResult.query.filter_by(session_id=existing.id).delete()
                db.session.delete(existing)
                db.session.commit()
                
            session = AssessmentSession(session_id="test-session-123", user_id=user.id, exam_track="JEE")
            db.session.add(session)
            db.session.commit()
            
            q1 = QuizQuestion.query.join(QuestionMetadata).filter(QuestionMetadata.concept=="math.addition").first()
            q3 = QuizQuestion.query.join(QuestionMetadata).filter(QuestionMetadata.concept=="math.calculus").first()
            
            r1 = AssessmentResponse(session_id=session.id, question_id=q1.id, submitted_answer="4", is_correct=True, difficulty_at_time=1)
            r2 = AssessmentResponse(session_id=session.id, question_id=q3.id, submitted_answer="wrong", is_correct=False, difficulty_at_time=3)
            db.session.add_all([r1, r2])
            db.session.commit()
            
            # Test Estimator
            knowledge_state = KnowledgeEstimator.compute_knowledge_state(session)
            self.assertIn("math.addition", knowledge_state)
            self.assertIn("math.calculus", knowledge_state)
            
            # Correct on diff 1 should increase slightly above 0.5
            self.assertGreater(knowledge_state["math.addition"], 0.5)
            # Incorrect on diff 3 should decrease below 0.5
            self.assertLess(knowledge_state["math.calculus"], 0.5)
            
            # Test DNA
            dna = DNASeeder.seed_learning_dna(session)
            self.assertEqual(dna["preferred_style"], "Mathematical") # JEE default
            self.assertEqual(dna["preferred_level"], 2) # Accuracy 0.5 -> stays at default 2
            
            # Clean up
            AssessmentResponse.query.filter_by(session_id=session.id).delete()
            db.session.delete(session)
            db.session.commit()

    def test_assessment_pipeline(self):
        with app.app_context():
            user = User.query.first()
            pipeline = AssessmentPipeline()
            
            # Start
            start_res = pipeline.start_assessment(user.id, "JEE")
            self.assertIn("session_id", start_res)
            self.assertIsNotNone(start_res["question"])
            self.assertEqual(start_res["current_difficulty"], 2)
            
            session_id = start_res["session_id"]
            question = start_res["question"]
            
            # Answer correctly
            ans_res = pipeline.submit_answer(session_id, question.id, question.correct_answer, 2)
            self.assertEqual(ans_res["status"], "active")
            self.assertTrue(ans_res["is_correct"])
            self.assertEqual(ans_res["next_difficulty"], 3) # Scaled up
            
            # Complete
            result = pipeline.complete_assessment(session_id)
            self.assertIsNotNone(result.knowledge_state)
            self.assertIsNotNone(result.inferred_style)
            
if __name__ == '__main__':
    unittest.main()
