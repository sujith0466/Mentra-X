from __future__ import annotations

import re
from typing import Dict, List

from services.ai.career.resume_service import SKILL_KEYWORDS


def extract_text_from_pdf(file_path: str) -> str:
    try:
        import pdfplumber
    except Exception:
        return ""

    try:
        text_chunks: List[str] = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                if page_text:
                    text_chunks.append(page_text)
        return "\n".join(text_chunks).strip()
    except Exception:
        return ""


def extract_text_from_docx(file_path: str) -> str:
    try:
        import docx
    except Exception:
        return ""

    try:
        document = docx.Document(file_path)
        return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text).strip()
    except Exception:
        return ""


def _split_lines(text: str) -> List[str]:
    return [line.strip() for line in (text or "").splitlines() if line.strip()]


def _extract_section(lines: List[str], header: str) -> List[str]:
    header_lower = header.lower()
    collected: List[str] = []
    active = False
    for line in lines:
        lower = line.lower()
        if header_lower in lower and len(lower) <= len(header_lower) + 8:
            active = True
            continue
        if active:
            if re.match(r"^[A-Z][A-Za-z\s]{2,}$", line) and len(line) <= 40:
                break
            collected.append(line)
    return collected


def _extract_skills(text: str) -> List[str]:
    normalized = (text or "").lower()
    detected = []
    for skill, keywords in SKILL_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            detected.append(skill)
    return sorted(set(detected))


def parse_resume(text: str) -> Dict[str, List[str]]:
    lines = _split_lines(text)
    skills = _extract_skills(text)

    projects = _extract_section(lines, "projects") or [
        line for line in lines if any(token in line.lower() for token in ["project", "built", "developed"])
    ]
    education = _extract_section(lines, "education") or [
        line for line in lines if any(token in line.lower() for token in ["b.tech", "bachelor", "master", "degree", "university"])
    ]
    experience = _extract_section(lines, "experience") or [
        line for line in lines if any(token in line.lower() for token in ["intern", "internship", "experience", "company"])
    ]

    return {
        "skills": skills[:20],
        "projects": projects[:8],
        "education": education[:6],
        "experience": experience[:8],
    }
