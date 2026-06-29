from typing import Optional
from backend.models import db, AssessmentSession, AssessmentResponse, AssessmentResult, QuizQuestion, utcnow
import uuid

class AssessmentService:
    """
    Handles database operations for the Assessment lifecycle.
    """
    
    @staticmethod
    def create_session(user_id: int, exam_track: str) -> AssessmentSession:
        session = AssessmentSession(
            session_id=str(uuid.uuid4()),
            user_id=user_id,
            exam_track=exam_track,
            status='active'
        )
        db.session.add(session)
        db.session.commit()
        return session
        
    @staticmethod
    def get_session(session_id: str) -> Optional[AssessmentSession]:
        return AssessmentSession.query.filter_by(session_id=session_id).first()
        
    @staticmethod
    def log_response(session: AssessmentSession, question: QuizQuestion, submitted_answer: str, is_correct: bool, difficulty: int) -> AssessmentResponse:
        resp = AssessmentResponse(
            session_id=session.id,
            question_id=question.id,
            submitted_answer=submitted_answer,
            is_correct=is_correct,
            difficulty_at_time=difficulty
        )
        db.session.add(resp)
        db.session.commit()
        return resp
        
    @staticmethod
    def complete_session(session: AssessmentSession, knowledge_state: dict, dna: dict) -> AssessmentResult:
        session.status = 'completed'
        session.completed_at = utcnow()
        
        result = AssessmentResult(
            session_id=session.id,
            knowledge_state=knowledge_state,
            inferred_style=dna.get('preferred_style'),
            inferred_level=dna.get('preferred_level', 2)
        )
        db.session.add(result)
        db.session.commit()
        return result
