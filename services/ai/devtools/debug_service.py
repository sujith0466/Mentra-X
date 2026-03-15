from __future__ import annotations

from typing import Dict


ERROR_KNOWLEDGE = {
    "typeerror": {
        "error_type": "TypeError",
        "explanation": "A TypeError appears when Python receives a value of the wrong type for an operation or function.",
        "cause": "A variable or function argument is being used in a way that expects a different data type.",
        "possible_fix": "Check the variable types before the failing line and convert values explicitly if needed.",
        "corrected_example": "total = int(user_input) + 5",
        "example": "Example: adding an integer to a string. Convert the integer using str() or parse the string with int().",
    },
    "valueerror": {
        "error_type": "ValueError",
        "explanation": "A ValueError means the value format is wrong even though the data type is technically allowed.",
        "cause": "The code is receiving a badly formatted value, such as text where a number is expected.",
        "possible_fix": "Validate or sanitize the input before using it, especially when parsing numbers or dates.",
        "corrected_example": "if raw_value.isdigit():\n    count = int(raw_value)",
        "example": "Example: int('abc') fails because the string cannot be converted into a number.",
    },
    "syntaxerror": {
        "error_type": "SyntaxError",
        "explanation": "A SyntaxError means Python could not understand the code structure before running it.",
        "cause": "There is a malformed statement, missing punctuation, or indentation issue in the source code.",
        "possible_fix": "Review the line number in the error, then check for missing colons, brackets, quotes, or indentation issues.",
        "corrected_example": "if score > 50:\n    print('Pass')",
        "example": "Example: writing if score > 50 without the trailing colon causes a SyntaxError.",
    },
    "indexerror": {
        "error_type": "IndexError",
        "explanation": "An IndexError happens when code tries to access a list position that does not exist.",
        "cause": "The code is requesting an index outside the valid range of the list or sequence.",
        "possible_fix": "Check the list length before indexing or use a loop that stays within valid bounds.",
        "corrected_example": "if index < len(items):\n    print(items[index])",
        "example": "Example: items[5] fails when the list only contains three elements.",
    },
    "keyerror": {
        "error_type": "KeyError",
        "explanation": "A KeyError occurs when code looks for a dictionary key that is not present.",
        "cause": "The code assumes a key exists in a dictionary when it may not have been created yet.",
        "possible_fix": "Use dict.get(), check key existence with in, or ensure the expected key is created earlier.",
        "corrected_example": "github_url = profile.get('github', 'Not provided')",
        "example": "Example: profile['github'] raises KeyError if the dictionary only has name and email.",
    },
}


def explain_error(error_text: str) -> Dict[str, str]:
    normalized = (error_text or "").strip()
    lowered = normalized.lower()

    for error_name, payload in ERROR_KNOWLEDGE.items():
        if error_name in lowered:
            return {
                "error": normalized or payload["error_type"],
                "error_type": payload["error_type"],
                "explanation": payload["explanation"],
                "cause": payload["cause"],
                "possible_fix": payload["possible_fix"],
                "corrected_example": payload["corrected_example"],
                "example": payload["example"],
            }

    return {
        "error": normalized or "Unknown error",
        "error_type": "Runtime Error",
        "explanation": "This error type is not in the current rule-based catalog, but it still looks like a coding or runtime issue.",
        "cause": "The traceback likely points to a failing line, variable, or invalid assumption in the code path.",
        "possible_fix": "Read the traceback from bottom to top, identify the failing file and line, then inspect the variables used there.",
        "corrected_example": "Add logging or print statements around the failing line to inspect variable values before the exception occurs.",
        "example": "Look for the exception name, the file path, and the exact failing line before making a fix.",
    }
