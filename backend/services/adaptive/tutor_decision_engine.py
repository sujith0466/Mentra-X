"""
Mentra X — Tutor Decision Engine (Phase 6 Layer 6)

Implements the 5-level pedagogical escalation hierarchy and avoidance constraint
evaluation algorithm. Selects teaching strategy and level based on student mastery,
historical failure records, and cognitive traits.
"""

import math
import time
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from .dto import TutorDecisionDTO, AvoidanceConstraintsDTO


class TutorDecisionEngine:
    LEVEL_NAMES = {
        1: "Direct",
        2: "Worked Example",
        3: "Mistake Analysis",
        4: "Visual Analogy",
        5: "Alternative Paradigm"
    }

    LEVEL_STRATEGIES = {
        1: "Concise, precise",
        2: "Procedural, step-by-step",
        3: "Diagnostic, corrective",
        4: "Concrete, tangible",
        5: "Reframe, lateral"
    }

    def select_level(
        self,
        concept: str,
        dna: Any,
        explanation_history: Optional[List[Dict[str, Any]]] = None,
        weak_concepts: Optional[List[Dict[str, Any]]] = None
    ) -> TutorDecisionDTO:
        """
        Evaluates student state and history to select the optimal teaching level (1-5).
        
        Priority order:
        1. Critical weakness check -> jump to Level 4 or 5
        2. Consecutive failures check -> escalate level
        3. Avoidance constraint check -> skip failed levels
        4. Mastery threshold check -> baseline level selection
        5. Cognitive visual trait preference adjustment
        """
        if explanation_history is None:
            explanation_history = []
        if weak_concepts is None:
            weak_concepts = []

        # Convert dna to dict if it's an object/model
        dna_dict = dna if isinstance(dna, dict) else getattr(dna, "__dict__", {})
        if not isinstance(dna_dict, dict):
            try:
                dna_dict = dna.to_dict()
            except Exception:
                dna_dict = {}

        constraints = self.build_avoidance_constraints(concept, explanation_history)
        mastery, adjusted_mastery = self.compute_mastery_context(concept, dna_dict)

        rationale_parts = []
        selected_level = 2  # default fallback

        # Check 1: Critical Weakness
        is_critical = False
        for weak in weak_concepts:
            if isinstance(weak, dict):
                w_concept = weak.get("concept") or weak.get("name") or ""
                severity = str(weak.get("severity", "")).upper()
                if w_concept.lower() == concept.lower() and severity == "CRITICAL":
                    is_critical = True
                    break

        if is_critical:
            selected_level = 4
            rationale_parts.append(f"Concept '{concept}' is flagged as a CRITICAL weakness -> jumping to Level 4.")

        # Check 2: Consecutive failures at current/recent level
        consecutive_failures = 0
        last_failed_level = None
        for record in reversed(explanation_history):
            if not isinstance(record, dict):
                continue
            r_concept = record.get("concept", "")
            if r_concept and r_concept.lower() != concept.lower():
                continue
            is_success = record.get("outcome_success") or record.get("success") or False
            if not is_success:
                consecutive_failures += 1
                if last_failed_level is None:
                    last_failed_level = int(record.get("selected_level") or record.get("level") or 2)
            else:
                break

        if consecutive_failures >= 2 and last_failed_level is not None:
            escalated = min(5, last_failed_level + 2)
            if escalated > selected_level:
                selected_level = escalated
                rationale_parts.append(f"Detected {consecutive_failures} consecutive explanation failures at Level {last_failed_level} -> escalating by 2 to Level {selected_level}.")

        # Check 3: Mastery threshold baseline (if not already escalated by critical or consecutive failures)
        if not rationale_parts:
            if adjusted_mastery > 0.75:
                selected_level = 1
                rationale_parts.append(f"High adjusted mastery ({adjusted_mastery:.2f} > 0.75) -> Level 1 (Direct).")
            elif adjusted_mastery >= 0.45:
                selected_level = 2
                rationale_parts.append(f"Moderate adjusted mastery ({adjusted_mastery:.2f}) -> Level 2 (Worked Example).")
            else:
                selected_level = 3
                rationale_parts.append(f"Low adjusted mastery ({adjusted_mastery:.2f} < 0.45) -> Level 3 (Mistake Analysis).")

        # Check 4: Visual DNA preference or trait flag
        adaptive_traits = dna_dict.get("adaptive_traits", {})
        preferred_style = adaptive_traits.get("preferred_style") or dna_dict.get("preferred_style") or ""
        visual_flag = dna_dict.get("visual_flag") or (str(preferred_style).lower() == "visual")
        if visual_flag and selected_level < 4:
            # If student is visual and struggling (or moderate), prefer Level 4
            if selected_level in (2, 3):
                selected_level = 4
                rationale_parts.append("Student learning DNA indicates strong Visual preference -> elevating strategy to Level 4 (Visual Analogy).")

        # Check 5: Avoidance constraints (if selected level has failed before for this concept, escalate or shift)
        while selected_level in constraints.levels_to_avoid and selected_level <= 5:
            old_lvl = selected_level
            selected_level = min(5, selected_level + 1)
            if selected_level == old_lvl: # Already at 5
                break
            rationale_parts.append(f"Level {old_lvl} is in avoidance constraints due to prior failure -> shifted to Level {selected_level}.")

        # Final sanity bound
        selected_level = max(1, min(5, selected_level))
        level_name = self.LEVEL_NAMES.get(selected_level, "Worked Example")
        strategy = self.LEVEL_STRATEGIES.get(selected_level, "Procedural, step-by-step")
        rationale = " ".join(rationale_parts)

        return TutorDecisionDTO(
            level=selected_level,
            level_name=level_name,
            strategy=strategy,
            rationale=rationale,
            constraints=constraints,
            adjusted_mastery=adjusted_mastery
        )

    def build_avoidance_constraints(
        self,
        concept: str,
        explanation_history: List[Dict[str, Any]]
    ) -> AvoidanceConstraintsDTO:
        """
        Scans explanation history to extract failed levels and analogies to avoid,
        as well as analogies that previously succeeded.
        """
        levels_to_avoid = set()
        analogies_to_avoid = set()
        analogies_that_worked = set()

        for record in explanation_history:
            if not isinstance(record, dict):
                continue
            r_concept = record.get("concept", "")
            if r_concept and r_concept.lower() != concept.lower():
                continue

            is_success = record.get("outcome_success")
            if is_success is None:
                is_success = record.get("success", True)
                if record.get("failed") is True:
                    is_success = False

            level = record.get("selected_level") or record.get("level")
            analogy = record.get("analogy_used") or record.get("analogy")

            if not is_success:
                if level and isinstance(level, (int, str)):
                    try:
                        levels_to_avoid.add(int(level))
                    except ValueError:
                        pass
                if analogy and isinstance(analogy, str) and analogy.strip():
                    analogies_to_avoid.add(analogy.strip())
            else:
                if analogy and isinstance(analogy, str) and analogy.strip():
                    analogies_that_worked.add(analogy.strip())

        return AvoidanceConstraintsDTO(
            levels_to_avoid=sorted(list(levels_to_avoid)),
            analogies_to_avoid=sorted(list(analogies_to_avoid)),
            analogies_that_worked=sorted(list(analogies_that_worked))
        )

    def compute_mastery_context(
        self,
        concept: str,
        dna_dict: Dict[str, Any]
    ) -> (float, float):
        """
        Computes raw mastery and Ebbinghaus decay-adjusted retention.
        Formula: adjusted_mastery = mastery * e^(-t / S)
        where t is days elapsed since last study, and S is stability factor (10.0 days).
        """
        mastery_map = dna_dict.get("mastery_per_concept", {})
        if not isinstance(mastery_map, dict):
            mastery_map = {}
        
        raw_mastery = float(mastery_map.get(concept, 0.50))
        raw_mastery = max(0.0, min(1.0, raw_mastery))

        last_studied_str = dna_dict.get("last_studied_per_concept", {}).get(concept)
        if not last_studied_str:
            return raw_mastery, raw_mastery

        try:
            # Parse ISO timestamp or epoch
            if isinstance(last_studied_str, (int, float)):
                last_time = float(last_studied_str)
            else:
                dt = datetime.fromisoformat(str(last_studied_str).replace("Z", "+00:00"))
                last_time = dt.timestamp()
            
            elapsed_seconds = time.time() - last_time
            if elapsed_seconds <= 0:
                return raw_mastery, raw_mastery

            elapsed_days = elapsed_seconds / 86400.0
            stability_factor = float(dna_dict.get("memory_stability", 10.0))
            if stability_factor <= 0:
                stability_factor = 10.0

            decay_multiplier = math.exp(-elapsed_days / stability_factor)
            adjusted_mastery = raw_mastery * decay_multiplier
            adjusted_mastery = max(0.0, min(1.0, adjusted_mastery))
            return raw_mastery, adjusted_mastery
        except Exception:
            return raw_mastery, raw_mastery
