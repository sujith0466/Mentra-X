from typing import Optional
from backend.models import AssessmentSession, QuizQuestion
from backend.services.assessment.difficulty_policy import DifficultyPolicy
from backend.services.assessment.question_selector import QuestionSelector

class BranchingEngine:
    """
    Coordinates the difficulty progression and question selection for an active assessment session.
    """
    def __init__(self, difficulty_policy: Optional[DifficultyPolicy] = None):
        self.policy = difficulty_policy or DifficultyPolicy()

    def determine_next_step(self, session: AssessmentSession, last_answer_correct: bool, current_difficulty: int) -> Optional[QuizQuestion]:
        """
        Calculates next difficulty and fetches the next question.
        Returns None if no more questions exist or session should terminate.
        """
        # Determine next difficulty based on policy
        next_difficulty = self.policy.get_next_difficulty(current_difficulty, last_answer_correct)
        
        # Get list of already answered question IDs
        exclude_ids = [resp.question_id for resp in session.responses]
        
        # Fetch next question
        return QuestionSelector.get_next_question(
            exam_track=session.exam_track,
            target_difficulty=next_difficulty,
            exclude_ids=exclude_ids
        )
