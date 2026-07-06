"""
Mentra X — Dynamic Prompt Builder (Phase 6 Layer 6)

Constructs level-templated LLM system instructions tailored to the student's selected
teaching level (1-5), preferred learning style, historical avoidance constraints, and
hydrated semantic memory context.
"""

from typing import Dict, Any, Optional
from .dto import AvoidanceConstraintsDTO


class DynamicPromptBuilder:
    LEVEL_TEMPLATES = {
        1: (
            "Provide a concise, direct explanation of {concept}. "
            "The student has high mastery (score: {mastery:.2f}). "
            "One key formula and one sentence of context only."
        ),
        2: (
            "Teach {concept} via a worked, step-by-step example. "
            "Label every step. Start from first principles. "
            "Avoid {avoided_analogies}."
        ),
        3: (
            "The student commonly makes this mistake about {concept}: "
            "{common_error_pattern}. Address this error explicitly, "
            "then provide the correct explanation. Avoid {avoided_analogies}."
        ),
        4: (
            "Use a real-world visual analogy to explain {concept}. "
            "Do NOT use formulas until the analogy is established. "
            "Previous analogies that worked for this student: {worked_analogies}. "
            "Avoid: {avoided_analogies}."
        ),
        5: (
            "The student has failed to understand {concept} via "
            "mathematical and visual approaches. Use a completely "
            "alternative conceptual framework. Avoid all standard "
            "textbook approaches. Avoid {avoided_analogies}."
        ),
    }

    STYLE_INSTRUCTIONS = {
        "Visual": "Emphasize visual metaphors, spatial relationships, and mental imagery.",
        "Mathematical": "Emphasize algebraic derivations, numeric precision, and formal equations.",
        "Narrative": "Emphasize historical context, conceptual storytelling, and verbal intuition.",
        "Default": "Balance conceptual clarity with practical examples."
    }

    def build(
        self,
        concept: str,
        level: int,
        dna: Any,
        constraints: Optional[AvoidanceConstraintsDTO] = None,
        hydrated_context: Optional[Any] = None,
        style: str = "Default"
    ) -> str:
        """
        Renders the final system prompt for the Mastra Tutor Agent.
        """
        if not constraints:
            constraints = AvoidanceConstraintsDTO()

        level = max(1, min(5, int(level)))
        template = self.LEVEL_TEMPLATES.get(level, self.LEVEL_TEMPLATES[2])

        # Extract mastery
        dna_dict = dna if isinstance(dna, dict) else getattr(dna, "__dict__", {})
        if not isinstance(dna_dict, dict):
            try:
                dna_dict = dna.to_dict()
            except Exception:
                dna_dict = {}

        mastery_map = dna_dict.get("mastery_per_concept", {})
        if not isinstance(mastery_map, dict):
            mastery_map = {}
        mastery_val = float(mastery_map.get(concept, 0.50))

        # Extract common error patterns
        common_error = "misunderstanding foundational principles or boundary conditions"
        if hydrated_context:
            if isinstance(hydrated_context, dict):
                common_error = hydrated_context.get("common_error_pattern") or hydrated_context.get("notes") or common_error
            elif hasattr(hydrated_context, "notes") and getattr(hydrated_context, "notes"):
                common_error = str(getattr(hydrated_context, "notes"))

        avoided_str = ", ".join(constraints.analogies_to_avoid) if constraints.analogies_to_avoid else "none"
        worked_str = ", ".join(constraints.analogies_that_worked) if constraints.analogies_that_worked else "general real-world comparisons"

        try:
            rendered_prompt = template.format(
                concept=concept,
                mastery=mastery_val,
                avoided_analogies=avoided_str,
                worked_analogies=worked_str,
                common_error_pattern=common_error
            )
        except Exception:
            # Safe fallback if string format fails
            rendered_prompt = f"Teach {concept} at pedagogical level {level}. Avoid: {avoided_str}."

        style_note = self.STYLE_INSTRUCTIONS.get(style, self.STYLE_INSTRUCTIONS["Default"])
        final_prompt = f"[SYSTEM PEDAGOGICAL INSTRUCTION — LEVEL {level}]\n{rendered_prompt}\n[LEARNING STYLE ADJUSTMENT]\n{style_note}"

        return final_prompt
