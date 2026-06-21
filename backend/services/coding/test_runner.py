import ast
import json
from typing import Dict, List, Any
from backend.services.coding.executor import execute_code

def _extract_python_function_name(code: str) -> str:
    try:
        module = ast.parse(code or "")
        for node in module.body:
            if isinstance(node, ast.FunctionDef):
                return node.name
    except SyntaxError:
        pass
    return ""

def _parse_test_case_input(raw_input: str) -> tuple:
    if raw_input is None or raw_input == "":
        return tuple(), {}
    try:
        wrapped = f"({raw_input})"
        parsed = ast.literal_eval(wrapped)
        if isinstance(parsed, tuple):
            return parsed, {}
        return (parsed,), {}
    except:
        return (raw_input,), {}

def run_tests(code: str, language: str, test_cases: List[Dict]) -> Dict[str, Any]:
    normalized_lang = language.lower().strip()
    passed_tests = 0
    total_tests = len(test_cases)
    results = []

    if total_tests == 0:
        base_run = execute_code(normalized_lang, code, "")
        return {
            "passed_tests": 0,
            "total_tests": 0,
            "score": 0.0,
            "execution_output": base_run.get("output", ""),
            "error": base_run.get("error"),
            "results": []
        }

    # For Python
    if normalized_lang in {"python", "py"}:
        function_name = _extract_python_function_name(code)
        if not function_name:
             base_run = execute_code(normalized_lang, code, "")
             return {
                "passed_tests": 0,
                "total_tests": total_tests,
                "score": 0.0,
                "execution_output": base_run.get("output", ""),
                "error": "No callable function definition was found in the submitted code. Cannot run tests.",
                "results": []
            }
            
        for test in test_cases:
            raw_input = test.get("input", "")
            raw_output = test.get("output", "")
            
            try:
                args, kwargs = _parse_test_case_input(raw_input)
            except:
                args, kwargs = (), {}

            invocation_script = (
                "import json\n\n"
                + (code or "").strip()
                + "\n\n"
                + f"__res__ = {function_name}(*{(args)}, **{(kwargs)})\n"
                + "print(json.dumps(__res__))\n"
            )
            
            run_res = execute_code("python", invocation_script)
            
            # evaluate
            try:
                expected = ast.literal_eval(raw_output) if raw_output is not None else raw_output
            except:
                expected = raw_output
                
            actual = None
            if run_res["success"]:
                 try:
                     actual = json.loads(run_res["output"])
                 except:
                     actual = run_res["output"]
                     
            passed = run_res["success"] and (actual == expected or str(actual) == str(expected))
            if passed:
                passed_tests += 1
                
            results.append({
                "input": raw_input,
                "expected": expected,
                "actual": actual,
                "passed": passed,
                "error": run_res["error"]
            })
            
    elif normalized_lang in {"javascript", "js", "node"}:
        # basic text match for JS output
         for test in test_cases:
             raw_input = test.get("input", "")
             raw_output = str(test.get("output", ""))
             
             # Instead of analyzing AST, just run code with input injected
             # This is a basic harness
             run_res = execute_code("javascript", code, raw_input)
             actual = run_res["output"]
             
             passed = run_res["success"] and (actual.strip() == raw_output.strip())
             if passed: passed_tests += 1
             results.append({
                "input": raw_input,
                "expected": raw_output,
                "actual": actual,
                "passed": passed,
                "error": run_res["error"]
             })
             
    elif normalized_lang == "sql":
        # we will define the input as setup_sql and expected as expected_output.
        # But for SQL, standard test cases might not work cleanly. We fall back to standard execution comparing to output.
        for test in test_cases:
             raw_input = test.get("input", "") # setup sql
             raw_output = test.get("output", "") # expected output
             
             run_res = execute_code("sql", code, raw_input)
             actual = run_res["output"]
             
             # rough match
             passed = run_res["success"] and (raw_output.strip() in actual.strip() or raw_output.strip() == "")
             if passed: passed_tests += 1
             
             results.append({
                "input": raw_input,
                "expected": raw_output,
                "actual": actual,
                "passed": passed,
                "error": run_res["error"]
             })

    score = round((passed_tests / total_tests) * 100, 2) if total_tests > 0 else 0.0
    
    # Do a base run for execution output context
    base_run = execute_code(normalized_lang, code)
    
    return {
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "score": score,
        "execution_output": base_run.get("output", ""),
        "error": base_run.get("error"),
        "results": results
    }
