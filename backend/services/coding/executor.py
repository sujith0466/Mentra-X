import os
import subprocess
import sys
import tempfile
import sqlite3
import shutil
from typing import Dict, Any

EXECUTION_TIMEOUT_SECONDS = 3

def execute_python_code(code: str, input_str: str = "") -> Dict[str, Any]:
    sandbox_prologue = """
import sys
for mod in ['os', 'sys', 'subprocess', 'shutil', 'socket']:
    sys.modules[mod] = None
del sys
"""
    safe_code = sandbox_prologue + "\n" + (code or "")
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as handle:
            handle.write(safe_code)
            temp_path = handle.name

        completed = subprocess.run(
            [sys.executable, temp_path],
            input=input_str,
            capture_output=True,
            text=True,
            timeout=EXECUTION_TIMEOUT_SECONDS,
            check=False,
        )
        return {
            "success": completed.returncode == 0,
            "output": (completed.stdout or "").strip(),
            "error": (completed.stderr or "").strip() or None,
            "returncode": completed.returncode
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

def execute_javascript_code(code: str, input_str: str = "") -> Dict[str, Any]:
    safe_code = code or ""
    temp_path = None
    node_path = shutil.which("node")
    if not node_path:
        return {
             "success": False,
             "output": "",
             "error": "Node.js is not installed or not in PATH. JavaScript execution is unavailable.",
             "returncode": -1
        }

    try:
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as handle:
            handle.write(safe_code)
            temp_path = handle.name

        completed = subprocess.run(
            [node_path, temp_path],
            input=input_str,
            capture_output=True,
            text=True,
            timeout=EXECUTION_TIMEOUT_SECONDS,
            check=False,
        )
        return {
            "success": completed.returncode == 0,
            "output": (completed.stdout or "").strip(),
            "error": (completed.stderr or "").strip() or None,
            "returncode": completed.returncode
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

def execute_sql_code(code: str, setup_sql: str = "") -> Dict[str, Any]:
    # Prevent escaping the memory sandbox
    sanitized_code = code.translate(str.maketrans('','')).replace("ATTACH", "--").replace("PRAGMA", "--").replace("attach", "--").replace("pragma", "--")
    
    # Runs SQL against an in-memory SQLite database
    try:
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Setup schema if provided
        if setup_sql:
            cursor.executescript(setup_sql)
            
        # Execute user code
        output_rows = []
        statements = [s.strip() for s in sanitized_code.split(";") if s.strip()]
        for stmt in statements:
            cursor.execute(stmt)
            if stmt.upper().startswith("SELECT"):
                rows = cursor.fetchall()
                if rows:
                    columns = rows[0].keys()
                    header = " | ".join(columns)
                    output_rows.append(header)
                    output_rows.append("-" * len(header))
                    for row in rows:
                        output_rows.append(" | ".join(str(row[c]) for c in columns))
                else:
                    output_rows.append("No results.")
            else:
                conn.commit()
                if cursor.rowcount > 0:
                     output_rows.append(f"Query OK, {cursor.rowcount} rows affected.")
                
        output_str = "\n".join(output_rows)
        return {
            "success": True,
            "output": output_str,
            "error": None,
            "returncode": 0
        }
        
    except sqlite3.Error as e:
         return {
            "success": False,
            "output": "",
            "error": f"SQL Error: {str(e)}",
            "returncode": 1
        }
    finally:
         try:
            conn.close()
         except:
            pass

def execute_code(language: str, code: str, input_str: str = "") -> Dict[str, Any]:
    normalized = (language or "python").strip().lower()
    if normalized in {"python", "py"}:
        return execute_python_code(code, input_str)
    if normalized in {"javascript", "js", "node"}:
        return execute_javascript_code(code, input_str)
    if normalized in {"sql"}:
        return execute_sql_code(code, setup_sql=input_str)
    return {
        "success": False,
        "output": "",
        "error": f"Unsupported language: {language}. Please use python, javascript, or sql.",
    }
