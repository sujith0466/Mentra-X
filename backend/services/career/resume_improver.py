"""
AI Resume Improver — Service  (Feature 8 — Phase B)

Analyses raw resume text and returns:
  • improved_text  — a rewritten version with stronger phrasing
  • suggestions    — actionable improvement bullets

All logic is local pattern matching / heuristics — NO paid APIs.
"""

from __future__ import annotations

import re


# ---------------------------------------------------------------------------
# Weak → strong phrasing replacements
# ---------------------------------------------------------------------------

_WEAK_PHRASES: list[tuple[re.Pattern, str, str]] = [
    # (regex, replacement, suggestion note)
    (re.compile(r'\bhelped build\b', re.IGNORECASE),
     'Engineered', 'Use stronger ownership language like "Engineered" when describing what you built.'),
    (re.compile(r'\bresponsible for\b', re.IGNORECASE),
     'Led', 'Replace "responsible for" with action verbs like "Led", "Managed", or "Drove".'),
    (re.compile(r'\bhelped\b', re.IGNORECASE),
     'Assisted in', 'Replace vague "helped" with specific contributions like "Assisted in", "Facilitated", or "Enabled".'),
    (re.compile(r'\bworked on\b', re.IGNORECASE),
     'Developed', 'Replace "worked on" with concrete action verbs like "Developed", "Engineered", or "Designed".'),
    (re.compile(r'\bdid\b', re.IGNORECASE),
     'Executed', '"Did" is too vague. Use "Executed", "Implemented", or "Completed".'),
    (re.compile(r'\bmade\b', re.IGNORECASE),
     'Created', 'Replace "made" with "Created", "Built", or "Designed" for stronger impact.'),
    (re.compile(r'\btried to\b', re.IGNORECASE),
     'Worked towards', 'Avoid "tried to" — it implies failure. Reframe as "Worked towards" or remove it.'),
    (re.compile(r'\bused\b', re.IGNORECASE),
     'Leveraged', 'Replace generic "used" with "Leveraged", "Utilized", or "Applied".'),
    (re.compile(r'\bgood at\b', re.IGNORECASE),
     'Proficient in', '"Good at" is informal. Use "Proficient in", "Expert in", or "Skilled in".'),
    (re.compile(r'\bteam player\b', re.IGNORECASE),
     'Collaborative professional',
     '"Team player" is overused. Show collaboration through specific achievements.'),
    (re.compile(r'\bhard worker\b', re.IGNORECASE),
     'Dedicated professional',
     '"Hard worker" is generic. Demonstrate dedication through results and metrics.'),
    (re.compile(r'\blearned\b', re.IGNORECASE),
     'Acquired expertise in',
     'Replace "learned" with "Acquired expertise in" or "Mastered" for a professional tone.'),
    (re.compile(r'\bvarious\b', re.IGNORECASE),
     'multiple',
     '"Various" is vague — quantify instead (e.g. "5 projects" instead of "various projects").'),
]


# ---------------------------------------------------------------------------
# Section detection heuristics
# ---------------------------------------------------------------------------

_EXPECTED_SECTIONS = {
    'contact':    re.compile(r'\b(email|phone|address|linkedin|github|contact)\b', re.IGNORECASE),
    'summary':    re.compile(r'\b(summary|objective|profile|about me)\b', re.IGNORECASE),
    'experience': re.compile(r'\b(experience|work history|employment|professional)\b', re.IGNORECASE),
    'education':  re.compile(r'\b(education|degree|university|college|school|academic)\b', re.IGNORECASE),
    'skills':     re.compile(r'\b(skills|technologies|tech stack|technical skills|competencies)\b', re.IGNORECASE),
    'projects':   re.compile(r'\b(project|portfolio|personal project|open source)\b', re.IGNORECASE),
    'certifications': re.compile(r'\b(certification|certificate|license|accreditation)\b', re.IGNORECASE),
}


def _detect_present_sections(text: str) -> tuple[set[str], set[str]]:
    """Return (found_sections, missing_sections)."""
    found: set[str] = set()
    for name, pattern in _EXPECTED_SECTIONS.items():
        if pattern.search(text):
            found.add(name)
    missing = set(_EXPECTED_SECTIONS.keys()) - found
    return found, missing


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def improve_resume(resume_text: str) -> dict:
    """
    Analyse and improve raw resume text.

    Returns
    -------
    dict
        {
            "improved_text": str,
            "suggestions": [str, ...],
            "sections_found": [str, ...],
            "sections_missing": [str, ...],
            "weak_phrases_replaced": int,
        }
    """
    resume_text = (resume_text or '').strip()

    if not resume_text:
        return {
            'improved_text': '',
            'suggestions': ['No resume text provided. Paste your resume to get improvement suggestions.'],
            'sections_found': [],
            'sections_missing': list(_EXPECTED_SECTIONS.keys()),
            'weak_phrases_replaced': 0,
        }

    improved = resume_text
    suggestions: list[str] = []
    seen_suggestions: set[str] = set()
    replacements_count = 0

    # --- Apply phrasing improvements ---
    for pattern, replacement, suggestion in _WEAK_PHRASES:
        if pattern.search(improved):
            improved = pattern.sub(replacement, improved, count=0)
            replacements_count += 1
            if suggestion not in seen_suggestions:
                suggestions.append(suggestion)
                seen_suggestions.add(suggestion)

    # --- Section analysis ---
    found_sections, missing_sections = _detect_present_sections(resume_text)

    if 'summary' in missing_sections:
        suggestions.append(
            "Add a professional Summary / Objective section at the top of your resume. "
            "A 2–3 sentence overview makes a strong first impression."
        )
    if 'skills' in missing_sections:
        suggestions.append(
            "Add a Skills / Technologies section listing your technical competencies. "
            "Use bullet points or a comma-separated list."
        )
    if 'projects' in missing_sections:
        suggestions.append(
            "Include a Projects section to showcase hands-on experience, especially "
            "if you have limited work experience."
        )
    if 'certifications' in missing_sections:
        suggestions.append(
            "Consider adding a Certifications section if you have any relevant "
            "certifications (e.g. AWS, PMP, Google)."
        )

    # --- Quantification check ---
    has_numbers = bool(re.search(r'\b\d+[%+]?\b', resume_text))
    if not has_numbers:
        suggestions.append(
            "Your resume lacks quantified achievements. Add metrics like "
            "\"Increased sales by 20%\" or \"Managed a team of 5\" to increase impact."
        )

    # --- Length check ---
    word_count = len(resume_text.split())
    if word_count < 100:
        suggestions.append(
            f"Your resume seems short ({word_count} words). Aim for 300–600 words "
            "to adequately cover your experience and skills."
        )
    elif word_count > 1000:
        suggestions.append(
            f"Your resume is quite long ({word_count} words). Consider trimming to "
            "1–2 pages for maximum recruiter impact."
        )

    # --- Bullet point check ---
    bullet_count = len(re.findall(r'^\s*[-•*]', resume_text, re.MULTILINE))
    if bullet_count < 3:
        suggestions.append(
            "Use bullet points for experience and achievements. "
            "Bullet points improve readability and help recruiters scan quickly."
        )

    # --- Action verbs in experience ---
    action_verbs = re.findall(
        r'\b(Developed|Designed|Implemented|Managed|Led|Built|Deployed|Optimized|'
        r'Created|Delivered|Reduced|Improved|Achieved|Increased|Streamlined)\b',
        resume_text, re.IGNORECASE
    )
    if len(action_verbs) < 2:
        suggestions.append(
            "Start your experience bullet points with strong action verbs "
            "(Developed, Managed, Designed, Implemented, etc.)."
        )

    # Always include core actionable guidance for students.
    baseline_actions = [
        "Add measurable achievements (e.g., percentages, time saved, users impacted).",
        "Use strong action verbs at the start of each bullet point.",
        "Include a technical skills section grouped by tools/languages/frameworks.",
    ]
    for item in baseline_actions:
        if item not in suggestions:
            suggestions.append(item)

    # Fallback
    if not suggestions:
        suggestions.append("Your resume looks good! Consider having a peer review it for final polish.")

    return {
        'improved_text': improved,
        'suggestions': suggestions,
        'sections_found': sorted(found_sections),
        'sections_missing': sorted(missing_sections),
        'weak_phrases_replaced': replacements_count,
    }
