# Mentra X — Master Project Governance

**Version:** 2.0 (Post Round-1 + Engineering Enhancement)  
**Owner:** Sujith Kumar AI  
**Applies to:** All backend, frontend, and documentation work in the Mentra X repository.

---

## Engineering Documentation Index

| Document | Location | Purpose |
|---|---|---|
| Engineering Standards | `Docs/Engineering/STANDARDS.md` | Naming, Python style, git, PR/review checklists |
| Feature Flags | `Docs/Engineering/FEATURE_FLAGS.md` | Runtime feature control + rollout strategy |
| Event-Driven Architecture | `Docs/Engineering/EVENT_DRIVEN_ARCHITECTURE.md` | Event bus, event catalog, producer/consumer map |
| AI Observability | `Docs/Engineering/AI_OBSERVABILITY.md` | Agent tracing, metrics, observability dashboard |
| Prompt Versioning | `Docs/Engineering/PROMPT_VERSIONING.md` | Prompt lifecycle, file format, loader, registry |
| Shared DTOs | `Docs/Engineering/SHARED_DTOS.md` | All data transfer objects with validation |
| Performance & Security | `Docs/Engineering/PERFORMANCE_AND_SECURITY.md` | Latency targets, RBAC, secrets, monitoring |
| ADR Index | `Docs/ADR/` | Architecture Decision Records (ADR-001 through ADR-008) |
| Error Catalog | `Docs/Errors/ERROR_CATALOG.md` | All error codes with recovery steps |
| Developer Guide | `Docs/Playbooks/DEVELOPER_GUIDE.md` | Setup, debugging, adding features |
| Deployment Guide | `Docs/Playbooks/DEPLOYMENT_GUIDE.md` | Docker, manual, rollback |
| Testing Guide | `Docs/Playbooks/TESTING_GUIDE.md` | Unit, integration, E2E, load testing |
| Demo Playbook | `Docs/Demo/Round2_Demo_Playbook.md` | 5-minute judge demo script |

---

## API Versioning Policy
- **Major (v1, v2):** Breaking changes (e.g., removing endpoints, changing request/response schemas). Must include migration guides.
- **Minor (v1.1, v1.2):** Non-breaking changes (e.g., adding fields, new optional parameters).
- **Patch (v1.1.1):** Backend fixes that do not change contract.
- **Rules:** All new API endpoints MUST be versioned via URL prefix `/api/vX/`.

---

## Phase Progress Dashboard Template
*Copy this into `Docs/Roadmap/Phase-XX-Name.md` for every phase:*

```
## Phase Summary
- **Status:** [ ] TODO / [ ] IN-PROGRESS / [ ] DONE
- **Owner:** [Assignee]
- **Deadline:** [YYYY-MM-DD]

## Tasks
- [ ] Task 1
- [ ] Task 2

## Risks/Dependencies
- None.
```

---

## Source of Truth Priority Order

When making any implementation decision, follow this priority order:

1. This governance document + Updated Project Context
2. `Docs/Round-1/Technical_Architecture.md` (Round-1 submission)
3. `Docs/Round-1/PRD.md` (Round-1 submission)
4. `Docs/Round-1/Supporting_Document.md` (Round-1 submission)
5. Existing Mentra platform (production code)
6. Phase documents in `Docs/Roadmap/` (this folder)

> Older roadmaps, `Docs/Architecture-Research/`, and `Docs/v1_archive/` are **reference only**. They do not override the above.

---

## Non-Negotiable Rules

```
✓ DO preserve all existing Mentra LMS features
✓ DO add AI layers incrementally (never replace working systems)
✓ DO keep MySQL and MongoDB exactly as implemented
✓ DO keep the repository runnable after every phase
✓ DO commit modularly — one feature = one commit block

✗ DO NOT redesign the architecture
✗ DO NOT break any existing API
✗ DO NOT introduce duplicate systems
✗ DO NOT hardcode credentials or secrets
✗ DO NOT modify Docs/Round-1/ (submission files are frozen)
```

---

## Implementation Progress

| Phase | Title | Status | Progress |
|---|---|---|---|
| Phase 0 | Foundation Layer | ✅ COMPLETE | 100% |
| Phase 1 | Digital Twin Engine | 🔴 NOT STARTED | 0% |
| Phase 2 | Adaptive Assessment Engine | 🔴 NOT STARTED | 0% |
| Phase 3 | Qdrant Memory Engine | 🔴 NOT STARTED | 0% |
| Phase 4 | Mastra Cognitive Swarm | 🔴 NOT STARTED | 0% |
| Phase 5 | Adaptive Intelligence Layer | 🔴 NOT STARTED | 0% |
| Phase 6 | Enkrypt Safety Layer | 🔴 NOT STARTED | 0% |
| Phase 7 | Continuous Learning System | 🔴 NOT STARTED | 0% |
| Phase 8 | Intelligence Layer | 🔴 NOT STARTED | 0% |
| Phase 9 | Student Experience Layer | 🔴 NOT STARTED | 0% |
| Phase 10 | Production Readiness | 🔴 NOT STARTED | 0% |

---

## Architecture Integrity Map

Every feature implemented must strengthen one of these layers:

| Layer | Description | Phase(s) |
|---|---|---|
| **L1** | Foundation — Existing Mentra LMS | Phase 0 ✅ |
| **L2** | Digital Twin Engine | Phases 1, 2 |
| **L3** | Memory Engine (Qdrant) | Phase 3 |
| **L4** | Mastra Cognitive Swarm | Phase 4 |
| **L5** | Adaptive Intelligence | Phase 5 |
| **L6** | Enkrypt Safety Layer | Phase 6 |
| **L7** | Continuous Learning | Phase 7 |
| **L8** | Intelligence Layer | Phase 8 |
| **L9** | Student Experience | Phase 9 |
| **L10** | Production Readiness | Phase 10 |

> If a feature does not fit into any layer, it should not be implemented.

---

## Development Principles

1. **Digital Twin First** — every feature should improve the Digital Twin
2. **Memory-Native Architecture** — new data should flow into Qdrant where appropriate
3. **Multi-Agent by Design** — new intelligence should be a Mastra agent/tool
4. **Safety Before Generation** — no AI output bypasses Enkrypt
5. **Continuous Learning** — every interaction should mutate the twin
6. **Explainable AI** — log why every decision was made
7. **Production-Ready Engineering** — tested, monitored, documented
8. **Modular & Extensible** — one phase does not break another
9. **Student-Centric** — every feature ultimately serves the student
10. **Zero Feature Regression** — never remove existing functionality

---

## Dependency Chain

```
Phase 0 (Foundation) [COMPLETE]
      ↓
Phase 1 (Digital Twin)
      ↓
Phase 2 (Assessment)
      ↓
Phase 3 (Qdrant Memory)
      ↓
Phase 4 (Mastra Swarm)
      ↓
Phase 5 (Adaptive Intelligence) ──┐
Phase 6 (Enkrypt Safety)          ├── Can be parallelised
Phase 7 (Continuous Learning) ────┘
      ↓
Phase 8 (Intelligence Layer)
      ↓
Phase 9 (Student Experience)
      ↓
Phase 10 (Production Readiness)
```

> Phases 5, 6, and 7 can be developed in parallel after Phase 4 is complete.

---

## Phase Documents

| Document | Link |
|---|---|
| Phase 0 | `Docs/Roadmap/Phase-00-Architecture-Freeze.md` |
| Phase 1 | `Docs/Roadmap/Phase-01-Digital-Twin.md` |
| Phase 2 | `Docs/Roadmap/Phase-02-Adaptive-Assessment.md` |
| Phase 3 | `Docs/Roadmap/Phase-03-Qdrant-Memory.md` |
| Phase 4 | `Docs/Roadmap/Phase-04-Mastra-Learning-Agent.md` |
| Phase 5 | `Docs/Roadmap/Phase-05-Adaptive-Teaching.md` |
| Phase 6 | `Docs/Roadmap/Phase-06-Enkrypt-Safety.md` |
| Phase 7 | `Docs/Roadmap/Phase-07-Weakness-Intelligence.md` |
| Phase 8 | `Docs/Roadmap/Phase-08-Autonomous-Learning.md` |
| Phase 9 | `Docs/Roadmap/Phase-09-Opportunity-Intelligence.md` |
| Phase 10 | `Docs/Roadmap/Phase-10-Hackathon-Submission.md` |

---

## Implementation Start Checklist

Before writing the first line of Phase 1 code:

- [ ] Phase 0 confirmed complete (Foundation Layer running)
- [ ] `python run.py` boots without errors
- [ ] MySQL has 34 tables and at least 1 admin user
- [ ] `.env` file configured with all required environment variables
- [ ] `git status` is clean (no uncommitted Phase 0 changes)
- [ ] Phase 1 document (`Phase-01-Digital-Twin.md`) fully read and understood
- [ ] `student_twins` table does not yet exist (fresh start)

---

*Last updated: 2026-06-28 by governance rewrite.*  
*This document must be updated after every phase completion.*
