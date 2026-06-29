from typing import Dict
from backend.models import AssessmentSession

class KnowledgeEstimator:
    """
    Computes a Bayesian knowledge state map from an AssessmentSession using a simplified IRT model.
    """
    
    @staticmethod
    def compute_knowledge_state(session: AssessmentSession) -> Dict[str, float]:
        """
        Calculates mastery [0.0, 1.0] for each concept cluster encountered in the session.
        Uses a uniform prior (0.5) and updates based on correctness weighted by question difficulty.
        """
        # Concept -> list of (is_correct, difficulty)
        concept_observations = {}
        
        for response in session.responses:
            meta = response.question.assessment_metadata
            if not meta or not meta.concept:
                continue
                
            concept = meta.concept
            if concept not in concept_observations:
                concept_observations[concept] = []
                
            concept_observations[concept].append((response.is_correct, response.difficulty_at_time))
            
        knowledge_state = {}
        
        for concept, observations in concept_observations.items():
            # Initial uniform prior
            mastery = 0.5
            
            for is_correct, diff in observations:
                # Weight update by difficulty tier (1-5)
                # Correct on hard question (diff 5) boosts mastery significantly more than correct on easy (diff 1).
                # Incorrect on easy question drops mastery significantly more than incorrect on hard.
                
                diff_weight = diff / 5.0  # [0.2, 1.0]
                
                if is_correct:
                    # Positive update: close the gap to 1.0
                    update_delta = (1.0 - mastery) * 0.4 * diff_weight
                    mastery += update_delta
                else:
                    # Negative update: close the gap to 0.0
                    # For incorrect, higher difficulty means lower penalty
                    penalty_weight = 1.0 - (diff_weight * 0.8) # easy questions hurt more to get wrong
                    update_delta = mastery * 0.4 * penalty_weight
                    mastery -= update_delta
                    
            # Clamp to [0.0, 1.0] safely
            knowledge_state[concept] = max(0.0, min(1.0, mastery))
            
        return knowledge_state
