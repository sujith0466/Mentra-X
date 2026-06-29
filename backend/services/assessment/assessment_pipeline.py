from typing import Dict, Any, Optional
from backend.models import QuizQuestion, AssessmentSession, AssessmentResult, db
from backend.services.assessment.assessment_service import AssessmentService
from backend.services.assessment.branching_engine import BranchingEngine
from backend.services.assessment.knowledge_estimator import KnowledgeEstimator
from backend.services.assessment.dna_seeder import DNASeeder

class AssessmentPipeline:
    """
    Single orchestration point for the Adaptive Assessment Engine.
    Handles start, answer submission, and completion flows.
    """
    
    def __init__(self):
        self.branching = BranchingEngine()
        self.estimator = KnowledgeEstimator()
        self.seeder = DNASeeder()
        
    def start_assessment(self, user_id: int, exam_track: str) -> dict:
        """
        Creates a session and returns the first question.
        Starts at default difficulty tier 2.
        """
        session = AssessmentService.create_session(user_id, exam_track)
        
        # Initial question at difficulty 2
        next_question = self.branching.determine_next_step(session, True, 1) # acts as "started at diff 1, got right -> jump to 2" or we can just fetch manually.
        
        if not next_question:
            # Fallback direct fetch if branching engine acts weird on start
            from backend.services.assessment.question_selector import QuestionSelector
            next_question = QuestionSelector.get_next_question(exam_track, 2, [])
            
        return {
            'session_id': session.session_id,
            'question': next_question,
            'current_difficulty': 2 if next_question else None
        }
        
    def submit_answer(self, session_id: str, question_id: int, submitted_answer: str, current_difficulty: int) -> dict:
        """
        Evaluates the answer, logs it, and returns the next question or completion trigger.
        """
        session = AssessmentService.get_session(session_id)
        if not session or session.status != 'active':
            raise ValueError("Invalid or inactive session.")
            
        question = db.session.get(QuizQuestion, question_id)
        if not question:
            raise ValueError("Invalid question ID.")
            
        is_correct = (submitted_answer.strip().lower() == question.correct_answer.strip().lower())
        
        # Log response
        AssessmentService.log_response(session, question, submitted_answer, is_correct, current_difficulty)
        
        # Terminate if limit reached (e.g., 15 questions)
        if len(session.responses) >= 15:
            return {'status': 'completed'}
            
        # Determine next step
        next_question = self.branching.determine_next_step(session, is_correct, current_difficulty)
        
        if not next_question:
            # No more questions available
            return {'status': 'completed'}
            
        return {
            'status': 'active',
            'is_correct': is_correct,
            'next_question': next_question,
            'next_difficulty': self.branching.policy.get_next_difficulty(current_difficulty, is_correct)
        }
        
    def complete_assessment(self, session_id: str) -> AssessmentResult:
        """
        Finalizes the assessment and updates the Digital Twin.
        """
        session = AssessmentService.get_session(session_id)
        if not session or session.status != 'active':
            raise ValueError("Invalid or inactive session.")
            
        knowledge_state = self.estimator.compute_knowledge_state(session)
        dna = self.seeder.seed_learning_dna(session)
        
        # Write to assessment DB
        result = AssessmentService.complete_session(session, knowledge_state, dna)
        
        # Mutate the twin
        from backend.services.twin.twin_mutator import mutate_knowledge, mutate_learning_dna
        for concept, mastery in knowledge_state.items():
            mutate_knowledge(session.user_id, concept, mastery, "Assessment Pipeline Estimation")
            
        mutate_learning_dna(session.user_id, dna, "Assessment Pipeline Estimation")
        
        return result
