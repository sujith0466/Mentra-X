"""
Mentra X — Personalization Engine (Phase 6 Layer 6)

Unifying facade that coordinates the TutorDecisionEngine, LearningStyleDetector, and
DynamicPromptBuilder. Produces a validated PersonalizationBundleDTO consumed by the
Mastra Cognitive Swarm and TutorAgent tools.
"""

from typing import Dict, Any, List, Optional
from .dto import PersonalizationBundleDTO, TutorDecisionDTO
from .tutor_decision_engine import TutorDecisionEngine
from .learning_style_detector import LearningStyleDetector
from .dynamic_prompt_builder import DynamicPromptBuilder


class PersonalizationEngine:
    def __init__(self):
        self.decision_engine = TutorDecisionEngine()
        self.style_detector = LearningStyleDetector()
        self.prompt_builder = DynamicPromptBuilder()

    def assemble_personalization_bundle(
        self,
        user_id: str,
        concept: str,
        dna: Optional[Any] = None,
        explanation_history: Optional[List[Dict[str, Any]]] = None,
        weak_concepts: Optional[List[Dict[str, Any]]] = None,
        hydrated_context: Optional[Any] = None,
        session_response_times: Optional[List[float]] = None,
        answer_patterns: Optional[List[str]] = None,
        quiz_errors: Optional[List[str]] = None
    ) -> PersonalizationBundleDTO:
        """
        Orchestrates level selection, style inference, and prompt construction into a
        single typed DTO bundle.
        """
        if explanation_history is None:
            explanation_history = []
        if weak_concepts is None:
            weak_concepts = []

        # If DNA is not passed in, attempt to fetch from database
        if dna is None and user_id:
            try:
                from backend.models import StudentTwinRecord
                twin = StudentTwinRecord.query.filter_by(user_id=user_id).first()
                if twin and twin.learning_dna:
                    import json
                    dna = json.loads(twin.learning_dna) if isinstance(twin.learning_dna, str) else twin.learning_dna
            except Exception:
                dna = {}

        if dna is None:
            dna = {}

        # 1. Detect learning style
        detected_style, conf = self.style_detector.detect_style(
            session_response_times=session_response_times,
            answer_patterns=answer_patterns,
            quiz_errors=quiz_errors
        )

        # If DNA has a persistent preferred style with high confidence, prefer it over noisy single-session detection
        dna_dict = dna if isinstance(dna, dict) else getattr(dna, "__dict__", {})
        if not isinstance(dna_dict, dict):
            try:
                dna_dict = dna.to_dict()
            except Exception:
                dna_dict = {}

        adaptive_traits = dna_dict.get("adaptive_traits", {})
        preferred_style = adaptive_traits.get("preferred_style") or dna_dict.get("preferred_style")
        if preferred_style and isinstance(preferred_style, str) and preferred_style in ("Visual", "Mathematical", "Narrative"):
            final_style = preferred_style
        else:
            final_style = detected_style

        # 2. Select teaching level
        decision: TutorDecisionDTO = self.decision_engine.select_level(
            concept=concept,
            dna=dna_dict,
            explanation_history=explanation_history,
            weak_concepts=weak_concepts
        )

        # 3. Build level-templated dynamic system prompt
        system_prompt = self.prompt_builder.build(
            concept=concept,
            level=decision.level,
            dna=dna_dict,
            constraints=decision.constraints,
            hydrated_context=hydrated_context,
            style=final_style
        )

        # 4. Asynchronously update DNA style if we have user_id and confidence
        if user_id and final_style:
            try:
                self.style_detector.update_dna_style(user_id, final_style, conf)
            except Exception:
                pass

        return PersonalizationBundleDTO(
            selected_level=decision.level,
            selected_style=final_style,
            system_prompt=system_prompt,
            avoidance_constraints=decision.constraints.to_dict(),
            teaching_rationale=decision.rationale,
            level_name=decision.level_name
        )
