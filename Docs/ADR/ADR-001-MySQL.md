# ADR-001: MySQL as Primary Relational Database

| Field       | Value                          |
|-------------|--------------------------------|
| **Status**  | ✅ ACCEPTED                    |
| **Date**    | 2026-06-28                     |
| **Author**  | Sujith Kumar AI                |
| **Deciders**| Platform Architecture Team     |
| **Tags**    | database, storage, relational, lms, production |

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
9. [Implementation Notes](#9-implementation-notes)
10. [Future Revisions](#10-future-revisions)
11. [References](#11-references)

---

## 1. Context

Mentra X is an AI-powered Student Digital Twin and Adaptive Learning Platform built on top of an existing, production-grade Learning Management System (LMS). The LMS predates the Mentra X AI layer and has been in operation with real users. At the time of this decision, the platform serves **31 active users** and manages all academic workflows through a relational schema.

### Existing Database State

The production MySQL database comprises **34 tables** spanning the following functional domains:

| Domain                  | Table Count | Representative Tables                                          |
|-------------------------|-------------|---------------------------------------------------------------|
| User Identity & Auth    | 4           | `users`, `roles`, `user_roles`, `sessions`                    |
| Academic Structure      | 6           | `courses`, `modules`, `lessons`, `enrollments`, `sections`    |
| Assessment & Grading    | 5           | `quizzes`, `quiz_questions`, `quiz_attempts`, `grades`, `rubrics` |
| Skill Tracking          | 4           | `skills`, `user_skills`, `skill_categories`, `skill_progress` |
| Community & Engagement  | 4           | `posts`, `comments`, `reactions`, `community_groups`          |
| Career & Employability  | 5           | `resumes`, `resume_sections`, `job_listings`, `applications`, `interview_sessions` |
| Notifications & Events  | 3           | `notifications`, `events`, `event_registrations`              |
| Platform Config         | 3           | `settings`, `feature_flags`, `audit_log`                      |

This schema is fully normalized, actively written to by user workflows (course enrollment, quiz submission, skill updates), and is the **system of record** for all business-critical data.

### Technology Stack at Decision Time

- **Runtime**: Python 3.11 / Flask 3.x
- **ORM**: SQLAlchemy 2.x (Core + ORM modes)
- **Driver**: PyMySQL 1.1.x
- **Hosting**: MySQL 8.0 (self-hosted or managed cloud instance)
- **Migration Tool**: Alembic
- **Connection Pool**: SQLAlchemy's built-in pool (QueuePool, pool_size=10)

### AI Layer Integration

The Mentra X AI layer (Mastra agents, Qdrant vector memory, Enkrypt safety) consumes structured data from MySQL in several ways:

- **Agent context hydration**: The Orchestrator Agent reads `user_skills`, `quiz_attempts`, and `enrollments` to construct the context payload for AI tutoring sessions.
- **Digital Twin population**: Student Digital Twin state initialization reads from MySQL to build the baseline Academic State and Knowledge State.
- **HITL audit enrichment**: Human-in-the-Loop (HITL) flags are cross-referenced with `users` and `sessions` tables.
- **Career recommendations**: The Opportunity Pathfinder Agent reads `resumes` and `user_skills` to generate personalized opportunity mappings.

This integration makes MySQL not just a passive data store but an **active participant** in the AI reasoning pipeline.

---

## 2. Problem Statement

With the AI layer being layered on top of an existing production system, the architecture team must formally answer the following question:

> **Which relational database system should serve as the single source of truth for all structured LMS data, user records, academic history, assessment results, skill progression, and career data within the Mentra X platform?**

The decision must account for:

1. **Existing production data** — Migrating 34 tables of live data carries real risk and must be justified.
2. **ORM compatibility** — SQLAlchemy must interface cleanly with the chosen database.
3. **AI layer read patterns** — Agents issue complex joins (e.g., user → skills → quiz history → course enrollment) that require a performant query planner.
4. **Write throughput** — Assessment submissions, session updates, and skill mutations can occur concurrently.
5. **Operational cost** — The platform is at MVP/early scale. Operational overhead matters.
6. **Developer familiarity** — The existing engineering team has MySQL expertise baked into the existing codebase.

---

## 3. Decision

**We will use MySQL 8.0 as the primary relational database, accessed through SQLAlchemy ORM with the PyMySQL driver.**

This decision preserves the existing production database schema, avoids a costly and risky migration, and provides a fully-featured RDBMS that satisfies all current and near-term requirements. The following constraints are binding:

- All structured, schema-bound data **must** go through MySQL.
- SQLAlchemy models define the canonical schema — raw SQL is permitted only for migrations and complex aggregation queries.
- PyMySQL is the sole approved driver; `mysql-connector-python` is explicitly disallowed to avoid version conflicts.
- Schema changes must be managed through **Alembic migrations** — no ad-hoc `ALTER TABLE` in production.
- The AI layer **must not** write directly to MySQL; all writes flow through Flask service layers.

---

## 4. Alternatives Considered

### 4.1 Comparison Matrix

| Criterion                        | MySQL 8.0 ✅         | PostgreSQL 16         | SQLite 3              | PlanetScale (Serverless) |
|----------------------------------|----------------------|-----------------------|-----------------------|--------------------------|
| **Existing schema compatibility**| Native (34 tables)   | Requires migration    | Requires migration    | Requires migration       |
| **SQLAlchemy ORM support**       | First-class          | First-class           | First-class           | Partial (vitess quirks)  |
| **PyMySQL driver**               | Native               | N/A (psycopg2)        | Built-in              | MySQL-compatible          |
| **Full-text search**             | FULLTEXT indexes     | tsvector/GIN (superior)| Basic FTS             | Limited                  |
| **JSON column support**          | JSON type (MySQL 8)  | JSONB (superior)      | JSON as TEXT          | JSON type                |
| **Window functions**             | ✅ (MySQL 8.0+)       | ✅                     | ✅ (3.25+)             | ✅                        |
| **CTEs (WITH clause)**           | ✅ (MySQL 8.0+)       | ✅                     | ✅                     | ✅                        |
| **Horizontal scaling**           | Read replicas         | Read replicas          | ❌ (single file)       | Built-in (sharding)       |
| **Managed cloud options**        | RDS, CloudSQL, PlanetScale | RDS, Supabase   | ❌                     | PlanetScale native        |
| **Operational cost (self-host)** | Low                  | Low                   | Zero                  | Per-query billing         |
| **Migration risk**               | None (existing DB)   | High                  | Medium                | High                     |
| **Community ecosystem**          | Large                | Very large            | Large                 | Growing                  |
| **ACID guarantees**              | ✅ (InnoDB)           | ✅                     | ✅                     | ✅                        |
| **Foreign key enforcement**      | ✅ (InnoDB)           | ✅                     | Optional              | ❌ (vitess limitation)    |
| **GIS / spatial support**        | Basic                | PostGIS (excellent)   | SpatiaLite            | ❌                        |
| **Replication**                  | GTIDs, binlog        | WAL streaming         | ❌                     | Managed                  |
| **Branch/preview databases**     | Manual               | Manual / Supabase      | Manual                | ✅ Native                  |

### 4.2 PostgreSQL Analysis

PostgreSQL is technically superior to MySQL in several dimensions: its JSONB storage with GIN indexing outperforms MySQL's JSON type, its query planner is more sophisticated, and its extension ecosystem (PostGIS, pg_trgm, pgvector) is broader. However, migrating 34 tables of production LMS data with live users carries substantial risk:

- **Data type mapping**: MySQL's `TINYINT(1)` booleans, `ENUM` types, and `TEXT` defaults do not map cleanly to PostgreSQL.
- **SQL dialect differences**: Existing Flask route handlers and SQLAlchemy queries use MySQL-specific behaviors (e.g., `LIMIT x OFFSET y`, `GROUP BY` non-strict mode).
- **Driver change**: Moving from PyMySQL to psycopg2/asyncpg requires regression testing across all 34 models.
- **No demonstrated need**: None of the current Mentra X features require PostgreSQL-specific capabilities. The use of pgvector for vector storage was considered but rejected in favor of Qdrant (see ADR-003).

**Verdict**: Technically superior but not worth migration cost at current scale. Revisit when pgvector maturity or PostGIS need arises.

### 4.3 SQLite Analysis

SQLite is appropriate for local development and testing but is fundamentally unsuitable for a multi-user, concurrent-write production system. Mentra X serves 31 users today and is designed to scale to thousands. SQLite's write-serialization model (only one writer at a time), lack of a network server, and absence of row-level locking make it a non-starter for production.

**Verdict**: Acceptable for local dev/test environments only. Already configured as a fallback in development `config.py`.

### 4.4 PlanetScale Analysis

PlanetScale is a MySQL-compatible serverless database built on Vitess (YouTube's scaling layer). It offers compelling features: branching for schema changes, auto-scaling, and zero-downtime migrations. However, it has a critical limitation for Mentra X:

- **No foreign key constraints**: Vitess's sharding model disallows cross-shard foreign keys. Mentra X's schema relies heavily on foreign keys (e.g., `quiz_attempts.user_id → users.id`, `enrollments.course_id → courses.id`) for data integrity.
- **Cost model**: PlanetScale charges per row read/row written. AI agent context hydration (reading large sets of user history) could create unpredictable billing at scale.
- **Vendor lock-in**: PlanetScale's proprietary branching and deploy request workflow ties schema management to their platform.

**Verdict**: Attractive serverless model but foreign key removal is a hard blocker given existing schema integrity requirements.

---

## 5. Pros

### 5.1 Zero Migration Risk
The production database already exists with 34 tables, active data, and running application code. Choosing MySQL means zero data migration, zero schema transformation, and zero risk of data loss during transition.

### 5.2 Full ORM Parity
SQLAlchemy's MySQL dialect is mature and fully featured. All ORM features used in the existing codebase — relationships, eager loading, lazy loading, hybrid properties, and event hooks — work identically. The PyMySQL driver is stable, well-maintained, and already installed.

### 5.3 AI Layer Compatibility
MySQL's JSON column type (MySQL 8.0+) allows storing semi-structured agent context payloads alongside structured relational data when needed. The `information_schema` and `EXPLAIN ANALYZE` tooling allow the team to optimize AI-driven query patterns (complex joins across skill, quiz, and enrollment tables).

### 5.4 Operational Familiarity
The existing engineering team has institutional knowledge of MySQL operations: backup/restore via `mysqldump`, replication setup via binary logs, slow query analysis via `pt-query-digest`, and performance tuning via `EXPLAIN`. This reduces operational overhead compared to introducing a new database engine.

### 5.5 MySQL 8.0 Feature Parity
MySQL 8.0 introduced several features that close the historical gap with PostgreSQL:
- **Window functions**: `ROW_NUMBER()`, `RANK()`, `LAG()`, `LEAD()` — used for student progress analytics.
- **CTEs**: `WITH RECURSIVE` — used for hierarchical course module traversal.
- **Invisible indexes**: Allow performance testing without schema changes.
- **Atomic DDL**: Schema changes are now transactional.
- **Role-based access control**: Per-application user roles.
- **Descending indexes**: Optimize ORDER BY DESC queries for leaderboard and ranking features.

### 5.6 Managed Hosting Flexibility
MySQL is available as a managed service on every major cloud provider (AWS RDS, Google Cloud SQL, Azure Database for MySQL) without vendor lock-in. The platform can migrate to any managed provider without changing application code.

### 5.7 Alembic Migration Discipline
By standardizing on Alembic for all DDL changes, the team gains version-controlled, reproducible schema evolution. Every schema change is a committed, reviewable migration file — no undocumented `ALTER TABLE` statements in production.

---

## 6. Cons

### 6.1 JSON Support is Second-Class
MySQL's `JSON` column type does not support GIN indexing. Complex JSON path queries (`JSON_EXTRACT`, `JSON_TABLE`) are slower than PostgreSQL's JSONB with GIN indexes. For the AI layer's need to store and query structured context payloads, this means JSON data requiring high-frequency queries should be promoted to normalized columns.

**Mitigation**: Semi-structured AI data (agent logs, Enkrypt scores) are stored in MongoDB (see ADR-002), not MySQL JSON columns.

### 6.2 Full-Text Search Limitations
MySQL's `FULLTEXT` index and `MATCH() AGAINST()` syntax is functional but limited compared to Elasticsearch or PostgreSQL's `tsvector`. It lacks fuzzy matching, phonetic matching, and custom ranking functions.

**Mitigation**: Semantic search over student knowledge is handled by Qdrant (see ADR-003). MySQL FULLTEXT is only used for administrative content search (course titles, lesson descriptions), where exact phrase matching is sufficient.

### 6.3 Strict Mode Inconsistencies
MySQL's `STRICT_TRANS_TABLES` mode must be explicitly enabled to get ANSI-standard behavior for out-of-range values and truncation. In non-strict mode, MySQL silently truncates data, which can cause subtle bugs.

**Mitigation**: `STRICT_TRANS_TABLES` and `NO_ZERO_DATE` are set in `my.cnf` and enforced via the SQLAlchemy connection string: `?sql_mode=STRICT_TRANS_TABLES`.

### 6.4 No Native Branching
Unlike PlanetScale, MySQL has no native concept of database branches for feature development. Schema changes must be managed carefully across environments (development, staging, production).

**Mitigation**: Alembic's version-controlled migrations combined with environment-specific connection strings provide adequate schema environment isolation.

### 6.5 Limited Parallelism for Complex Queries
MySQL's query execution engine is less parallelized than PostgreSQL's for analytical queries. Complex aggregations (e.g., platform-wide skill gap analysis across all students) will be slower in MySQL.

**Mitigation**: Complex analytics are computed offline via scheduled jobs and cached. Real-time AI queries are optimized to be selective (user-scoped) rather than platform-wide.

---

## 7. Trade-offs

### 7.1 Stability vs. Technical Optimality

| Dimension                  | MySQL Choice       | Optimal Alternative          |
|----------------------------|--------------------|------------------------------|
| Migration risk             | Zero               | High (PostgreSQL)            |
| JSON query performance     | Acceptable         | Superior (PostgreSQL JSONB)  |
| Full-text search           | Adequate           | Superior (Elasticsearch)     |
| Vector search              | Not applicable     | pgvector (PostgreSQL)        |
| Operational familiarity    | High               | Lower (PostgreSQL)           |
| Schema branching           | None               | Native (PlanetScale)         |

The primary trade-off is **operational stability and zero migration risk versus technical capability**. MySQL is not the most technically capable database for all of Mentra X's needs — but it is the right choice given that the system is already in production, the AI layer has specialized stores (MongoDB, Qdrant) for non-relational needs, and the cost of migration outweighs the benefits at current scale.

### 7.2 Monolithic Schema vs. Microservice Per Domain

This decision implicitly accepts a **monolithic schema** — all 34 tables in one database. At 31 users, database-level domain separation (separate MySQL instances per domain: LMS, career, community) would add operational complexity with no throughput benefit. This trade-off will be revisited at scale (>10,000 users).

### 7.3 Synchronous ORM vs. Async

SQLAlchemy 2.x supports async operations via `asyncio` + `aiomysql`. The current codebase uses synchronous SQLAlchemy (Flask's request-per-thread model). Introducing async would require refactoring Flask to use async routes or migrating to FastAPI — a significant cost not justified by current traffic.

---

## 8. Consequences

### 8.1 Immediate Consequences

- **All new LMS features** must extend the existing MySQL schema via Alembic migrations.
- **AI layer data contracts** must be defined at the SQLAlchemy model layer — agents read from ORM models, not raw SQL.
- **No new JSON column sprawl** — semi-structured data must go to MongoDB (ADR-002) or be normalized into MySQL tables.
- **Development environments** must run a local MySQL 8.0 instance (or Docker: `mysql:8.0`) — SQLite is acceptable only for unit tests with in-memory databases.

### 8.2 Schema Evolution Governance

Every schema change must follow this protocol:
1. Write Alembic migration in `migrations/versions/`
2. Test migration on a database dump from production (anonymized)
3. Review migration in pull request — DBA/lead engineer approval required for table creation/deletion
4. Deploy migration during off-peak hours
5. Maintain backward-compatible migrations where possible (add columns with defaults; never drop without deprecation period)

### 8.3 AI Agent Data Access Patterns

Agents must access MySQL data through defined **Repository classes** (not direct SQLAlchemy Session access):

```python
# CORRECT: Repository pattern
class StudentRepository:
    def get_skill_profile(self, user_id: int) -> SkillProfile:
        return db.session.query(UserSkill).filter_by(user_id=user_id).all()

# INCORRECT: Direct session in agent code
skills = db.session.execute("SELECT * FROM user_skills WHERE user_id = ?", [user_id])
```

This ensures that AI agent data access is testable, mockable, and insulated from schema changes.

### 8.4 Performance Baselines

The following query performance budgets are established:

| Query Type                                | Max Acceptable Time |
|-------------------------------------------|---------------------|
| Single user profile lookup                | < 5ms               |
| User skill profile (all skills)           | < 20ms              |
| Quiz history for one user                 | < 30ms              |
| Course enrollment with module progress    | < 50ms              |
| Agent context hydration (full user state) | < 100ms             |
| Platform analytics aggregation            | < 2000ms (scheduled)|

Queries exceeding these budgets must be optimized via indexing, denormalization, or caching (Redis/Memcached) before production deployment.

### 8.5 Connection Pool Configuration

```python
# config.py — Production database configuration
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,
    "max_overflow": 20,
    "pool_recycle": 3600,          # Recycle connections every hour
    "pool_pre_ping": True,          # Verify connection health before use
    "connect_args": {
        "connect_timeout": 10,
        "sql_mode": "STRICT_TRANS_TABLES,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO"
    }
}
```

### 8.6 Backup and Recovery Obligations

- **Daily logical backups**: `mysqldump` to encrypted S3-compatible storage, 30-day retention.
- **Point-in-time recovery**: Binary logging enabled; PITR window of 7 days.
- **Recovery time objective (RTO)**: < 1 hour for full restore from latest backup.
- **Recovery point objective (RPO)**: < 5 minutes via binlog replay.

---

## 9. Implementation Notes

### 9.1 SQLAlchemy Model Conventions

All models follow these conventions:

```python
from datetime import datetime
from extensions import db

class BaseModel(db.Model):
    """Abstract base for all Mentra X MySQL models."""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                           onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self) -> dict:
        """Serialize model to dictionary for agent context payloads."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
```

### 9.2 Alembic Migration Template

```python
# migrations/versions/YYYYMMDD_HHMMSS_description.py
"""Add skill_gap_score to user_skills

Revision ID: abc123def456
Revises: prev_revision_id
Create Date: 2026-06-28 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('user_skills',
        sa.Column('gap_score', sa.Float(), nullable=True, comment='AI-computed skill gap score [0.0-1.0]')
    )

def downgrade():
    op.drop_column('user_skills', 'gap_score')
```

### 9.3 Index Strategy for AI Query Paths

```sql
-- Agent context hydration indexes
CREATE INDEX idx_user_skills_user_id ON user_skills(user_id);
CREATE INDEX idx_quiz_attempts_user_course ON quiz_attempts(user_id, course_id);
CREATE INDEX idx_enrollments_user_active ON enrollments(user_id, status) WHERE status = 'active';
CREATE INDEX idx_sessions_user_created ON sessions(user_id, created_at DESC);
```

---

## 10. Future Revisions

This decision should be revisited under the following conditions:

| Trigger Condition                                      | Recommended Action                                                |
|--------------------------------------------------------|-------------------------------------------------------------------|
| Platform exceeds 50,000 users                          | Evaluate read replicas; introduce Redis caching layer             |
| AI analytics require complex cross-table aggregations  | Evaluate read replica + columnar engine (MySQL HeatWave or BigQuery sync) |
| Need for pgvector integration for in-DB vector search  | Evaluate PostgreSQL migration with `pgloader` tool                |
| PlanetScale removes foreign key restriction            | Re-evaluate PlanetScale for horizontal scalability                |
| Platform introduces multi-tenancy                      | Evaluate schema-per-tenant or database-per-tenant model           |
| MySQL EOL for version 8.0                              | Plan migration to MySQL 8.4 LTS or MySQL 9.x                     |
| Reporting/analytics workload exceeds 10s per query     | Introduce dedicated OLAP store (ClickHouse, BigQuery)             |

The decision to remain on MySQL should be **affirmatively confirmed or challenged** at the following milestones:
- **1,000 active users**: Confirm indexes and pool configuration are holding.
- **10,000 active users**: Full performance audit; consider read replicas.
- **100,000 active users**: Re-evaluate entire database architecture; MySQL monolith likely needs sharding strategy.

---

## 11. References

- [MySQL 8.0 Reference Manual — InnoDB Storage Engine](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html)
- [SQLAlchemy 2.0 — MySQL Dialect](https://docs.sqlalchemy.org/en/20/dialects/mysql.html)
- [Alembic — Auto-generating Migrations](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
- [PyMySQL — GitHub Repository](https://github.com/PyMySQL/PyMySQL)
- [PlanetScale — Foreign Key Constraints](https://planetscale.com/docs/learn/operating-without-foreign-key-constraints)
- [Mentra X — System Architecture Overview](../Architecture/system-overview.md)
- [Mentra X — ADR-002: MongoDB as AI Interaction Audit Log Store](./ADR-002-MongoDB.md)
- [Mentra X — ADR-003: Qdrant as Vector Memory Engine](./ADR-003-Qdrant.md)

---

*This document is part of the Mentra X Architecture Decision Record series. All ADRs are stored in `D:\AI-Student Platform\Docs\ADR\` and version-controlled alongside the codebase.*
