"""Quick smoke test for the orchestrator module."""
from backend.services.ai.orchestrator import detect_intent, get_available_agents

tests = [
    ("I have a Python error",          "debug"),
    ("Suggest a learning path for AI",  "learning"),
    ("How to improve my resume",        "career"),
    ("Give me project ideas",           "project"),
    ("Explain recursion",               "mentor"),
    ("Start mock interview",            "career"),  # 'interview' keyword is under career
    ("Show community questions",        "community"),
]

print("=" * 60)
print("ORCHESTRATOR INTENT DETECTION TEST")
print("=" * 60)

all_pass = True
for message, expected in tests:
    actual = detect_intent(message)
    status = "PASS" if actual == expected else "FAIL"
    if actual != expected:
        all_pass = False
    print(f"  [{status}] \"{message}\" => {actual} (expected: {expected})")

print("-" * 60)
agents = get_available_agents()
print(f"Registered agents: {[a['key'] for a in agents]}")
print(f"All tests passed: {all_pass}")
print("=" * 60)
