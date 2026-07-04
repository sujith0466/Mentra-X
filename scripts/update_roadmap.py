import os
import re

roadmap_dir = r"Docs\Roadmap"

replacements = {
    # File name -> array of tuples (old, new)
    "Phase-07-Enkrypt-Safety.md": [
        ("Phase 6 — Enkrypt Safety Layer", "Phase 7 — Enkrypt Safety Layer"),
        ("Phase 6 of 10", "Phase 7 of 11"),
        ("| **Phase** | 6 |", "| **Phase** | 7 |"),
        ("Awaiting Phase 5 (Adaptive Intelligence)", "Awaiting Phase 6 (Adaptive Learning Intelligence)"),
        ("Phase 6 is the final defensive line", "Phase 7 is the final defensive line"),
        ("**Layer 6 — Enkrypt Safety**", "**Layer 7 — Enkrypt Safety**")
    ],
    "Phase-08-Weakness-Intelligence.md": [
        ("Phase 7 — Weakness Intelligence", "Phase 8 — Weakness Intelligence"),
        ("Phase 7 of 10", "Phase 8 of 11"),
        ("| **Phase** | 7 |", "| **Phase** | 8 |"),
        ("Awaiting Phase 6 (Enkrypt Safety)", "Awaiting Phase 7 (Enkrypt Safety)"),
        ("**Layer 7 — Continuous Learning**", "**Layer 8 — Continuous Learning**")
    ],
    "Phase-09-Autonomous-Learning.md": [
        ("Phase 8 — Autonomous Learning", "Phase 9 — Autonomous Learning"),
        ("Phase 8 of 10", "Phase 9 of 11"),
        ("| **Phase** | 8 |", "| **Phase** | 9 |"),
        ("Awaiting Phase 7 (Weakness Intelligence)", "Awaiting Phase 8 (Weakness Intelligence)"),
        ("**Layer 8 — Intelligence Layer**", "**Layer 9 — Intelligence Layer**")
    ],
    "Phase-10-Opportunity-Intelligence.md": [
        ("Phase 9 — Opportunity Intelligence", "Phase 10 — Opportunity Intelligence"),
        ("Phase 9 of 10", "Phase 10 of 11"),
        ("| **Phase** | 9 |", "| **Phase** | 10 |"),
        ("Awaiting Phase 8 (Autonomous Learning)", "Awaiting Phase 9 (Autonomous Learning)"),
        ("**Layer 9 — Student Experience**", "**Layer 10 — Student Experience**")
    ],
    "Phase-11-Hackathon-Submission.md": [
        ("Phase 10 — Hackathon Submission", "Phase 11 — Hackathon Submission"),
        ("Phase 10 of 10", "Phase 11 of 11"),
        ("| **Phase** | 10 |", "| **Phase** | 11 |"),
        ("Awaiting Phase 9 (Opportunity Intelligence)", "Awaiting Phase 10 (Opportunity Intelligence)"),
        ("**Layer 10 — Production Readiness**", "**Layer 11 — Production Readiness**")
    ]
}

def update_file(filepath, rep_list):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, not found.")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for old, new in rep_list:
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

for filename, reps in replacements.items():
    path = os.path.join(roadmap_dir, filename)
    update_file(path, reps)

# Also update README.md, GOVERNANCE.md, and SYSTEM_ARCHITECTURE.md to reflect new phase numbers
global_reps = [
    ("Phase 6 (Enkrypt Safety)", "Phase 7 (Enkrypt Safety)"),
    ("Phase 7 (Continuous Learning)", "Phase 8 (Continuous Learning)"),
    ("Phase 8 (Intelligence Layer)", "Phase 9 (Intelligence Layer)"),
    ("Phase 9 (Student Experience)", "Phase 10 (Student Experience)"),
    ("Phase 10 (Production Readiness)", "Phase 11 (Production Readiness)"),
    
    ("Phase-06-Enkrypt-Safety", "Phase-07-Enkrypt-Safety"),
    ("Phase-07-Weakness-Intelligence", "Phase-08-Weakness-Intelligence"),
    ("Phase-08-Autonomous-Learning", "Phase-09-Autonomous-Learning"),
    ("Phase-09-Opportunity-Intelligence", "Phase-10-Opportunity-Intelligence"),
    ("Phase-10-Hackathon-Submission", "Phase-11-Hackathon-Submission"),
    
    ("| Phase 6 | Enkrypt Safety Layer |", "| Phase 7 | Enkrypt Safety Layer |"),
    ("| Phase 7 | Intelligence Layer |", "| Phase 8 | Intelligence Layer |"),
    ("| Phase 8 | Student Experience Layer |", "| Phase 9 | Student Experience Layer |"),
    ("| Phase 9 | Production Readiness |", "| Phase 10 | Production Readiness |"),
    
    ("**Phase 6:** Enkrypt Safety Layer", "**Phase 7:** Enkrypt Safety Layer"),
    ("**L7** | Enkrypt Safety Layer | Phase 7", "**L7** | Enkrypt Safety Layer | Phase 7"),
    ("**L8** | Intelligence Layer | Phase 8", "**L8** | Intelligence Layer | Phase 8"),
    ("**L9** | Student Experience | Phase 9", "**L9** | Student Experience | Phase 9"),
    ("**L10** | Production Readiness | Phase 10", "**L11** | Production Readiness | Phase 11"),
    
    ("Phase 7 | Enkrypt Safety Layer", "Phase 7 | Enkrypt Safety Layer"),
    ("Phase 8 | Intelligence Layer", "Phase 8 | Intelligence Layer"),
    ("Phase 9 | Student Experience Layer", "Phase 9 | Student Experience Layer"),
    ("Phase 10 | Production Readiness", "Phase 11 | Production Readiness"),
]

for doc in ["README.md", "Docs\\Roadmap\\GOVERNANCE.md", "Docs\\Architecture\\SYSTEM_ARCHITECTURE.md"]:
    update_file(doc, global_reps)

# Fix phase table in GOVERNANCE.md manually due to possible formatting issues
gov_path = "Docs\\Roadmap\\GOVERNANCE.md"
with open(gov_path, 'r', encoding='utf-8') as f:
    gov = f.read()

gov = gov.replace("| Phase 8 | Intelligence Layer | 🔴 NOT STARTED | 0% |", "| Phase 9 | Intelligence Layer | 🔴 NOT STARTED | 0% |")
gov = gov.replace("| Phase 9 | Student Experience Layer | 🔴 NOT STARTED | 0% |", "| Phase 10 | Student Experience Layer | 🔴 NOT STARTED | 0% |")
gov = gov.replace("| Phase 10 | Production Readiness | 🔴 NOT STARTED | 0% |", "| Phase 11 | Production Readiness | 🔴 NOT STARTED | 0% |")

gov = gov.replace("| **L8** | Intelligence Layer | Phase 8 |", "| **L8** | Intelligence Layer | Phase 9 |")
gov = gov.replace("| **L9** | Student Experience | Phase 9 |", "| **L9** | Student Experience | Phase 10 |")
gov = gov.replace("| **L10** | Production Readiness | Phase 10 |", "| **L10** | Production Readiness | Phase 11 |")

gov = gov.replace("| Phase 7 | `Docs/Roadmap/Phase-06-Enkrypt-Safety.md` |", "| Phase 7 | `Docs/Roadmap/Phase-07-Enkrypt-Safety.md` |")
gov = gov.replace("| Phase 8 | `Docs/Roadmap/Phase-07-Weakness-Intelligence.md` |", "| Phase 8 | `Docs/Roadmap/Phase-08-Weakness-Intelligence.md` |")
gov = gov.replace("| Phase 9 | `Docs/Roadmap/Phase-08-Autonomous-Learning.md` |", "| Phase 9 | `Docs/Roadmap/Phase-09-Autonomous-Learning.md` |")
gov = gov.replace("| Phase 10 | `Docs/Roadmap/Phase-09-Opportunity-Intelligence.md` |", "| Phase 10 | `Docs/Roadmap/Phase-10-Opportunity-Intelligence.md` |")
gov = gov.replace("| Phase 11 | `Docs/Roadmap/Phase-10-Hackathon-Submission.md` |", "| Phase 11 | `Docs/Roadmap/Phase-11-Hackathon-Submission.md` |")

with open(gov_path, 'w', encoding='utf-8') as f:
    f.write(gov)
