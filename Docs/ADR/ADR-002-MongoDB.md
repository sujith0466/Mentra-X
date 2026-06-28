# ADR-002: MongoDB as AI Interaction Audit Log Store

| Field       | Value                               |
|-------------|-------------------------------------|
| **Status**  | ✅ ACCEPTED                         |
| **Date**    | 2026-06-28                          |
| **Author**  | Sujith Kumar AI                     |
| **Deciders**| Platform Architecture Team          |
| **Tags**    | database, mongodb, ai, logging, audit, enkrypt, agents |

---

## Table of Contents

1. [Context](#1-context)
2. [Problem Statement](#2-problem-statement)
3. [Decision](#3-decision)
4. [Alternatives Considered](#4-alternatives-considered)
5. [Pros](#5-pros)
6. [Cons](#6-cons)
7. [Trade-offs](#7-trade-offs)
8. [Consequences](#8-consequences)
9. [Graceful Fallback Design](#9-graceful-fallback-design)
10. [Implementation Notes](#10-implementation-notes)
11. [Future Revisions](#11-future-revisions)
12. [References](#12-references)

---

## 1. Context

### 1.1 The AI Interaction Surface

Mentra X's AI layer generates a substantial volume of **interaction artifacts** during every user session. These artifacts are produced by six specialized agents operating in a Directed Acyclic Graph (DAG) orchestrated by Mastra:

| Agent                        | Log Artifacts Generated                                                                 |
|------------------------------|-----------------------------------------------------------------------------------------|
| **Orchestrator Agent**       | Session initialization payload, agent dispatch records, DAG execution metadata          |
| **Weakness Intelligence Agent** | Weakness cluster computations, confidence scores, topic divergence maps              |
| **Adaptive Content Agent**   | Content selection rationale, difficulty calibration trace, concept substitution log      |
| **Doubt Resolution Agent**   | Parsed student query, retrieved context chunks, generated explanation, quality score     |
| **Project Mentor Agent**     | Milestone review payloads, code feedback trace, rubric scoring breakdown                |
| **Opportunity Pathfinder Agent** | Career match scores, skill-to-opportunity gap map, recommendation reasoning trace  |

### 1.2 Enkrypt AI Safety Layer

Every AI-generated response passes through the **Enkrypt AI safety validation pipeline** before delivery to the student. This pipeline produces a per-response audit record containing:

```json
{
  "session_id": "sess_abc123",
  "agent_id": "doubt_resolution_agent",
  "request_id": "req_uuid_789",
  "timestamp": "2026-06-28T12:34:56.789Z",
  "student_id": 42,
  "input_text": "Explain dynamic programming with memoization",
  "output_text": "Dynamic programming breaks problems into...",
  "enkrypt_scores": {
    "toxicity": 0.002,
    "bias": 0.008,
    "hallucination_risk": 0.031,
    "pii_detected": false,
    "policy_compliance": 0.997
  },
  "validation_passed": true,
  "latency_ms": 87,
  "model_used": "gpt-4o",
  "token_usage": {"prompt": 1240, "completion": 380, "total": 1620},
  "hitl_flagged": false,
  "hitl_reason": null
}
```

This document is **semi-structured** — the `enkrypt_scores` object varies by validation pipeline version; the `hitl_reason` field is nullable; the `token_usage` structure may include additional fields as the model API evolves. Its schema is not fixed and changes without coordinated migration.

### 1.3 Human-in-the-Loop (HITL) Records

When Enkrypt validation scores exceed safety thresholds or agent confidence falls below acceptable levels, a **HITL flag** is raised. This creates a HITL review record:

```json
{
  "hitl_id": "hitl_uuid_456",
  "session_id": "sess_abc123",
  "flagged_at": "2026-06-28T12:35:01.234Z",
  "flag_reason": "hallucination_risk > 0.15",
  "agent_output_suppressed": true,
  "reviewer_id": null,
  "reviewed_at": null,
  "reviewer_decision": null,
  "reviewer_notes": null,
  "escalation_level": 1
}
```

HITL records are created at high speed (synchronous with the AI response pipeline) but reviewed asynchronously by human instructors. Their structure evolves as the HITL workflow matures.

### 1.4 Agent Execution Traces

Mastra exposes per-agent execution traces for debugging and performance analysis. Each trace captures:
- Agent input/output messages
- Tool calls made during execution
- Intermediate reasoning steps (chain-of-thought, if captured)
- Latency per step
- Error states and retry counts

These traces are invaluable for debugging agent behavior but are high-volume, variable-length, and not queried transactionally.

### 1.5 Volume Projections

At 31 current users with average daily active usage:

| Log Category            | Events per Session | Sessions/Day | Daily Records |
|-------------------------|--------------------|--------------|----------------|
| Enkrypt validation logs | ~12 per session    | ~20          | ~240           |
| Agent execution traces  | ~6 per session     | ~20          | ~120           |
| HITL flag records       | ~0.05 per session  | ~20          | ~1             |
| Session metadata        | 1 per session      | ~20          | ~20            |
| **Total Daily**         |                    |              | **~381**       |

Projected at **10,000 active users** (Phase 5 target):

| Log Category            | Daily Records |
|-------------------------|---------------|
| Enkrypt validation logs | ~1,200,000    |
| Agent execution traces  | ~600,000      |
| HITL flag records       | ~5,000        |
| Session metadata        | ~100,000      |
| **Total Daily**         | **~1,905,000** |

At this volume, ~57 million records per month. A purpose-built document store is required.

---

## 2. Problem Statement

> **Where should Mentra X store AI interaction audit logs — Enkrypt validation records, agent execution traces, session metadata, HITL flags — given that these records are semi-structured, high-write-volume, rarely queried but comprehensively read when needed, and must not block the primary AI response pipeline?**

Specific requirements:

| Requirement                           | Details                                                                     |
|---------------------------------------|-----------------------------------------------------------------------------|
| **Schema flexibility**                | Enkrypt score schema changes with pipeline version; no rigid column contract |
| **Write performance**                 | Writes must be fire-and-forget; must not add latency to AI response path    |
| **Query pattern**                     | Bulk reads by `session_id`, `student_id`, date range for HITL review; not transactional |
| **Volume tolerance**                  | Must scale to millions of records per month without DBA intervention        |
| **Platform integrity**                | Failure to write an audit log must NEVER fail the AI response to the student |
| **Retention policy support**          | Must support TTL-based automatic expiry of old logs                         |
| **Development optionality**           | Platform must function without MongoDB available (local dev without Docker)  |

---

## 3. Decision

**We will use MongoDB as the AI interaction audit log store, accessed through PyMongo, with a graceful fallback to structured file logging when MongoDB is unavailable.**

### 3.1 Binding Constraints

- MongoDB is used **exclusively for AI audit data** — no LMS business data, no user accounts, no course data.
- All writes to MongoDB are **fire-and-forget** (non-blocking). The AI response pipeline does not wait for MongoDB acknowledgment.
- MongoDB is treated as **optional infrastructure** — the platform starts and operates fully without it; logs degrade to structured JSON file output.
- All MongoDB collections use **TTL indexes** for automatic data lifecycle management.
- MongoDB access is abstracted behind a `MongoAuditLogger` service class — no direct PyMongo calls in agent code.

### 3.2 Collection Architecture

Five collections are defined in the `mentrax_audit` database:

| Collection                  | Primary Use                                         | TTL           |
|-----------------------------|-----------------------------------------------------|---------------|
| `enkrypt_validation_logs`   | Per-response safety validation records              | 90 days       |
| `agent_execution_traces`    | Per-agent run trace (input, output, steps, latency) | 30 days       |
| `hitl_review_queue`         | HITL-flagged items pending human review             | No TTL (manual archival) |
| `session_ai_metadata`       | Per-session AI context summary                      | 180 days      |
| `twin_mutation_audit`       | Digital Twin state change records                   | 365 days      |

---

## 4. Alternatives Considered

### 4.1 Comparison Matrix

| Criterion                       | MongoDB ✅           | MySQL (Extend Existing) | Elasticsearch        | ClickHouse           | AWS CloudWatch Logs   |
|---------------------------------|----------------------|-------------------------|----------------------|----------------------|-----------------------|
| **Schema flexibility**          | Native (BSON)        | Rigid (ALTER required)  | Flexible (mappings)  | Rigid (columnar)     | Unstructured text     |
| **Write throughput**            | Very High            | High (with tuning)      | High                 | Extremely High       | High                  |
| **Fire-and-forget writes**      | ✅ Native (w:0)       | ❌ (transaction cost)    | ✅ (async index)      | ✅                    | ✅                     |
| **TTL-based expiry**            | ✅ Native             | Manual (cron job)       | ✅ ILM policies       | ✅ TTL column          | ✅ Log group retention |
| **Semi-structured storage**     | ✅ First-class        | JSON columns (limited)  | ✅ First-class        | JSON type (limited)  | Text blobs            |
| **Query by field path**         | ✅ dot notation       | JSON_EXTRACT (slow)     | ✅ Lucene query       | JSON path (limited)  | CloudWatch Insights   |
| **Operational complexity**      | Medium               | None (already running)  | High                 | Medium               | Zero (managed)        |
| **Cost at scale**               | Self-host: Low        | Scales poorly for logs  | Medium-High          | Self-host: Low        | Per-GB ingestion      |
| **Optional / graceful fallback**| ✅ Feasible           | N/A                     | Feasible             | Feasible             | No local equivalent   |
| **PyMongo integration**         | ✅ Official           | N/A                     | elasticsearch-py     | clickhouse-driver    | boto3                 |
| **Local development support**   | Docker or Atlas Free | ✅ Already running       | Docker (heavy)       | Docker               | AWS only              |
| **HITL workflow queries**       | ✅ ($match, $sort)    | ✅ SQL                   | ✅ Full-text          | ✅ SQL                 | CloudWatch Insights   |

### 4.2 MySQL (Extend Existing) Analysis

The most immediately obvious alternative is to extend the existing MySQL database with additional tables: `enkrypt_logs`, `agent_traces`, `hitl_queue`. This approach has zero new infrastructure cost and uses a system already in production.

However, it fails on three critical dimensions:

1. **Schema rigidity vs. log evolution**: MySQL requires `ALTER TABLE` for every new field in Enkrypt scores or agent trace structure. The Enkrypt API evolves independently of Mentra X's deployment cycle. Using a `JSON` column to store the variable part defeats the purpose — it is effectively using MySQL as a document store, poorly.

2. **Write volume contamination**: At projected scale (1.9M records/day), AI log writes would dominate MySQL's InnoDB write buffer. This directly degrades the performance of LMS business operations (quiz submissions, enrollment updates) that share the same write path and buffer pool.

3. **Table size explosion**: A 90-day retention of Enkrypt logs at scale means ~108M rows in a single table. MySQL's InnoDB handles large tables, but without partitioning (which adds operational complexity), query performance degrades significantly. Partitioning by date requires ongoing partition management.

**Verdict**: Technically feasible but operationally dangerous. The AI log write pattern would canibalize MySQL's buffer pool and degrade LMS performance. Hard reject.

### 4.3 Elasticsearch Analysis

Elasticsearch is purpose-built for log ingestion and full-text search. Its Index Lifecycle Management (ILM) policies handle retention automatically, and its Kibana UI would provide excellent HITL review tooling. However:

- **Operational complexity**: Elasticsearch requires JVM tuning, dedicated heap sizing, and careful index management. For a team at MVP scale, operating Elasticsearch is a significant burden.
- **Overkill for query patterns**: Mentra X's audit log queries are simple: lookup by `session_id`, filter by `student_id` and date range. These do not require Elasticsearch's full-text Lucene query engine.
- **Graceful fallback complexity**: Degrading gracefully when Elasticsearch is unavailable is possible but requires more sophisticated connection management than MongoDB.

**Verdict**: Excellent technology but operationally over-engineered for Mentra X's current log query requirements. Consider for Phase 7+ when centralized observability platform is introduced.

### 4.4 ClickHouse Analysis

ClickHouse is a column-oriented OLAP database with extraordinary write throughput and query speed for analytics over time-series data. It would be ideal for aggregate queries (e.g., "what is the average Enkrypt hallucination score for all sessions this week?").

- **Not suitable for document storage**: ClickHouse's columnar model requires a fixed, wide schema. Semi-structured log data requires either JSON columns (limited) or pre-defined schema — exactly the problem we're trying to avoid.
- **Overkill for current scale**: ClickHouse shines at billions of rows. At current Mentra X scale, its advantages are not realized.
- **No flexible schema**: Agent traces have highly variable depth (1-20 steps), which maps poorly to ClickHouse's flat column model.

**Verdict**: Ideal for future analytics over aggregated metrics. Not suitable for variable-structure audit log storage. Re-evaluate for Phase 8 analytics engine.

### 4.5 AWS CloudWatch Logs Analysis

CloudWatch Logs provides managed log ingestion, retention, and querying via CloudWatch Logs Insights. It requires zero infrastructure operation.

- **Vendor lock-in**: Ties the entire audit log system to AWS. Mentra X's infrastructure neutrality goal conflicts with full CloudWatch commitment.
- **Query limitations**: CloudWatch Logs Insights is powerful but not a replacement for structured document queries. Correlating logs across `session_id` and `student_id` requires careful log group organization.
- **Cost at scale**: CloudWatch charges per GB ingested and per GB scanned during queries. At 1.9M records/day with average record size of 2KB, ingestion costs would be ~$11/day (~$330/month) at Phase 5 scale.
- **No local development equivalent**: Local development and testing cannot use CloudWatch without AWS credentials and internet access.

**Verdict**: Suitable as a supplementary observability tool (ship structured logs to CloudWatch for alerting) but not as the primary audit log store.

---

## 5. Pros

### 5.1 Schema Flexibility Matches Log Evolution

MongoDB's BSON document model accepts any JSON-compatible structure without schema definition. When Enkrypt releases a new validation pipeline that adds `coherence_score` and `factual_accuracy` fields to its output, MongoDB stores these automatically — no migration, no `ALTER TABLE`, no deployment coordination.

### 5.2 High Write Throughput with Fire-and-Forget

PyMongo's `insert_one()` with `w=0` (unacknowledged write) returns immediately after network handoff, adding effectively zero latency to the AI response pipeline. MongoDB's write-optimized WiredTiger storage engine with write-ahead logging sustains high write throughput even on modest hardware.

```python
# Non-blocking audit log write — does not delay agent response
collection.insert_one(audit_record, write_concern=WriteConcern(w=0))
```

### 5.3 Native TTL Indexes for Data Lifecycle

MongoDB's TTL indexes automatically delete documents past their expiry. This is a first-class feature requiring no cron jobs, stored procedures, or manual partition pruning:

```python
# Created once during collection initialization
collection.create_index(
    [("created_at", ASCENDING)],
    expireAfterSeconds=7776000  # 90 days
)
```

### 5.4 PyMongo Integration is Straightforward

PyMongo is the official MongoDB Python driver, maintained by MongoDB Inc. It is stable, well-documented, and integrates cleanly with Flask. Connection pooling, TLS support, and replica set awareness are built in.

### 5.5 Powerful Aggregation Pipeline for HITL Review

MongoDB's aggregation pipeline allows instructors to query HITL records with complex filters:

```javascript
// Find all unreviewed HITL flags for a student this week, sorted by risk score
db.hitl_review_queue.aggregate([
  { $match: { student_id: 42, reviewed_at: null, flagged_at: { $gte: weekStart } } },
  { $sort: { "enkrypt_scores.hallucination_risk": -1 } },
  { $limit: 50 }
])
```

### 5.6 Atlas Free Tier for Development / Production Entry

MongoDB Atlas offers a permanently free M0 cluster (512MB) suitable for development and early-stage production logging. This allows the platform to use managed MongoDB without infrastructure cost during Phase 1-3. As volume grows, migration to a self-hosted replica set or Atlas M10+ cluster is straightforward.

### 5.7 Replica Set for Durability

MongoDB's replica set (primary + 2 secondaries) provides automatic failover and data durability without the operational complexity of MySQL GTID replication. Read preferences can route HITL dashboard queries to secondaries, preserving primary write throughput.

---

## 6. Cons

### 6.1 Additional Infrastructure Dependency

Every new piece of infrastructure is an operational burden. Introducing MongoDB means the platform now has three database systems (MySQL, MongoDB, Qdrant) — each with its own backup strategy, monitoring, and failure modes.

**Mitigation**: The graceful fallback design (Section 9) ensures that MongoDB failure does not affect platform availability. MongoDB is categorized as **optional Tier-2 infrastructure** — SLA requirements are relaxed compared to MySQL.

### 6.2 Eventual Consistency (in Replica Sets)

With unacknowledged writes (`w=0`) and secondary reads, there is a window of inconsistency where a HITL record written by the AI pipeline is not yet visible to the review dashboard querying a secondary.

**Mitigation**: The HITL review dashboard uses read preference `primaryPreferred` to avoid stale reads on critical review data. The bulk of read traffic (analytics) uses `secondaryPreferred`.

### 6.3 No Transactions Across MySQL and MongoDB

If a session completion event needs to atomically update MySQL (mark session complete) and write a summary to MongoDB (session audit log), there is no cross-database transaction. These operations are eventually consistent.

**Mitigation**: By design, MySQL session records and MongoDB audit logs are separate concerns. MySQL is the source of truth for session state; MongoDB audit logs are observational. A missing MongoDB audit log does not corrupt the MySQL session record. The two are decoupled by design.

### 6.4 Schema-less Does Not Mean Structure-less

MongoDB's flexibility can lead to inconsistent document shapes over time ("schemaless decay"). Without schema enforcement, the `enkrypt_validation_logs` collection could accumulate documents with different field names due to typos or version skew.

**Mitigation**: All audit log documents are produced by the `MongoAuditLogger` service class, which validates against a Pydantic schema before insertion. The Pydantic model enforces structure at the application layer:

```python
class EnkryptValidationLog(BaseModel):
    session_id: str
    agent_id: str
    student_id: int
    timestamp: datetime
    enkrypt_scores: dict[str, float | bool]
    validation_passed: bool
    latency_ms: int
    token_usage: dict[str, int]
    hitl_flagged: bool
    hitl_reason: Optional[str] = None
    model_config = ConfigDict(extra='allow')  # Allow future fields
```

### 6.5 Backup Strategy Complexity

MongoDB's backup approach (mongodump, Atlas backup, or Ops Manager) is different from MySQL's mysqldump workflow. The team must maintain separate backup procedures for each database.

**Mitigation**: For the early phases, MongoDB Atlas automated backups handle this. For self-hosted, `mongodump` is scripted alongside `mysqldump` in the same backup cron job.

---

## 7. Trade-offs

### 7.1 Infrastructure Complexity vs. Operational Safety

| Trade-off Axis                | MongoDB Choice                      | Alternative (MySQL Extension)         |
|-------------------------------|-------------------------------------|---------------------------------------|
| Infrastructure complexity     | Higher (new system)                 | None (existing system)                |
| Write isolation from LMS ops  | Complete                            | None (shared buffer pool)             |
| Schema evolution agility      | Excellent (no migrations needed)    | Poor (ALTER TABLE per field)          |
| Query capability for logs     | Purpose-built                       | Adequate but degraded by volume       |
| Platform resilience           | MongoDB failure isolated             | MySQL overload fails entire platform  |

The core trade-off is: **more infrastructure complexity in exchange for operational safety and schema agility**. This trade-off is accepted because a MongoDB failure is survivable (logs degrade to file); a MySQL overload caused by log write volume is not (LMS goes down).

### 7.2 Developer Experience

Developers must now understand two query languages (SQL + MongoDB aggregation) and two driver APIs (SQLAlchemy + PyMongo). This increases onboarding time.

**Mitigation**: MongoDB usage is entirely encapsulated within `MongoAuditLogger`. Application developers never write raw PyMongo queries — they call high-level methods like `log_enkrypt_validation()`, `log_hitl_flag()`, `get_session_audit_trail()`.

---

## 8. Consequences

### 8.1 Service Architecture

MongoDB is accessed exclusively through the `MongoAuditLogger` service:

```
Mastra Agent → Enkrypt Pipeline → MongoAuditLogger → MongoDB (if available)
                                                    ↓ (fallback)
                                              StructuredFileLogger → /logs/audit/YYYY-MM-DD.jsonl
```

### 8.2 Data Governance

- **Data classification**: AI audit logs are classified as **Platform Operational Data** — not Personal Data under GDPR (they contain `student_id` as a foreign key, not PII directly).
- **PII handling**: If a student's account is deleted, their AI audit logs are anonymized (student_id nullified) within 30 days per retention policy.
- **HITL records** containing reviewer notes are classified as **Internal Review Data** with restricted access (instructor role required to read).

### 8.3 Monitoring Obligations

The following MongoDB health metrics must be monitored:

| Metric                        | Alert Threshold               |
|-------------------------------|-------------------------------|
| Replication lag (replica set) | > 30 seconds                  |
| Connection pool utilization   | > 80%                         |
| Write operation latency (p99) | > 500ms                       |
| Oplog window                  | < 48 hours                    |
| Disk utilization              | > 75%                         |

---

## 9. Graceful Fallback Design

This section documents the most critical design element of this ADR: **MongoDB must be optional infrastructure**.

### 9.1 Rationale

Mentra X operates in environments where MongoDB may not be available:
- **Local development**: Developers without Docker or MongoDB installed must not be blocked from running the platform.
- **MongoDB service failure**: A production MongoDB outage must not cause the AI tutoring pipeline to fail. The student must continue receiving responses.
- **CI/CD environments**: Automated tests must run without a MongoDB instance.

### 9.2 Fallback Architecture

```python
# services/mongo_audit_logger.py

import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

class MongoAuditLogger:
    """
    AI interaction audit logger with graceful MongoDB fallback.
    
    When MongoDB is unavailable, logs are written to structured JSONL files
    in the configured fallback directory. These files can be bulk-imported
    into MongoDB when the connection is restored.
    """
    
    def __init__(self, mongo_uri: Optional[str], fallback_log_dir: str):
        self._mongo_available = False
        self._db = None
        self._fallback_dir = Path(fallback_log_dir)
        self._fallback_dir.mkdir(parents=True, exist_ok=True)
        
        if mongo_uri:
            self._try_connect(mongo_uri)
    
    def _try_connect(self, mongo_uri: str) -> None:
        try:
            from pymongo import MongoClient
            from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
            
            client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=3000,  # 3-second connect timeout
                connectTimeoutMS=3000
            )
            client.admin.command('ping')  # Verify connectivity
            self._db = client['mentrax_audit']
            self._mongo_available = True
            logger.info("MongoAuditLogger: Connected to MongoDB successfully.")
        
        except Exception as e:
            self._mongo_available = False
            logger.warning(
                f"MongoAuditLogger: MongoDB unavailable ({e}). "
                f"Falling back to structured file logging in {self._fallback_dir}"
            )
    
    def _write(self, collection_name: str, document: dict) -> None:
        """Route write to MongoDB or file fallback."""
        document['_logged_at'] = datetime.utcnow().isoformat()
        document['_collection'] = collection_name
        
        if self._mongo_available:
            try:
                from pymongo import WriteConcern
                collection = self._db[collection_name].with_options(
                    write_concern=WriteConcern(w=0)  # Fire-and-forget
                )
                collection.insert_one(document)
                return
            except Exception as e:
                logger.error(f"MongoAuditLogger: Write to MongoDB failed: {e}. Falling back to file.")
        
        # Fallback: structured JSONL file
        log_file = self._fallback_dir / f"{collection_name}_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(document, default=str) + '\n')
    
    def log_enkrypt_validation(self, record: dict) -> None:
        self._write('enkrypt_validation_logs', record)
    
    def log_hitl_flag(self, record: dict) -> None:
        self._write('hitl_review_queue', record)
    
    def log_agent_trace(self, record: dict) -> None:
        self._write('agent_execution_traces', record)
    
    def log_session_metadata(self, record: dict) -> None:
        self._write('session_ai_metadata', record)
    
    def log_twin_mutation(self, record: dict) -> None:
        self._write('twin_mutation_audit', record)
    
    @property
    def is_available(self) -> bool:
        return self._mongo_available
```

### 9.3 Fallback File Recovery

When MongoDB is restored after an outage, the fallback JSONL files can be bulk-imported:

```bash
# Recover fallback logs into MongoDB after restoration
mongoimport \
  --uri "$MONGO_URI" \
  --db mentrax_audit \
  --collection enkrypt_validation_logs \
  --file ./logs/audit/enkrypt_validation_logs_2026-06-28.jsonl \
  --jsonArray
```

A scheduled recovery script runs on MongoDB reconnection to automatically import any accumulated fallback files.

### 9.4 Configuration

```python
# config.py
class ProductionConfig:
    MONGO_URI = os.environ.get('MONGO_URI')  # None = disable MongoDB, use fallback
    MONGO_FALLBACK_LOG_DIR = os.environ.get('MONGO_FALLBACK_LOG_DIR', './logs/audit')

class DevelopmentConfig:
    MONGO_URI = os.environ.get('MONGO_URI', None)  # Optional in dev
    MONGO_FALLBACK_LOG_DIR = './logs/audit'

class TestingConfig:
    MONGO_URI = None  # Always use file fallback in tests
    MONGO_FALLBACK_LOG_DIR = './tests/logs/audit'
```

---

## 10. Implementation Notes

### 10.1 Collection Index Definitions

```python
# services/mongo_setup.py — Run once on deployment

def setup_mongo_collections(db):
    from pymongo import ASCENDING, DESCENDING, IndexModel
    
    # enkrypt_validation_logs
    db.enkrypt_validation_logs.create_indexes([
        IndexModel([("created_at", ASCENDING)], expireAfterSeconds=7776000),  # 90 days TTL
        IndexModel([("session_id", ASCENDING)]),
        IndexModel([("student_id", ASCENDING), ("created_at", DESCENDING)]),
        IndexModel([("hitl_flagged", ASCENDING)], sparse=True),
    ])
    
    # agent_execution_traces
    db.agent_execution_traces.create_indexes([
        IndexModel([("created_at", ASCENDING)], expireAfterSeconds=2592000),  # 30 days TTL
        IndexModel([("session_id", ASCENDING)]),
        IndexModel([("agent_id", ASCENDING), ("created_at", DESCENDING)]),
    ])
    
    # hitl_review_queue — No TTL; manual archival after review
    db.hitl_review_queue.create_indexes([
        IndexModel([("reviewed_at", ASCENDING)], sparse=True),  # Null = unreviewed
        IndexModel([("student_id", ASCENDING)]),
        IndexModel([("flagged_at", DESCENDING)]),
        IndexModel([("escalation_level", DESCENDING)]),
    ])
    
    # session_ai_metadata
    db.session_ai_metadata.create_indexes([
        IndexModel([("created_at", ASCENDING)], expireAfterSeconds=15552000),  # 180 days TTL
        IndexModel([("student_id", ASCENDING), ("created_at", DESCENDING)]),
    ])
    
    # twin_mutation_audit
    db.twin_mutation_audit.create_indexes([
        IndexModel([("created_at", ASCENDING)], expireAfterSeconds=31536000),  # 365 days TTL
        IndexModel([("student_id", ASCENDING)]),
        IndexModel([("twin_state_type", ASCENDING)]),
    ])
```

### 10.2 HITL Review Dashboard Query

```python
# api/hitl_review.py

def get_pending_hitl_reviews(page: int = 1, per_page: int = 20) -> list[dict]:
    """Retrieve unreviewed HITL items sorted by risk severity."""
    pipeline = [
        {"$match": {"reviewed_at": None}},
        {"$addFields": {
            "risk_score": {
                "$max": [
                    "$enkrypt_scores.hallucination_risk",
                    "$enkrypt_scores.toxicity",
                    "$enkrypt_scores.bias"
                ]
            }
        }},
        {"$sort": {"risk_score": -1, "flagged_at": 1}},
        {"$skip": (page - 1) * per_page},
        {"$limit": per_page},
        {"$project": {
            "hitl_id": 1, "session_id": 1, "student_id": 1,
            "flag_reason": 1, "flagged_at": 1, "risk_score": 1,
            "agent_output_suppressed": 1, "escalation_level": 1
        }}
    ]
    return list(mongo_audit_logger._db.hitl_review_queue.aggregate(pipeline))
```

---

## 11. Future Revisions

| Trigger Condition                                      | Recommended Action                                                      |
|--------------------------------------------------------|-------------------------------------------------------------------------|
| Daily log volume exceeds 5M records                    | Evaluate sharded MongoDB cluster or ClickHouse for analytics queries    |
| HITL review workflow requires full-text search         | Sync HITL queue to Elasticsearch for Kibana-based review dashboard      |
| Regulatory requirement for immutable audit logs        | Evaluate WORM-compliant storage (AWS S3 Object Lock) for audit archive  |
| MongoDB Atlas cost exceeds $500/month                  | Migrate to self-hosted replica set on managed VPS                       |
| Enkrypt safety scores need real-time aggregation       | Introduce Redis Streams as intermediate buffer before MongoDB write     |
| Team adopts async Flask (async routes)                 | Replace PyMongo with Motor (async MongoDB driver) for non-blocking I/O  |

---

## 12. References

- [MongoDB — WiredTiger Storage Engine](https://www.mongodb.com/docs/manual/core/wiredtiger/)
- [PyMongo — Official Documentation](https://pymongo.readthedocs.io/en/stable/)
- [MongoDB — TTL Indexes](https://www.mongodb.com/docs/manual/core/index-ttl/)
- [MongoDB — Write Concern](https://www.mongodb.com/docs/manual/reference/write-concern/)
- [Enkrypt AI — Safety Validation API](https://enkryptai.com/docs)
- [Mentra X — ADR-001: MySQL as Primary Relational Database](./ADR-001-MySQL.md)
- [Mentra X — ADR-004: Mastra as Multi-Agent Orchestration Framework](./ADR-004-Mastra.md)
- [Mentra X — System Architecture Overview](../Architecture/system-overview.md)

---

*This document is part of the Mentra X Architecture Decision Record series. All ADRs are stored in `D:\AI-Student Platform\Docs\ADR\` and version-controlled alongside the codebase.*
