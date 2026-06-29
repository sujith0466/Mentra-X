from typing import List, Optional
from sqlalchemy import func
from backend.models import QuizQuestion, QuestionMetadata

class QuestionSelector:
    """
    Handles fetching questions from the global question bank using the new QuestionMetadata.
    """
    
    @staticmethod
    def get_next_question(exam_track: str, target_difficulty: int, exclude_ids: List[int]) -> Optional[QuizQuestion]:
        """
        Fetches the next most appropriate question matching the track and difficulty.
        If no exact difficulty match is found, attempts to find the closest match.
        """
        # First, try exact difficulty match
        query = (QuizQuestion.query
                 .join(QuestionMetadata)
                 .filter(QuestionMetadata.exam_track == exam_track)
                 .filter(QuestionMetadata.difficulty_tier == target_difficulty)
                 .filter(~QuizQuestion.id.in_(exclude_ids) if exclude_ids else True))
                 
        # Order randomly for variety within the same tier
        question = query.order_by(func.random()).first()
        
        if not question:
            # Fallback: Find any question in this track not yet answered
            fallback_query = (QuizQuestion.query
                             .join(QuestionMetadata)
                             .filter(QuestionMetadata.exam_track == exam_track)
                             .filter(~QuizQuestion.id.in_(exclude_ids) if exclude_ids else True))
            question = fallback_query.order_by(func.random()).first()
            
        return question
