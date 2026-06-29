from flask import current_app
from backend.services.assessment.assessment_pipeline import AssessmentPipeline
from backend.services.assessment.assessment_service import AssessmentService
from backend.models import QuizQuestion

class AssessmentFacade:
    """
    Acts as the entrypoint for API routes. 
    Handles validation, formatting, and secure invocation of the underlying pipeline.
    """
    
    def __init__(self):
        self.pipeline = AssessmentPipeline()

    def start(self, user_id: int, exam_track: str) -> tuple[dict, int]:
        if not exam_track:
            return {"status": "error", "message": "Exam track is required."}, 400
            
        try:
            result = self.pipeline.start_assessment(user_id, exam_track)
            
            payload = {
                "status": "success",
                "session_id": result["session_id"],
                "question": self._format_question(result["question"]),
                "current_difficulty": result["current_difficulty"]
            }
            return payload, 201
        except Exception as e:
            current_app.logger.error(f"Error starting assessment: {str(e)}")
            return {"status": "error", "message": "Internal server error"}, 500

    def answer(self, user_id: int, session_id: str, question_id: int, submitted_answer: str, current_difficulty: int) -> tuple[dict, int]:
        if not session_id or not question_id or submitted_answer is None:
            return {"status": "error", "message": "Missing required fields."}, 400
            
        # Security: verify session belongs to user
        session = AssessmentService.get_session(session_id)
        if not session or session.user_id != user_id:
            return {"status": "error", "message": "Invalid session."}, 403
            
        try:
            result = self.pipeline.submit_answer(session_id, question_id, submitted_answer, current_difficulty)
            
            if result.get("status") == "completed":
                return {"status": "completed", "message": "Assessment limit reached, ready for completion."}, 200
                
            payload = {
                "status": "active",
                "is_correct": result["is_correct"],
                "next_question": self._format_question(result["next_question"]),
                "next_difficulty": result["next_difficulty"]
            }
            return payload, 200
            
        except ValueError as ve:
            return {"status": "error", "message": str(ve)}, 400
        except Exception as e:
            current_app.logger.error(f"Error submitting answer: {str(e)}")
            return {"status": "error", "message": "Internal server error"}, 500

    def complete(self, user_id: int, session_id: str) -> tuple[dict, int]:
        if not session_id:
            return {"status": "error", "message": "Missing session ID."}, 400
            
        # Security: verify session belongs to user
        session = AssessmentService.get_session(session_id)
        if not session or session.user_id != user_id:
            return {"status": "error", "message": "Invalid session."}, 403
            
        try:
            result = self.pipeline.complete_assessment(session_id)
            payload = {
                "status": "success",
                "message": "Assessment finalized. Twin updated.",
                "inferred_style": result.inferred_style,
                "inferred_level": result.inferred_level
            }
            return payload, 200
        except ValueError as ve:
            return {"status": "error", "message": str(ve)}, 400
        except Exception as e:
            current_app.logger.error(f"Error completing assessment: {str(e)}")
            return {"status": "error", "message": "Internal server error"}, 500
            
    def get_session(self, user_id: int, session_id: str) -> tuple[dict, int]:
        session = AssessmentService.get_session(session_id)
        if not session or session.user_id != user_id:
            return {"status": "error", "message": "Invalid session."}, 404
            
        return {
            "status": "success",
            "session_id": session.session_id,
            "session_status": session.status,
            "exam_track": session.exam_track,
            "questions_answered": len(session.responses)
        }, 200
        
    def _format_question(self, question: QuizQuestion) -> dict:
        if not question:
            return None
        return {
            "id": question.id,
            "text": question.question_text,
            "type": question.question_type,
            "options": {
                "a": question.option_a,
                "b": question.option_b,
                "c": question.option_c,
                "d": question.option_d
            }
        }
