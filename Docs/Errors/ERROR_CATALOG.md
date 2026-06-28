# Mentra X — Standardized Error Catalog

**Version:** 1.0  
**Owner:** Sujith Kumar AI  

## Overview
This document defines all standard error codes returned by the Mentra X backend API. Client applications should use these codes to trigger specific UI states, retries, or fallback logic.

### Error Response Format
All errors return HTTP 400, 401, 403, 404, 429, or 500, with the following JSON schema:
```json
{
    "success": false,
    "error": {
        "code": "TWIN_001",
        "message": "Twin not initialized for user.",
        "recovery": "Call POST /api/v1/twin/initialize first.",
        "severity": "HIGH"
    },
    "meta": {
        "timestamp": "2026-06-28T12:00:00Z",
        "request_id": "req_abc123"
    }
}
```

### Severity Definitions
- **LOW:** Does not impact core functionality. No immediate action required.
- **MEDIUM:** Impedes a specific feature, but graceful fallback exists.
- **HIGH:** Blocks a core flow for a single user (e.g., Twin sync failed).
- **CRITICAL:** System-wide failure (e.g., Database unavailable).

---

## TWIN Errors (Digital Twin Engine)

| Code | HTTP Status | Description | Cause | Recovery Steps | Severity | Retry Behaviour |
|---|---|---|---|---|---|---|
| `TWIN_001` | 404 | Twin not initialized for user | Attempted to read twin data before Phase 2 assessment completion | Redirect to diagnostic assessment | HIGH | None |
| `TWIN_002` | 409 | Twin mutation failed | Optimistic lock conflict (version mismatch) | Fetch latest twin state and reapply | MEDIUM | Automatic retry (x3) |
| `TWIN_003` | 400 | Twin version mismatch | Client provided stale twin version | Client must sync twin state | MEDIUM | Manual |
| `TWIN_004` | 500 | Twin health computation failed | Missing required state properties | Recompute health score asynchronously | LOW | Automatic |
| `TWIN_005` | 500 | Twin sync conflict | MySQL and Qdrant versions diverged | Force sync from Qdrant to MySQL | HIGH | Manual admin action |
| `TWIN_006` | 400 | Invalid exam track | Track not in [JEE, NEET, UPSC, CAT] | Prompt user to select valid track | MEDIUM | Manual |
| `TWIN_007` | 500 | Twin initialization data incomplete | Assessment completed but failed to seed all states | Run manual seed script | HIGH | Manual admin action |
| `TWIN_008` | 500 | Mutation log write failed | MongoDB timeout or schema error | Log locally, twin state still valid | LOW | Automatic |
| `TWIN_009` | 500 | Twin snapshot failed | Nightly snapshot backup failed | Ignore, retry next cycle | LOW | None |
| `TWIN_010` | 404 | Twin not found | User ID does not exist | Validate user authentication | HIGH | None |

## MEMORY Errors (Qdrant & Context)

| Code | HTTP Status | Description | Cause | Recovery Steps | Severity | Retry Behaviour |
|---|---|---|---|---|---|---|
| `MEMORY_001` | 500 | Qdrant collection not found | Collection was deleted or not initialized | Run init_qdrant.py | CRITICAL | Manual admin action |
| `MEMORY_002` | 503 | Embedding generation failed | OpenAI API timeout/rate limit | Fallback to BM25 or keyword match | MEDIUM | Automatic retry with exponential backoff |
| `MEMORY_003` | 504 | Memory write timeout | Qdrant cluster overloaded | Queue write operation for later | MEDIUM | Automatic background retry |
| `MEMORY_004` | 504 | Memory read timeout | Qdrant cluster overloaded | Return empty context or fallback | HIGH | Automatic (fast fail) |
| `MEMORY_005` | 500 | Context assembly failed | Invalid DTO structure retrieved | Log error, return partial context | HIGH | None |
| `MEMORY_006` | 200 (Warn) | Redis cache miss | Cache expired or evicted | Fetch from Qdrant, repopulate cache | LOW | None (Graceful) |
| `MEMORY_007` | 500 | Embedding dimension mismatch | Switched embedding model (e.g., ada-002 -> 3-small) | Re-index all vectors | CRITICAL | Manual admin action |
| `MEMORY_008` | 500 | Collection not initialized | Missing test collections during tests | Run pytest setup fixtures | HIGH | None |
| `MEMORY_009` | 403 | User isolation violation attempt | Query lacked user_id filter | Deny request, flag security audit | CRITICAL | None |
| `MEMORY_010` | 503 | Qdrant unavailable | Qdrant host unreachable | Graceful degradation to MySQL JSON | CRITICAL | Poll until healthy |

## MASTRA Errors (Agent Swarm)

| Code | HTTP Status | Description | Cause | Recovery Steps | Severity | Retry Behaviour |
|---|---|---|---|---|---|---|
| `MASTRA_001` | 500 | Agent tool not found | Typo in tool registration | Fix code, redeploy | HIGH | None |
| `MASTRA_002` | 504 | DAG execution timeout | An agent took longer than threshold | Return timeout error to client | HIGH | Manual user retry |
| `MASTRA_003` | 400 | Agent context overflow | Context + query exceeded token limit | Truncate history, summarize | MEDIUM | Automatic internal retry |
| `MASTRA_004` | 500 | Tool execution failed | Exception inside Mastra tool | Log trace, return fallback response | HIGH | None |
| `MASTRA_005` | 500 | HITL queue write failed | Database error while flagging hard fail | Log locally, alert admin | MEDIUM | Automatic |
| `MASTRA_006` | 500 | Cron workflow failed | Weakness or Insights run crashed | Log trace, skip user, continue batch | LOW | Retry next cycle |
| `MASTRA_007` | 500 | Agent communication error | Invalid Pydantic schema passed | Fix agent I/O contract | HIGH | None |
| `MASTRA_008` | 500 | Workflow state corrupted | DAG state machine out of sync | Terminate session, create new | HIGH | None |

## ENKRYPT Errors (Safety Validation)

| Code | HTTP Status | Description | Cause | Recovery Steps | Severity | Retry Behaviour |
|---|---|---|---|---|---|---|
| `ENKRYPT_001` | 503 | Enkrypt API unavailable | API down or rate limited | Allow through (log warning) OR hard fail (config dependent) | CRITICAL | Automatic |
| `ENKRYPT_002` | 500 | Validation confidence below threshold | LLM failed safety rules max times | Trigger hard fail (Textbook fallback) | HIGH | None (already retried max times) |
| `ENKRYPT_003` | 500 | Math validator parsing error | Invalid formula formatting | Skip math validation, rely on science | MEDIUM | None |
| `ENKRYPT_004` | 500 | Science validator KB miss | Concept not found in Enkrypt KB | Rely on generic hallucination validator | MEDIUM | None |
| `ENKRYPT_005` | 200 (Warn) | Hard fail — textbook fallback served | Composite score < 0.70 | Serve NCERT fallback, raise HITL flag | HIGH | None |
| `ENKRYPT_006` | 200 (Warn) | HITL flag raised | Safety violation detected | Admin must review intercept log | MEDIUM | None |

## ASSESSMENT Errors (Diagnostic Engine)

| Code | HTTP Status | Description | Cause | Recovery Steps | Severity | Retry Behaviour |
|---|---|---|---|---|---|---|
| `ASSESSMENT_001` | 404 | Session not found | Invalid or expired session ID | Start new assessment session | MEDIUM | None |
| `ASSESSMENT_002` | 500 | Question bank insufficient | Ran out of questions for track | End assessment early, extrapolate | HIGH | None |
| `ASSESSMENT_003` | 400 | Assessment already completed | Attempted to submit answer post-completion | Redirect to dashboard | LOW | None |
| `ASSESSMENT_004` | 400 | Assessment session abandoned | Timeout > 24 hours | Start new assessment session | LOW | None |
| `ASSESSMENT_005` | 500 | KnowledgeState computation failed | Bayesian update error | Use simple average | MEDIUM | Automatic |
| `ASSESSMENT_006` | 500 | DNA seeding failed | Could not save to Qdrant | Save to MySQL, queue Qdrant sync | HIGH | Automatic |

## AUTH Errors (Authentication & Authorization)

| Code | HTTP Status | Description | Cause | Recovery Steps | Severity | Retry Behaviour |
|---|---|---|---|---|---|---|
| `AUTH_001` | 401 | Invalid credentials | Wrong email/password | Prompt to try again or reset password | LOW | Manual |
| `AUTH_002` | 401 | Session expired | Token TTL reached | Redirect to login page | LOW | Manual |
| `AUTH_003` | 403 | Insufficient permissions | Student accessing admin route | Deny access, log audit | HIGH | None |
| `AUTH_004` | 403 | Admin role required | Missing admin claims | Deny access | HIGH | None |
| `AUTH_005` | 429 | Rate limit exceeded | Too many requests | Wait until reset window | MEDIUM | Manual after window |
| `AUTH_006` | 403 | CSRF token invalid | Missing or mismatched CSRF token | Refresh page, submit again | MEDIUM | Manual |

## SYSTEM Errors (Infrastructure)

| Code | HTTP Status | Description | Cause | Recovery Steps | Severity | Retry Behaviour |
|---|---|---|---|---|---|---|
| `SYS_001` | 503 | MySQL connection failed | DB down or pool exhausted | Return 503, trigger PagerDuty | CRITICAL | Automatic |
| `SYS_002` | 503 | MongoDB connection failed | DB down or auth error | Disable observability writing, continue | MEDIUM | Automatic |
| `SYS_003` | 500 | Scheduler not running | APScheduler thread died | Restart scheduler process | HIGH | Manual admin action |
| `SYS_004` | 500 | Environment variable missing | Missing required .env config | Crash on startup, log missing key | CRITICAL | None (Startup block) |
| `SYS_005` | 500 | Production readiness check failed | Debug mode True in production | Crash on startup | CRITICAL | None (Startup block) |
