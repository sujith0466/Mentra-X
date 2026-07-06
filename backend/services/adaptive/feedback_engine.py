"""
Mentra X — Real-Time Adaptive Feedback Engines (Phase 6 Layer 6)

Contains:
1. ProgressiveHintEngine: Supplies incremental hints (conceptual nudge -> structural
   framework -> specific step -> full walkthrough) without giving away immediate answers.
2. SocraticFeedbackEngine: Generates guiding Socratic questions in response to student
   errors rather than flat corrections, promoting metacognition.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class ProgressiveHintDTO:
    hint_level: int
    hint_type: str  # "CONCEPTUAL_NUDGE" | "STRUCTURAL_FRAMEWORK" | "STEP_GUIDANCE" | "WALKTHROUGH"
    hint_text: str
    remaining_hints: int
    penalty_factor: float  # Grade deduction factor for requesting this level of hint

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SocraticFeedbackDTO:
    is_correct: bool
    socratic_question: str
    concept_targeted: str
    reflective_prompt: str
    encouragement: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ProgressiveHintEngine:
    HINT_LADDER_TEMPLATES = [
        {
            "type": "CONCEPTUAL_NUDGE",
            "template": "Consider the underlying principle of {concept}. What key property or invariant must hold true here?",
            "penalty": 0.05
        },
        {
            "type": "STRUCTURAL_FRAMEWORK",
            "template": "Let's structure the approach for {concept}: breaking the problem into initialization, iteration/transition, and termination steps.",
            "penalty": 0.10
        },
        {
            "type": "STEP_GUIDANCE",
            "template": "Specific check for {concept}: verify how you handle boundary conditions or edge cases in your intermediate step.",
            "penalty": 0.20
        },
        {
            "type": "WALKTHROUGH",
            "template": "Walkthrough outline for {concept}: 1) Define state/variables. 2) Execute core transformation step-by-step. 3) Return evaluated result.",
            "penalty": 0.35
        }
    ]

    def get_hint(
        self,
        concept: str,
        current_hint_index: int = 0,
        problem_context: Optional[str] = None,
        custom_hints: Optional[List[str]] = None
    ) -> ProgressiveHintDTO:
        """
        Returns the next incremental hint in the ladder.
        """
        max_idx = len(self.HINT_LADDER_TEMPLATES) - 1
        idx = min(max(0, int(current_hint_index)), max_idx)
        template_info = self.HINT_LADDER_TEMPLATES[idx]

        if custom_hints and idx < len(custom_hints):
            text = custom_hints[idx]
        else:
            clean_concept = concept.replace("_", " ") if concept else "this problem"
            text = template_info["template"].format(concept=clean_concept)
            if problem_context and idx >= 1:
                text += f" (Context: {problem_context[:100]}...)"

        return ProgressiveHintDTO(
            hint_level=idx + 1,
            hint_type=template_info["type"],
            hint_text=text,
            remaining_hints=max_idx - idx,
            penalty_factor=template_info["penalty"]
        )


class SocraticFeedbackEngine:
    def generate_socratic_feedback(
        self,
        concept: str,
        student_answer: Any,
        expected_concept_rule: str = "",
        is_correct: bool = False
    ) -> SocraticFeedbackDTO:
        """
        Formulates a Socratic guiding question when a student submits an incorrect response.
        """
        clean_concept = concept.replace("_", " ") if concept else "this topic"
        
        if is_correct:
            return SocraticFeedbackDTO(
                is_correct=True,
                socratic_question="Excellent! Why do you think this solution works so efficiently?",
                concept_targeted=clean_concept,
                reflective_prompt="How would your approach change if the input size were doubled?",
                encouragement="Great mastery demonstrated!"
            )

        ans_str = str(student_answer)[:100]
        rule_str = f" Recall that {expected_concept_rule}." if expected_concept_rule else ""

        question = f"You answered '{ans_str}'. Why did you choose that approach for {clean_concept}?{rule_str} What assumption might we need to re-examine?"
        prompt = f"Try tracing your answer step-by-step against a simple example for {clean_concept}."
        encouragement = "Mistakes are essential for deep learning! Let's examine the reasoning together."

        return SocraticFeedbackDTO(
            is_correct=False,
            socratic_question=question,
            concept_targeted=clean_concept,
            reflective_prompt=prompt,
            encouragement=encouragement
        )
