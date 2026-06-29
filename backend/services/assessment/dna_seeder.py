from typing import Dict, Any
from backend.models import AssessmentSession

class DNASeeder:
    """
    Infers the initial Learning DNA from a completed AssessmentSession response pattern.
    Supports expansion for future phases (Teaching Preference, Pacing, Hint Usage, etc.).
    """
    
    # Exam-Track Defaults (Cold Start fallbacks)
    TRACK_DEFAULTS = {
        'JEE': {'style': 'Mathematical', 'level': 2},
        'NEET': {'style': 'Narrative', 'level': 2},
        'UPSC': {'style': 'Narrative', 'level': 1},
        'CAT': {'style': 'Visual', 'level': 2},
        'DEFAULT': {'style': 'Visual', 'level': 1}
    }

    @classmethod
    def seed_learning_dna(cls, session: AssessmentSession) -> Dict[str, Any]:
        """
        Calculates initial Learning DNA payload for TwinMutator.
        Currently focuses on inferring 'preferred_style' and 'preferred_level'.
        """
        track = session.exam_track if session.exam_track in cls.TRACK_DEFAULTS else 'DEFAULT'
        defaults = cls.TRACK_DEFAULTS[track]
        
        # Inference logic based on assessment patterns could go here.
        # For Phase 2, we use a simple heuristic based on correct answers per subject/topic type,
        # but to keep it simple as requested ("seed only initial profile, do not over-engineer"), 
        # we will rely heavily on track defaults, tweaked slightly if possible.
        
        inferred_style = defaults['style']
        
        # Let's say if they failed heavily (lots of decays), drop the level
        total_qs = len(session.responses)
        if total_qs > 0:
            correct_count = sum(1 for r in session.responses if r.is_correct)
            accuracy = correct_count / total_qs
            
            inferred_level = defaults['level']
            if accuracy < 0.3:
                inferred_level = max(1, inferred_level - 1)
            elif accuracy > 0.8:
                inferred_level = min(5, inferred_level + 1)
        else:
            inferred_level = defaults['level']
            
        return {
            'preferred_style': inferred_style,
            'preferred_level': inferred_level,
            # Future fields can be initialized here safely:
            # 'frustration_tolerance': 0.3,
            # 'engagement_score': 0.5
        }
