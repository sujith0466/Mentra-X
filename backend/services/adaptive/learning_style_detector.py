"""
Mentra X — Learning Style Detector (Phase 6 Layer 6)

Real-time inference engine that evaluates student response latencies, answer keywords,
and quiz error patterns to infer preferred cognitive learning style:
- 'Visual' (diagrams, analogies, tangible metaphors)
- 'Mathematical' (formulas, equations, step-by-step derivations)
- 'Narrative' (conceptual stories, verbal context, why-based explanations)
"""

from typing import List, Dict, Any, Tuple, Optional
import json


class LearningStyleDetector:
    VISUAL_KEYWORDS = {"diagram", "picture", "analogy", "chart", "visual", "look", "imagine", "graph", "draw", "metaphor", "color", "shape"}
    MATH_KEYWORDS = {"formula", "equation", "math", "calc", "number", "step", "derive", "proof", "variable", "function", "integral", "matrix"}
    NARRATIVE_KEYWORDS = {"story", "why", "concept", "explain", "read", "context", "history", "meaning", "words", "describe", "understand", "reason"}

    def detect_style(
        self,
        session_response_times: Optional[List[float]] = None,
        answer_patterns: Optional[List[str]] = None,
        quiz_errors: Optional[List[str]] = None
    ) -> Tuple[str, float]:
        """
        Infers preferred learning style and confidence score (0.0 to 1.0).
        Returns: (style_name, confidence)
        """
        if session_response_times is None:
            session_response_times = []
        if answer_patterns is None:
            answer_patterns = []
        if quiz_errors is None:
            quiz_errors = []

        scores = {"Visual": 0.0, "Mathematical": 0.0, "Narrative": 0.0}

        # 1. Analyze verbal answer patterns & keywords
        for text in answer_patterns:
            if not isinstance(text, str):
                continue
            words = set(text.lower().replace(".", " ").replace(",", " ").split())
            scores["Visual"] += len(words.intersection(self.VISUAL_KEYWORDS)) * 2.0
            scores["Mathematical"] += len(words.intersection(self.MATH_KEYWORDS)) * 2.0
            scores["Narrative"] += len(words.intersection(self.NARRATIVE_KEYWORDS)) * 2.0

        # 2. Analyze response latencies (fast responses < 12s on math often indicate math fluency;
        # medium latencies 12-25s on verbal indicate narrative reading; visual often engages quickly with analogies)
        avg_time = sum(session_response_times) / len(session_response_times) if session_response_times else 20.0
        if avg_time < 12.0:
            scores["Mathematical"] += 1.5
        elif 12.0 <= avg_time <= 25.0:
            scores["Narrative"] += 1.5
        else:
            scores["Visual"] += 1.5

        # 3. Analyze quiz error keywords (if student misses math questions, they might need visual or narrative support)
        for err in quiz_errors:
            if not isinstance(err, str):
                continue
            words = set(err.lower().replace(".", " ").replace(",", " ").split())
            if words.intersection(self.MATH_KEYWORDS):
                # Struggling with math -> boost Visual and Narrative as alternative representations
                scores["Visual"] += 1.0
                scores["Narrative"] += 1.0
            elif words.intersection(self.NARRATIVE_KEYWORDS):
                scores["Visual"] += 1.0
                scores["Mathematical"] += 1.0

        total_score = sum(scores.values())
        if total_score == 0:
            return "Visual", 0.50  # Default baseline fallback

        best_style = max(scores, key=scores.get)
        confidence = scores[best_style] / total_score
        confidence = max(0.33, min(0.99, confidence))

        return best_style, confidence

    def update_dna_style(
        self,
        user_id: str,
        detected_style: str,
        confidence: float,
        session_id: Optional[str] = None
    ) -> bool:
        """
        Updates preferred_style in student's LearningDNA if detected_style is consistent
        over 3+ consecutive sessions (hysteresis noise prevention).
        """
        try:
            from backend.models import db, StudentTwinRecord
            twin = StudentTwinRecord.query.filter_by(user_id=user_id).first()
            if not twin:
                return False

            dna_dict = {}
            if twin.learning_dna:
                try:
                    dna_dict = json.loads(twin.learning_dna) if isinstance(twin.learning_dna, str) else twin.learning_dna
                except Exception:
                    dna_dict = {}
            if not isinstance(dna_dict, dict):
                dna_dict = {}

            adaptive_traits = dna_dict.get("adaptive_traits", {})
            if not isinstance(adaptive_traits, dict):
                adaptive_traits = {}

            style_history = adaptive_traits.get("style_history", [])
            if not isinstance(style_history, list):
                style_history = []

            style_history.append({"style": detected_style, "confidence": confidence, "session_id": session_id})
            # Keep last 10 sessions
            style_history = style_history[-10:]
            adaptive_traits["style_history"] = style_history

            # Hysteresis rule: check last 3 sessions
            recent_styles = [s.get("style") for s in style_history[-3:] if isinstance(s, dict)]
            current_preferred = adaptive_traits.get("preferred_style") or dna_dict.get("preferred_style")

            if not current_preferred:
                # First time setting style
                adaptive_traits["preferred_style"] = detected_style
                adaptive_traits["style_confidence"] = confidence
            elif len(recent_styles) >= 3 and all(s == detected_style for s in recent_styles):
                # 3 consecutive consistent detections -> update preferred style
                adaptive_traits["preferred_style"] = detected_style
                adaptive_traits["style_confidence"] = confidence

            dna_dict["adaptive_traits"] = adaptive_traits
            if "preferred_style" in adaptive_traits:
                dna_dict["preferred_style"] = adaptive_traits["preferred_style"]

            twin.learning_dna = json.dumps(dna_dict)
            db.session.commit()
            return True
        except Exception:
            try:
                from backend.models import db
                db.session.rollback()
            except Exception:
                pass
            return False
