from __future__ import annotations

import ast
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from backend.models import CodingChallenge, CodingSubmission, SkillProgress, db
from backend.services.ai.coding.code_execution_service import execute_code, execute_python_code


def get_coding_challenges(topic: Optional[str] = None) -> List[CodingChallenge]:
    query = CodingChallenge.query
    if topic:
        query = query.filter(CodingChallenge.topic.ilike(topic))
    return query.order_by(CodingChallenge.created_at.desc(), CodingChallenge.id.desc()).all()


def _extract_function_name(code: str) -> Optional[str]:
    try:
        module = ast.parse(code or "")
    except SyntaxError:
        return None

    for node in module.body:
        if isinstance(node, ast.FunctionDef):
            return node.name
    return None


def _needs_base_execution(code: str) -> bool:
    try:
        module = ast.parse(code or "")
    except SyntaxError:
        return True

    for index, node in enumerate(module.body):
        if isinstance(node, ast.Expr) and index == 0 and isinstance(getattr(node, "value", None), ast.Constant) and isinstance(node.value.value, str):
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom)):
            continue
        return True
    return False


def _parse_test_case_input(raw_input: str) -> Tuple[tuple, dict]:
    if raw_input is None or raw_input == "":
        return tuple(), {}

    wrapped = f"({raw_input})"
    parsed = ast.literal_eval(wrapped)
    if isinstance(parsed, tuple):
        return parsed, {}
    return (parsed,), {}


def _normalize_result(value):
    if isinstance(value, tuple):
        return list(value)
    return value


def _invoke_submission(code: str, function_name: str, raw_input: str) -> Dict[str, object]:
    try:
        args, kwargs = _parse_test_case_input(raw_input)
    except Exception as exc:
        return {"success": False, "result": None, "error": f"Invalid test case input: {exc}"}

    invocation_script = (
        "import json\n\n"
        + (code or "").strip()
        + "\n\n"
        + f"__challenge_args__ = {repr(args)}\n"
        + f"__challenge_kwargs__ = {repr(kwargs)}\n"
        + f"__challenge_result__ = {function_name}(*__challenge_args__, **__challenge_kwargs__)\n"
        + "print(json.dumps(__challenge_result__))\n"
    )
    execution = execute_python_code(invocation_script)
    if not execution["success"]:
        return {"success": False, "result": None, "error": execution["error"] or execution["output"]}

    output = execution["output"] or ""
    try:
        return {"success": True, "result": json.loads(output), "error": None}
    except json.JSONDecodeError:
        return {"success": True, "result": output, "error": None}


def evaluate_submission(code: str, challenge: CodingChallenge, language: str = "python") -> Dict[str, object]:
    code = code or ""
    normalized_language = (language or "python").strip().lower()
    if normalized_language not in {"python", "py"}:
        execution = execute_code(normalized_language, code)
        return {
            "passed_tests": 0,
            "total_tests": len(challenge.get_test_cases()),
            "score": 0,
            "execution_output": execution.get("output", ""),
            "error": execution.get("error") or "Only Python challenges support automated tests right now.",
            "results": [],
        }

    function_name = _extract_function_name(code)
    test_cases = challenge.get_test_cases()
    results: List[Dict[str, object]] = []
    passed_tests = 0
    execution_output = ""

    if not function_name:
        base_run = execute_python_code(code)
        return {
            "passed_tests": 0,
            "total_tests": len(test_cases),
            "score": 0,
            "execution_output": base_run.get("output", ""),
            "error": "No callable function definition was found in the submitted code.",
            "results": results,
        }

    if _needs_base_execution(code):
        base_run = execute_python_code(code)
        execution_output = base_run.get("output", "")
        if not base_run["success"] and base_run.get("error"):
            return {
                "passed_tests": 0,
                "total_tests": len(test_cases),
                "score": 0,
                "execution_output": execution_output,
                "error": base_run["error"],
                "results": results,
            }

    for test_case in test_cases:
        invocation = _invoke_submission(code, function_name, test_case.get("input", ""))
        expected_raw = test_case.get("output")
        try:
            expected = ast.literal_eval(expected_raw) if expected_raw is not None else expected_raw
        except Exception:
            expected = expected_raw

        actual = _normalize_result(invocation.get("result"))
        expected = _normalize_result(expected)
        passed = invocation["success"] and actual == expected
        if passed:
            passed_tests += 1

        results.append(
            {
                "input": test_case.get("input", ""),
                "expected": expected,
                "actual": actual,
                "passed": passed,
                "error": invocation.get("error"),
            }
        )

    total_tests = len(test_cases)
    score = round((passed_tests / total_tests) * 100, 2) if total_tests else 0.0
    return {
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "score": score,
        "execution_output": execution_output,
        "error": None,
        "results": results,
    }


def create_submission(user_id: int, challenge: CodingChallenge, code: str, evaluation: Dict[str, object]) -> CodingSubmission:
    submission = CodingSubmission(
        user_id=user_id,
        challenge_id=challenge.id,
        code_submitted=code,
        execution_output=evaluation.get("execution_output") or evaluation.get("error") or "",
        passed_tests=int(evaluation.get("passed_tests") or 0),
        score=float(evaluation.get("score") or 0.0),
        submitted_at=datetime.utcnow(),
    )
    db.session.add(submission)
    db.session.commit()
    return submission


def get_or_create_skill_progress(user_id: int, skill_name: str) -> SkillProgress:
    row = SkillProgress.query.filter_by(user_id=user_id, skill_name=skill_name).first()
    if not row:
        row = SkillProgress(user_id=user_id, skill_name=skill_name, progress_percentage=0.0)
        db.session.add(row)
    return row


def update_skill_progress_for_challenge(user_id: int, challenge: CodingChallenge, score: float) -> SkillProgress:
    row = get_or_create_skill_progress(user_id, challenge.topic)
    row.progress_percentage = min(100.0, round(max(row.progress_percentage, float(score or 0.0)), 2))
    row.last_updated = datetime.utcnow()
    db.session.commit()
    return row


def get_coding_results_summary(submission: CodingSubmission) -> Dict[str, object]:
    challenge = submission.challenge
    return {
        "submission_id": submission.id,
        "challenge_title": challenge.title if challenge else "Coding Challenge",
        "topic": challenge.topic if challenge else "",
        "score": submission.score,
        "passed_tests": submission.passed_tests,
        "total_tests": len(challenge.get_test_cases()) if challenge else 0,
        "execution_output": submission.execution_output,
    }
