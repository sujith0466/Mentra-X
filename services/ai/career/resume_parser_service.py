from __future__ import annotations

import re
from typing import Dict, List, Iterable

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


def extract_text_from_txt(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as handle:
            return handle.read().strip()
    except Exception:
        return ""


def _split_lines(text: str) -> List[str]:
    return [line.strip() for line in (text or "").splitlines() if line and line.strip()]


def _normalize_line(line: str) -> str:
    cleaned = (line or "").strip()
    cleaned = re.sub(r"^[\-\u2022\u2013\u2014\*\u00b7]+\s*", "", cleaned)
    return cleaned.strip()


def _header_match(line: str, headers: Iterable[str]) -> bool:
    lowered = (line or "").strip().lower().rstrip(":")
    if not lowered:
        return False
    return any(lowered == header or lowered.startswith(header + " ") for header in headers)


def _extract_section(lines: List[str], headers: Iterable[str]) -> List[str]:
    header_set = {header.lower() for header in headers}
    collected: List[str] = []
    active = False
    for raw_line in lines:
        line = _normalize_line(raw_line)
        if _header_match(line, header_set):
            active = True
            continue
        if active and _header_match(line, header_set):
            break
        if active:
            if re.match(r"^[A-Z][A-Za-z\s]{2,}$", line) and len(line) <= 40:
                break
            if line:
                collected.append(line)
    return collected


def _extract_skills(text: str) -> List[str]:
    normalized = (text or "").lower()
    detected = []
    for skill, keywords in SKILL_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            detected.append(skill)
    return sorted(set(detected))


def _split_skill_line(line: str) -> List[str]:
    if not line:
        return []
    tokens = re.split(r"[,;/\|]+", line)
    cleaned = [token.strip(" •\t") for token in tokens if token.strip()]
    normalized = []
    for token in cleaned:
        token = re.sub(r"^skills?\s*:\s*", "", token, flags=re.IGNORECASE)
        if len(token) > 1:
            normalized.append(token)
    return normalized


def _unique_list(items: Iterable[str]) -> List[str]:
    seen = set()
    output = []
    for item in items:
        normalized = item.strip()
        if not normalized or normalized.lower() in seen:
            continue
        seen.add(normalized.lower())
        output.append(normalized)
    return output


def parse_resume(text: str) -> Dict[str, List[str]]:
    lines = _split_lines(text)
    skills = _extract_skills(text)

    skill_section = _extract_section(lines, ["skills", "technical skills", "skill summary", "skills summary", "toolbox"])
    if skill_section:
        parsed_tokens = []
        for line in skill_section:
            parsed_tokens.extend(_split_skill_line(line))
        skills = _unique_list(skills + parsed_tokens)

    projects = _extract_section(lines, ["projects", "project experience", "project work", "academic projects"]) or [
        line for line in lines if any(token in line.lower() for token in ["project", "built", "developed", "implemented"])
    ]
    education = _extract_section(lines, ["education", "academics", "academic background"]) or [
        line for line in lines if any(token in line.lower() for token in ["b.tech", "bachelor", "master", "degree", "university", "college"])
    ]
    experience = _extract_section(lines, ["experience", "work experience", "professional experience", "employment", "internship"]) or [
        line for line in lines if any(token in line.lower() for token in ["intern", "internship", "experience", "company", "employment"])
    ]

    return {
        "skills": _unique_list(skills)[:24],
        "projects": _unique_list([_normalize_line(item) for item in projects])[:8],
        "education": _unique_list([_normalize_line(item) for item in education])[:6],
        "experience": _unique_list([_normalize_line(item) for item in experience])[:8],
    }
