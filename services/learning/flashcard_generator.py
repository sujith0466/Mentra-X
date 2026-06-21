"""
Notes -> Flashcards Generator Service (Feature 9 - Phase C)

Converts student notes into a list of QA flashcards using local
rule-based sentence splitting and pattern matching. No paid APIs.
"""

from __future__ import annotations

import re


_SENTENCE_SPLIT = re.compile(r'(?<=[.!?])\s+')


def _clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', (text or '').strip())
    return text.strip(' .;:-')


def _clean_term(term: str) -> str:
    term = _clean_text(term)
    term = re.sub(r'^(the|a|an)\s+', '', term, flags=re.IGNORECASE)
    return term


def _clean_answer(answer: str) -> str:
    answer = _clean_text(answer)
    if not answer:
        return answer
    if answer[0].islower():
        answer = answer[0].upper() + answer[1:]
    return answer


def _make_qa(term: str, answer: str) -> dict | None:
    term = _clean_term(term)
    answer = _clean_answer(answer)

    if not term or not answer:
        return None
    if len(term.split()) > 7:
        return None
    if term.lower() in {'it', 'this', 'that', 'they', 'there'}:
        return None

    return {
        'question': f'What is {term}?',
        'answer': answer,
    }


def generate_flashcards(notes_text: str) -> list[dict]:
    """
    Parse notes text and extract clean Q/A flashcards.

    Supported patterns include:
      - X is Y
      - X refers to Y
      - X: Y / X - Y
    """
    notes_text = (notes_text or '').strip()
    if not notes_text:
        return []

    cards: list[dict] = []
    seen_questions: set[str] = set()

    # 1) Line-based term-definition formats
    kv_pattern = re.compile(r'^\s*([A-Za-z][A-Za-z0-9_ /+-]{0,60})\s*[:\-]\s*(.+)$', re.MULTILINE)
    for match in kv_pattern.finditer(notes_text):
        qa = _make_qa(match.group(1), match.group(2))
        if qa and qa['question'] not in seen_questions:
            cards.append(qa)
            seen_questions.add(qa['question'])

    # 2) Sentence patterns: "X is Y" and "X refers to Y"
    for sentence in _SENTENCE_SPLIT.split(notes_text):
        s = _clean_text(sentence)
        if not s:
            continue

        m_is = re.match(r'^([A-Za-z][A-Za-z0-9_ /+-]{0,60})\s+is\s+(.+)$', s, flags=re.IGNORECASE)
        m_refers = re.match(r'^([A-Za-z][A-Za-z0-9_ /+-]{0,60})\s+refers\s+to\s+(.+)$', s, flags=re.IGNORECASE)

        target = m_is or m_refers
        if target:
            qa = _make_qa(target.group(1), target.group(2))
            if qa and qa['question'] not in seen_questions:
                cards.append(qa)
                seen_questions.add(qa['question'])

    # 3) Fallback: concise recall cards from informative sentences
    if not cards:
        for sentence in _SENTENCE_SPLIT.split(notes_text):
            s = _clean_text(sentence)
            if len(s.split()) >= 5:
                cards.append({
                    'question': 'Explain this concept:',
                    'answer': s,
                })
            if len(cards) >= 10:
                break

    return cards[:20]
