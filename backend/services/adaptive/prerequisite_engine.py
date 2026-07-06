"""
Mentra X — Prerequisite Dependency Engine (Phase 6 Layer 6)

Evaluates concept dependency graphs to verify whether a student has sufficient
foundational mastery before attempting advanced lessons or quizzes. Prevents cognitive
overload and pedagogical frustration by blocking unready progression.
"""

from typing import Dict, Any, List, Optional


class PrerequisiteEngine:
    DEFAULT_DEPENDENCIES = {
        "dynamic_programming": ["recursion", "arrays"],
        "recursion": ["functions", "stack_memory"],
        "graph_algorithms": ["trees", "recursion", "queues"],
        "trees": ["linked_lists", "recursion"],
        "hash_tables": ["arrays", "hashing_basics"],
        "advanced_sql": ["basic_sql", "relational_algebra"],
        "machine_learning": ["linear_algebra", "calculus", "python_syntax"],
        "deep_learning": ["machine_learning", "neural_networks_basics"]
    }

    def check_prerequisites(
        self,
        target_concept: str,
        dna: Any,
        dependency_graph: Optional[Dict[str, List[str]]] = None,
        mastery_threshold: float = 0.60
    ) -> Dict[str, Any]:
        """
        Checks if all prerequisites for target_concept meet or exceed mastery_threshold.
        Returns: { allowed: bool, missing_prereqs: list[dict], warning_message: str }
        """
        if dependency_graph is None:
            dependency_graph = self.DEFAULT_DEPENDENCIES

        target_key = target_concept.lower().replace(" ", "_")
        prereqs = dependency_graph.get(target_key, [])
        if not prereqs:
            return {
                "allowed": True,
                "target_concept": target_concept,
                "missing_prereqs": [],
                "warning_message": ""
            }

        dna_dict = dna if isinstance(dna, dict) else getattr(dna, "__dict__", {})
        if not isinstance(dna_dict, dict):
            try:
                dna_dict = dna.to_dict()
            except Exception:
                dna_dict = {}

        mastery_map = dna_dict.get("mastery_per_concept", {})
        if not isinstance(mastery_map, dict):
            mastery_map = {}

        missing = []
        for p in prereqs:
            p_score = float(mastery_map.get(p, 0.50)) # default 0.50 assume moderate
            if p_score < mastery_threshold:
                missing.append({
                    "concept": p,
                    "current_mastery": round(p_score, 2),
                    "required_mastery": mastery_threshold
                })

        if not missing:
            return {
                "allowed": True,
                "target_concept": target_concept,
                "missing_prereqs": [],
                "warning_message": ""
            }

        missing_names = [m["concept"] for m in missing]
        msg = f"Cannot start '{target_concept}' yet. Please review prerequisite concepts with mastery below {mastery_threshold * 100:.0f}%: {', '.join(missing_names)}."

        return {
            "allowed": False,
            "target_concept": target_concept,
            "missing_prereqs": missing,
            "warning_message": msg
        }
