from __future__ import annotations

from typing import Dict, List


def analyze_code_solution(code: str) -> Dict[str, object]:
    source = code or ""
    lowered = source.lower()
    issues: List[str] = []

    nested_loops = source.count("for ") >= 2 or ("while " in source and "for " in source)
    uses_hash_map = "dict(" in lowered or "{}" in source or "set(" in lowered
    returns_placeholder = "pass" in lowered or "todo" in lowered

    if nested_loops and not uses_hash_map:
        complexity_hint = "Your solution appears O(n^2). Consider using a hash map for faster lookup."
        suggestion = "Use a dictionary to store seen values and reduce repeated scans."
    elif uses_hash_map:
        complexity_hint = "Your approach likely benefits from near O(n) lookup performance."
        suggestion = "Keep variable names clear and return as soon as the target match is found."
    else:
        complexity_hint = "Your complexity looks acceptable for small inputs, but watch repeated list scans."
        suggestion = "Look for ways to avoid duplicate work and handle edge cases early."

    if returns_placeholder:
        issues.append("Your code still contains a placeholder like pass or TODO.")
    if "print(" in lowered and "return" not in lowered:
        issues.append("You may be printing results instead of returning them from the function.")
    if "input(" in lowered:
        issues.append("Challenge solutions should avoid interactive input() and rely on function arguments.")
    if "==" not in source and "if " in lowered:
        issues.append("Double-check your condition logic to make sure comparisons are explicit.")

    return {
        "complexity_hint": complexity_hint,
        "suggestion": suggestion,
        "common_mistakes": issues,
    }

