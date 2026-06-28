# Mentra X — Testing Guide

**Owner:** Sujith Kumar AI  
**Version:** 1.0  

## 1. Testing Philosophy
Mentra X tests prioritize reliability and speed. We focus on:
- **Unit Tests:** Pure business logic (`backend/services/`). Mock all external dependencies (DB, Qdrant, APIs). Target >80% coverage.
- **Integration Tests:** Database and Qdrant interactions. We use dedicated `test_` prefixed collections.
- **End-to-End (E2E) Tests:** Full student journeys simulating HTTP requests.

We do *not* write unit tests for Flask routes, as routes should contain zero business logic. We test routes via E2E tests.

## 2. Test Structure
```
backend/tests/
├── conftest.py              # Global pytest fixtures (DB session, mocks)
├── unit/
│   ├── test_twin_builder.py
│   ├── test_decay_engine.py
│   └── test_event_bus.py
├── integration/
│   ├── test_qdrant_memory.py
│   └── test_enkrypt_flow.py
└── e2e/
    └── test_student_journey.py
```

## 3. Unit Testing
Run unit tests locally (fast, no DB required):
```bash
pytest backend/tests/unit/ -v --cov=backend
```

**Writing a Unit Test (Example: Decay Engine):**
```python
# backend/tests/unit/test_decay_engine.py
def test_decay_engine_14_days_returns_near_zero_retention():
    # Arrange
    mastery = 1.0
    days = 14
    
    # Act
    retention = compute_retention(mastery, days, stability=7.0)
    
    # Assert
    assert retention < 0.20
    assert retention > 0.10
```

## 4. Integration Testing
Run integration tests locally (Requires MySQL and Qdrant Docker to be running):
```bash
pytest backend/tests/integration/ -v
```

**Qdrant Test Collections:**
Integration tests must NEVER use production collections. The `conftest.py` fixture automatically intercepts Qdrant calls and redirects them to `test_learning_dna`, `test_past_doubts`, etc.

**Teardown Strategy:**
Integration tests must clean up their own data. The `conftest.py` handles MySQL rollbacks and Qdrant collection clearing after each test.

## 5. End-to-End (E2E) Testing
E2E tests spin up a Flask test client and simulate an entire user session.

```bash
pytest backend/tests/e2e/ -v
```

**Student Journey Test:**
Tests the critical path: Login -> Diagnostic Assessment -> Twin Initialized -> Query Submitted -> DAG Execution -> Dashboard Update.

## 6. Performance Testing (Locust)
For load testing, we use Locust.

**Setup:**
```bash
pip install locust
```

**Run Load Test:**
```bash
locust -f backend/tests/performance/locustfile.py --host=http://localhost:5000
```

Target metrics to validate:
- Assessment submission latency < 200ms
- Dashboard load < 800ms
- AI Query initiation (streaming start) < 1500ms

## 7. Security Testing
**Static Application Security Testing (SAST):**
Run Bandit to scan for common Python vulnerabilities (e.g., hardcoded passwords, shell injections).
```bash
bandit -r backend/ -ll
```

**Manual Checklist:**
- [ ] Attempt to access `/admin/` as a student role. (Must return 403).
- [ ] Attempt to query `/api/v1/twin/profile?user_id=OTHER_USER`. (Must return 403).
- [ ] Attempt SQL injection in assessment submission.
- [ ] Attempt Prompt Injection (e.g., "Ignore all previous instructions...").

## 8. Test Data Management
To seed the local database for manual UI testing:
```bash
# Creates 5 mock students with varying Twin states and quiz histories
python scripts/seed_test_data.py
```
Do NOT run this script in production.

## 9. CI/CD Integration
GitHub Actions runs the test suite on every PR to `main`.
```yaml
# .github/workflows/test.yml
name: Tests
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
      qdrant:
        image: qdrant/qdrant
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt pytest-cov
      - run: pytest backend/tests/ -v --cov=backend
```

## 10. Common Test Failures
| Failure | Reason | Fix |
|---|---|---|
| `QdrantConnectionError` in Integration Test | Qdrant Docker not running | `docker run -p 6333:6333 qdrant/qdrant` |
| Route unit tests failing | Route imported business logic | Refactor logic to `services/` |
| Flaky timestamp tests | Comparing exact datetime | Use `unittest.mock.patch('datetime.utcnow')` or allow delta |
