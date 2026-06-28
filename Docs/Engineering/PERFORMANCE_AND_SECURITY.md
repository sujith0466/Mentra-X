# Mentra X — Performance & Security Standards

**Version:** 1.0  
**Owner:** Sujith Kumar AI

---

# Part A — Performance Standards

## Latency Targets by Operation

| Operation | Target (p50) | Target (p95) | Target (p99) | Measurement Point |
|---|---|---|---|---|
| **Memory Agent (4 parallel Qdrant queries)** | 80ms | 150ms | 300ms | Agent start → context bundle returned |
| **Redis cache read (learning_dna)** | 1ms | 3ms | 10ms | Cache lookup only |
| **Qdrant exact get (learning_dna)** | 10ms | 30ms | 80ms | Single collection query |
| **Qdrant similarity search (past_doubts)** | 20ms | 50ms | 120ms | top_k=3 vector search |
| **Embedding generation (OpenAI)** | 100ms | 250ms | 600ms | API call round-trip |
| **LLM explanation generation** | 1200ms | 2000ms | 3500ms | First token to last token |
| **LLM response (streamed, first token)** | 300ms | 600ms | 1200ms | Request sent → first token received |
| **Enkrypt validation** | 200ms | 500ms | 1000ms | API call round-trip |
| **Full DAG (end-to-end doubt resolution)** | 1800ms | 3000ms | 5000ms | Student submits query → response starts streaming |
| **Twin mutation write (Qdrant upsert)** | 8ms | 20ms | 50ms | Single upsert |
| **Twin mutation write (MySQL)** | 5ms | 15ms | 40ms | Single UPDATE query |
| **Assessment question delivery** | 50ms | 150ms | 400ms | Answer submitted → next question returned |
| **Nightly decay (per user)** | 80ms | 200ms | 500ms | Single user processing time |
| **Nightly decay (full batch, 1K users)** | 90s | 180s | 300s | Full batch completion |
| **Weakness analysis (5 sessions)** | 2s | 8s | 15s | Cron job for single user |
| **Weekly report generation** | 500ms | 2s | 5s | Report computation |
| **Opportunity matching** | 200ms | 600ms | 1500ms | Qdrant similarity search + ranking |
| **Dashboard data load** | 300ms | 800ms | 2000ms | `/api/v1/ui/dashboard_data` response |
| **Student dashboard page render** | 500ms | 1500ms | 3000ms | Full page load (including assets) |
| **Knowledge map data** | 100ms | 300ms | 800ms | All concepts for user |

## Performance Optimization Strategy

### Layer 1: Parallel Execution

The Memory Agent's 4 Qdrant queries run concurrently via `asyncio.gather()`. This reduces Memory Agent latency from ~300ms (sequential) to ~80ms (parallel):

```python
# REQUIRED: Always use gather() for multi-collection retrieval
dna, doubts, history, weaknesses = await asyncio.gather(
    fetch_learning_dna(user_id),
    retrieve_past_doubts(user_id, query),
    get_explanation_history(user_id, concept),
    get_weak_concepts(user_id)
)
```

### Layer 2: Redis Hot-Twin Cache

The `learning_dna` collection is the most frequently read. Cache TTL = 300 seconds (5 minutes):

```python
# Cache hit rate target: > 85%
# Cache miss fallback: Qdrant direct read (< 30ms)
# Cache invalidation: Every twin mutation calls redis.delete(f"dna:{user_id}")
```

### Layer 3: Response Streaming

LLM responses stream token-by-token to eliminate perceived latency:

```python
@swarm_bp.route('/api/v1/swarm/query', methods=['POST'])
def swarm_query():
    def generate():
        for chunk in tutor_agent.stream_explanation(context, level):
            yield f"data: {json.dumps({'token': chunk})}\n\n"
        yield f"data: {json.dumps({'done': True, 'session_id': session_id})}\n\n"
    return Response(generate(), mimetype='text/event-stream')
```

### Layer 4: Database Connection Pooling

```python
# backend/app.py
app.config.update({
    'SQLALCHEMY_POOL_SIZE': 20,          # Concurrent connections
    'SQLALCHEMY_POOL_TIMEOUT': 30,       # Seconds before timeout
    'SQLALCHEMY_POOL_RECYCLE': 1800,     # Recycle connections every 30 min
    'SQLALCHEMY_MAX_OVERFLOW': 10,       # Extra connections on peak
})
```

### Layer 5: Qdrant Query Optimization

- Every query must include `filter={"user_id": user_id}` — prevents full-collection scans
- Use `top_k=3` for similarity searches (not top_k=10) — minimizes data transfer
- Batch upserts in nightly decay (100 users per batch) — reduces API overhead

### Layer 6: Background Job Distribution

Nightly decay processing 1,000 users in < 3 hours:

```python
# Process in batches of 100 with 500ms sleep between batches
BATCH_SIZE = 100
BATCH_SLEEP_MS = 500

for i in range(0, len(active_users), BATCH_SIZE):
    batch = active_users[i:i+BATCH_SIZE]
    await asyncio.gather(*[process_user_decay(uid) for uid in batch])
    await asyncio.sleep(BATCH_SLEEP_MS / 1000)
```

## Performance Monitoring

Capture these metrics on every AI session:

```sql
-- These columns exist in ai_sessions (added Phase 10)
memory_retrieval_ms   INT     -- Memory Agent total duration
enkrypt_validation_ms INT     -- Enkrypt API call duration
total_response_ms     INT     -- Full end-to-end duration
llm_tokens_used       INT     -- input + output tokens
```

Alert thresholds:
- P95 E2E > 5000ms → page engineering on-call
- Enkrypt hard fail rate > 5% → investigate LLM quality drift
- Redis cache hit rate < 70% → investigate cache invalidation bugs

---

# Part B — Security Standards

## Authentication & Session Security

| Requirement | Implementation |
|---|---|
| Password hashing | `werkzeug.security` PBKDF2-SHA256, 600,000 iterations |
| Session management | Flask server-side sessions, `SESSION_COOKIE_SECURE=True`, `SESSION_COOKIE_HTTPONLY=True` |
| CSRF protection | Flask-WTF CSRF tokens on all forms and state-modifying API calls |
| Session timeout | 8 hours idle timeout |
| Failed login handling | Log to `audit_logs`, no account lockout (rate limiting instead) |

## Authorization (RBAC)

Three roles: `student`, `admin`, `super_admin`

| Route Category | Required Role |
|---|---|
| `/api/v1/twin/*` | `student` (own data only) |
| `/api/v1/swarm/*` | `student` (own sessions only) |
| `/api/v1/intelligence/*` | `student` (own reports only) |
| `/admin/*` | `admin` |
| `/api/v1/safety/hitl_*` | `admin` |
| `/api/v1/ui/agent_trace` | `admin` |
| `/admin/super/*` | `super_admin` |

Every admin route must include:

```python
@admin_bp.route('/admin/safety/hitl_queue')
@login_required
@require_role('admin')
def hitl_queue(): ...
```

## Secrets Management

| Secret | Storage | Rotation |
|---|---|---|
| MySQL password | `.env` (never in source) | Quarterly |
| MongoDB URI | `.env` | Quarterly |
| Qdrant API key | `.env` | On breach |
| OpenAI API key | `.env` | Monthly |
| Enkrypt API key | `.env` | Monthly |
| Flask `SECRET_KEY` | `.env` (32+ random bytes) | On breach |
| Admin password | `.env` (`DEFAULT_ADMIN_PASSWORD`) | Monthly |

**Rules:**
- `.env` is in `.gitignore` — never committed
- `.env.example` is in source control — shows variable names, never values
- Production uses environment injection (Docker secrets or deployment platform env vars)
- All env vars validated on startup; missing required var → startup failure with clear error

## Rate Limiting

```python
# Per-endpoint limits (backend/security/rate_limiter.py)
RATE_LIMITS = {
    "/api/v1/swarm/query":         "30/minute",   # AI query (expensive)
    "/api/v1/assessment/answer":   "60/minute",   # Assessment answers
    "/api/v1/twin/*":              "100/minute",  # Twin reads
    "/api/v1/intelligence/*":      "20/minute",   # Reports
    "auth.login":                  "10/minute",   # Login attempts
    "auth.register":               "5/minute",    # Registration
    "default":                     "200/day, 50/hour"
}
```

## Input Validation

All POST/PUT/PATCH endpoints validate input using Marshmallow schemas:

```python
class SwarmQuerySchema(Schema):
    query = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=2000),
            validate.Regexp(r'^[\w\s\.\,\?\!\:\;\-\+\=\(\)\[\]\{\}\/\\\*\&\%\$\#\@]+$',
                           error="Query contains invalid characters")
        ]
    )
    exam_track = fields.Str(validate=validate.OneOf(["JEE", "NEET", "UPSC", "CAT"]))
    concept_tag = fields.Str(validate=validate.Length(max=100))

# Usage in route:
@swarm_bp.route('/api/v1/swarm/query', methods=['POST'])
def swarm_query():
    schema = SwarmQuerySchema()
    errors = schema.validate(request.json)
    if errors:
        return error_response("MASTRA_001", f"Invalid input: {errors}", 400)
```

## Prompt Injection Mitigation

AI prompts receive student-provided text. Prevent injection attacks:

```python
def sanitize_student_query(query: str) -> str:
    """
    Remove prompt injection patterns before passing to LLM.
    """
    # Remove common injection prefixes
    injection_patterns = [
        r"ignore (all |previous |above )?instructions",
        r"you are now",
        r"system:",
        r"<\|im_start\|>",
        r"<\|im_end\|>",
        r"\[INST\]",
        r"\[/INST\]",
    ]
    for pattern in injection_patterns:
        query = re.sub(pattern, "[filtered]", query, flags=re.IGNORECASE)

    return query[:2000]  # Hard length limit
```

Additionally: student input is always in the `user` role, never the `system` role of the prompt.

## Audit Logging

All security-relevant events logged to `audit_logs` MySQL table:

| Event | Logged Fields |
|---|---|
| Login success/failure | user_id, ip_address, timestamp, success |
| Admin action | admin_id, action_type, target_id, timestamp |
| Role change | acting_admin_id, target_user_id, old_role, new_role, timestamp |
| HITL review | admin_id, session_id, action_taken, timestamp |
| Rate limit exceeded | user_id, endpoint, limit, timestamp |
| Enkrypt hard fail | session_id, user_id, composite_score, timestamp |

## Data Privacy

| Data Category | Access Policy |
|---|---|
| Learning DNA | Read: own student + admin. Write: AI system only. |
| Session logs | Read: own student + admin. Never exposed to other students. |
| Enkrypt intercept logs | Read: admin only. Original flawed output never shown to student. |
| Agent traces | Read: admin/developer only. |
| HITL queue | Read/write: admin only. |
| User passwords | Never readable (hashed). Stored as bcrypt hash. |
| Qdrant queries | Always filtered by `user_id`. Cross-user reads architecturally impossible. |

## Encryption Strategy

| Data at Rest | Encryption |
|---|---|
| MySQL database | AES-256 (RDS/cloud provider encryption or disk-level encryption) |
| Qdrant storage | Disk-level encryption on Qdrant Cloud; volume encryption on self-hosted |
| Redis cache | Memory only (TTL=300s); no persistent storage of sensitive data |

| Data in Transit | Encryption |
|---|---|
| Client ↔ Flask | TLS 1.3 (HTTPS enforced in production) |
| Flask ↔ MySQL | Encrypted connection (`ssl_ca` parameter in MySQL URI) |
| Flask ↔ Qdrant Cloud | HTTPS |
| Flask ↔ OpenAI | HTTPS (enforced by OpenAI SDK) |
| Flask ↔ Enkrypt | HTTPS |

## Monitoring Standards

### Health Checks

```python
@app.route('/health')
def health_check():
    """Unauthenticated health check for load balancer / uptime monitoring."""
    checks = {
        "mysql": _check_mysql(),
        "qdrant": _check_qdrant(),
        "redis": _check_redis(),         # Optional (graceful if missing)
        "scheduler": _check_scheduler()  # Optional (graceful if disabled)
    }
    status = "healthy" if all(v["ok"] for v in checks.values()) else "degraded"
    http_code = 200 if status == "healthy" else 503
    return jsonify({"status": status, "checks": checks}), http_code
```

### Key Metrics to Alert On

| Metric | Warning | Critical | Responder |
|---|---|---|---|
| API P95 response time | > 3s | > 8s | Engineering |
| Enkrypt hard fail rate | > 2% | > 5% | Engineering |
| MySQL connection pool | > 70% used | > 90% used | Engineering |
| HITL queue depth | > 10 items | > 50 items | Content team |
| Nightly decay job | > 2h late | Not run | Engineering |
| Redis cache hit rate | < 80% | < 60% | Engineering |
| Failed logins | > 20/min | > 100/min | Security |

### Incident Response

**P0 (Full outage):**
1. Check `/health` endpoint
2. Identify failing service (MySQL / Qdrant / LLM API)
3. Enable feature flags degradation (disable ENABLE_QDRANT, fall back to MySQL)
4. Investigate root cause
5. Re-enable flags after fix confirmed

**P1 (Partial degradation):**
1. Identify affected feature (high Enkrypt fail rate / slow LLM)
2. Check observability dashboard for pattern
3. Disable specific feature flag if needed
4. Students receive textbook fallback (Enkrypt) or legacy chatbot (Mastra)
