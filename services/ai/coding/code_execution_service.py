from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from typing import Dict


EXECUTION_TIMEOUT_SECONDS = 5


def execute_python_code(code: str) -> Dict[str, object]:
    safe_code = code or ""
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as handle:
            handle.write(safe_code)
            temp_path = handle.name

        completed = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=EXECUTION_TIMEOUT_SECONDS,
            check=False,
        )
        output = (completed.stdout or "").strip()
        error = (completed.stderr or "").strip() or None
        return {
            "success": completed.returncode == 0,
            "output": output,
            "error": error,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": f"Execution timed out after {EXECUTION_TIMEOUT_SECONDS} seconds.",
        }
    except Exception as exc:
        return {
            "success": False,
            "output": "",
            "error": str(exc),
        }
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def execute_code(language: str, code: str) -> Dict[str, object]:
    normalized = (language or "python").strip().lower()
    if normalized in {"python", "py"}:
        return execute_python_code(code)
    if normalized in {"javascript", "js"}:
        return {
            "success": False,
            "output": "",
            "error": "JavaScript execution is not available in this environment yet. Please use Python for now.",
        }
    if normalized in {"sql"}:
        return {
            "success": False,
            "output": "",
            "error": "SQL execution is not available in this environment yet. Please use Python for now.",
        }
    return {
        "success": False,
        "output": "",
        "error": "Unsupported language selected. Please use Python.",
    }
