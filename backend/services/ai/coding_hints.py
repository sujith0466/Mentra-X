"""
Real-Time Coding Hints Service (Feature 5 - Phase B)

Provides lightweight, pattern-based coding hints for common programming
mistakes. Returns helpful hints (NOT full solutions) so students learn
to debug on their own.
"""

from __future__ import annotations

import ast
import re


def _normalize_language(language: str) -> str:
    return (language or 'python').strip().lower()


def _add_hint(hints: list[dict], seen: set[str], hint_type: str, message: str) -> None:
    if message not in seen:
        hints.append({'type': hint_type, 'message': message})
        seen.add(message)


def _check_brackets(code: str, language: str, hints: list[dict], seen: set[str]) -> None:
    paren_balance = code.count('(') - code.count(')')
    bracket_balance = code.count('[') - code.count(']')
    brace_balance = code.count('{') - code.count('}')

    if paren_balance != 0:
        _add_hint(hints, seen, 'syntax', "Unmatched parentheses detected. Check '(' and ')' balance.")
    if bracket_balance != 0:
        _add_hint(hints, seen, 'syntax', "Unmatched square brackets detected. Check '[' and ']' balance.")
    if brace_balance != 0 and language not in {'python', 'py'}:
        _add_hint(hints, seen, 'syntax', "Unmatched curly braces detected. Check '{' and '}' balance.")


def _python_regex_checks(code: str, hints: list[dict], seen: set[str]) -> None:
    # Missing colon in Python control/function blocks
    missing_colon = re.compile(r'^\s*(if|elif|else|for|while|def|class|try|except|finally|with)\b[^:\n]*$', re.MULTILINE)
    if missing_colon.search(code):
        _add_hint(hints, seen, 'syntax', "Possible missing ':' at the end of a Python block statement.")

    # Indentation smell: lines that start with odd spaces (1,2,3) or mixed tab+space starts
    if re.search(r'^( {1,3}|\t +)\S', code, re.MULTILINE):
        _add_hint(hints, seen, 'syntax', 'Indentation looks inconsistent. Prefer 4 spaces per Python block level.')


def _python_ast_checks(code: str, hints: list[dict], seen: set[str]) -> None:
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        msg = str(exc).lower()
        if 'expected' in msg and ':' in msg:
            _add_hint(hints, seen, 'syntax', "Python syntax error: expected ':' in a block statement.")
        elif 'indent' in msg:
            _add_hint(hints, seen, 'syntax', 'Python syntax error: indentation issue detected.')
        else:
            _add_hint(hints, seen, 'syntax', f'Python syntax error detected: {exc.msg}.')
        return

    # Infinite loop smell: while True without break/return inside body
    for node in ast.walk(tree):
        if isinstance(node, ast.While) and isinstance(node.test, ast.Constant) and node.test.value is True:
            has_exit = any(isinstance(inner, (ast.Break, ast.Return, ast.Raise)) for inner in ast.walk(ast.Module(body=node.body, type_ignores=[])))
            if not has_exit:
                _add_hint(hints, seen, 'logic', "'while True' loop may be infinite because no break/return/raise was found.")
                break

    # Unused variable smell (module-level heuristic)
    assigned: set[str] = set()
    used: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                assigned.add(node.id)
            elif isinstance(node.ctx, ast.Load):
                used.add(node.id)

    candidates = sorted(v for v in assigned if v not in used and not v.startswith('_'))
    if candidates:
        preview = ', '.join(candidates[:3])
        _add_hint(hints, seen, 'logic', f'Possible unused variable(s): {preview}. Remove them or use them to simplify your code.')


def generate_hint(code: str, language: str = 'python') -> dict:
    """
    Analyse code and return categorized educational hints.

    Returns:
    {
      "hints": [{"type": "syntax|logic|general", "message": "..."}],
      "hint_messages": ["..."],
      "language": "python",
      "total_hints": 2
    }
    """
    code = (code or '').strip()
    language = _normalize_language(language)

    if not code:
        base = {'type': 'general', 'message': 'No code provided. Paste your code to receive hints.'}
        return {
            'hints': [base],
            'hint_messages': [base['message']],
            'language': language,
            'total_hints': 1,
        }

    hints: list[dict] = []
    seen: set[str] = set()

    _check_brackets(code, language, hints, seen)

    if language in {'python', 'py'}:
        _python_regex_checks(code, hints, seen)
        _python_ast_checks(code, hints, seen)
    else:
        # Lightweight non-python checks
        if re.search(r'\bwhile\s*\(\s*true\s*\)', code, re.IGNORECASE) and not re.search(r'\bbreak\b', code):
            _add_hint(hints, seen, 'logic', "'while(true)' may loop forever. Add a break condition.")

    if not hints:
        _add_hint(
            hints,
            seen,
            'general',
            'No common issues detected. Validate edge cases and add test inputs before submitting.'
        )

    return {
        'hints': hints,
        'hint_messages': [item['message'] for item in hints],
        'language': language,
        'total_hints': len(hints),
    }
