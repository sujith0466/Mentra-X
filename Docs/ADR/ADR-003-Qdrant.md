# ADR-003: Qdrant as Vector Memory Engine

| Field       | Value                                              |
|-------------|----------------------------------------------------|
| **Status**  | ✅ ACCEPTED                                        |
| **Date**    | 2026-06-28                                         |
| **Author**  | Sujith Kumar AI                                    |
| **Deciders**| Platform Architecture Team                         |
| **Tags**    | vector-database, semantic-search, digital-twin, qdrant, memory, embeddings |

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
9. [5-Collection Architecture Rationale](#9-5-collection-architecture-rationale)
10. [Implementation Notes](#10-implementation-notes)
11. [Future Revisions](#11-future-revisions)
12. [References](#12-references)

---

## 1. Context

### 1.1 The Student Digital Twin Model

The foundational intelligence of Mentra X is the **Student Digital Twin** — a live, evolving computational model of each student's cognitive and academic profile. The twin is not a snapshot; it is a continuously mutated state object that reflects learning history, behavioral patterns, and knowledge topology.

The twin comprises **seven state dimensions**:

| State Dimension         | Description                                                                              | Data Character                        |
|-------------------------|------------------------------------------------------------------------------------------|---------------------------------------|
| **Academic State**      | Course enrollment, grades, assignment completion, GPA trajectory                         | Structured (MySQL)                    |
| **Knowledge State**     | Conceptual understanding map — what the student knows, misunderstands, or hasn't reached | Semantic (Qdrant)                     |
| **Skill State**         | Technical and soft skill proficiencies with evidence markers                             | Structured + Semantic (MySQL + Qdrant)|
| **Learning DNA**        | Preferred explanation modality, pacing pattern, error-response pattern, time-of-day bias | Behavioral / Semantic (Qdrant)        |
| **Career State**        | Career aspirations, industry fit signals, opportunity readiness score                    | Structured + Semantic (MySQL + Qdrant)|
| **Project State**       | Active and completed project portfolio with AI-assessed quality metrics                  | Structured (MySQL) + Semantic (Qdrant)|
| **Opportunity State**   | Curated opportunity matches (jobs, scholarships, competitions) with fit scores           | Semantic (Qdrant)                     |

The **semantic dimensions** (Knowledge, Learning DNA, Career, Opportunity, and components of Skill and Project) require a storage layer that can answer questions like:

- *"What concepts similar to 'dynamic programming' has this student struggled with?"*
- *"Find past explanations about recursion that this student rated highly."*
- *"Which behavioral patterns from this student's history suggest visual learning preference?"*
- *"What past doubts are semantically similar to the current question about gradient descent?"*

These queries cannot be answered by exact-match database lookups. They require **semantic similarity search** over high-dimensional vector embeddings.

### 1.2 Embedding Model

All text data entering the vector memory is embedded using **text-embedding-3-small** (OpenAI), producing 1,536-dimensional float32 vectors. The embedding pipeline runs in the Mastra agent layer before Qdrant writes. The similarity metric for all collections is **Cosine Similarity** — appropriate for comparing semantic meaning where magnitude is not the distinguishing factor.

### 1.3 Access Patterns

Vector memory in Mentra X has two distinct access patterns:

**Pattern A — Real-time tutoring reads** (latency-critical):
- Triggered during live AI tutoring sessions
- Query: "Find the 5 past explanations most similar to the current student question"
- Requirement: < 150ms end-to-end (Qdrant query budget: < 50ms)
- Frequency: Multiple times per tutoring session

**Pattern B — Twin mutation writes** (high-frequency):
- Triggered at end of each session or milestone event
- Operation: Upsert new knowledge state points, Learning DNA embeddings, session summaries
- Requirement: Non-blocking (async write acceptable)
- Frequency: ~6-12 upserts per user session

**Pattern C — Offline intelligence synthesis** (batch):
- Triggered by cron-scheduled Weakness Intelligence Agent
- Operation: Bulk scan over a student's full knowledge state to identify weakness clusters
- Requirement: < 5 seconds for a student with 500 historical knowledge points
- Frequency: Daily or after significant learning milestone

### 1.4 Isolation and Filtering Requirements

A fundamental requirement is **per-user isolation** at the vector layer. A query for "recursive algorithms knowledge for student 42" must never return results from student 17's memory. Qdrant's **payload filter** system allows embedding a `student_id` in the point payload and filtering queries by this field — providing user-level data isolation without separate collections per user (which would be thousands of collections).

---

## 2. Problem Statement

> **Where should the Student Digital Twin's semantic memory live — the store that holds behavioral embeddings, knowledge state vectors, explanation histories, session summaries, and weakness clusters — such that it supports: per-user payload filtering, cosine similarity search, real-time reads in < 150ms during live tutoring sessions, high-frequency writes during twin mutations, and batch scan for the Weakness Intelligence Agent's daily computation?**

Additional constraints:

| Requirement                          | Specification                                                                 |
|--------------------------------------|-------------------------------------------------------------------------------|
| Embedding dimensionality             | 1,536 (text-embedding-3-small) — must support without truncation              |
| Per-user isolation                   | Queries must filter by `student_id` payload field — no cross-student leakage  |
| Vector count per user (steady state) | ~500–2,000 points (across all collections)                                    |
| Vector count at platform scale       | ~5M–20M points total at 10,000 users                                          |
| Upsert support                       | Twin mutations update existing points — upsert semantics required             |
| Metadata storage                     | Each point stores a payload (JSON) with rich metadata                         |
| Self-hostable                        | Must not require a cloud-managed service for production operation             |
| Open-source license                  | Must be available under an OSI-approved license                               |

---

## 3. Decision

**We will use Qdrant as the vector memory engine for the Student Digital Twin, organized into 5 purpose-built collections, accessed via the `qdrant-client` Python library.**

### 3.1 Binding Constraints

- Qdrant is the **sole** vector storage system in Mentra X. `pgvector`, in-memory numpy arrays, and other vector stores are explicitly disallowed.
- All vector writes go through the **`VectorMemoryService`** class — no direct qdrant-client calls in agent code.
- All queries **must** include a `student_id` payload filter — unfiltered (global) searches are only permitted in administrative analytics contexts with explicit audit logging.
- Vector points are **never deleted** during normal operation; they are soft-deleted via `is_active: false` payload flag. Hard deletion only occurs during account termination.
- The **5-collection architecture** is fixed for Phase 1-4. Additional collections require a new ADR revision.

### 3.2 Qdrant Configuration

```yaml
# qdrant/config.yaml — Production configuration
storage:
  storage_path: /qdrant/storage
  
service:
  host: 0.0.0.0
  http_port: 6333
  grpc_port: 6334
  
performance:
  max_search_threads: 0  # Auto-detect CPU count
  
optimizers:
  default_segment_number: 4
  memmap_threshold: 50000  # HNSW graph kept in RAM below this; mmap above
```

### 3.3 Client Configuration

```python
# services/vector_memory/client.py
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

def create_qdrant_client(host: str, port: int, api_key: str = None) -> QdrantClient:
    return QdrantClient(
        host=host,
        port=port,
        api_key=api_key,  # For cloud deployments
        timeout=10.0,      # 10-second operation timeout
        prefer_grpc=True   # gRPC for lower latency on search operations
    )
```

---

## 4. Alternatives Considered

### 4.1 Comparison Matrix

| Criterion                          | Qdrant ✅             | Pinecone              | Weaviate              | pgvector (PostgreSQL) | Chroma                | In-Memory (numpy)     |
|------------------------------------|----------------------|-----------------------|-----------------------|-----------------------|-----------------------|-----------------------|
| **Self-hostable**                  | ✅ Native             | ❌ (SaaS only)         | ✅                     | ✅ (extension)         | ✅                     | N/A                   |
| **Open-source license**            | Apache 2.0           | ❌ Proprietary         | BSD-3-Clause          | PostgreSQL License    | Apache 2.0            | BSD (numpy)           |
| **Payload filtering**              | ✅ Excellent          | ✅ Metadata filtering  | ✅ Where filter        | ✅ SQL WHERE           | ✅ Basic               | Manual                |
| **Cosine similarity**              | ✅                    | ✅                     | ✅                     | ✅                     | ✅                     | ✅                     |
| **1,536-dim vector support**       | ✅                    | ✅                     | ✅                     | ✅ (up to 2000)        | ✅                     | ✅                     |
| **Upsert semantics**               | ✅ Native             | ✅                     | ✅                     | ✅ (INSERT ON CONFLICT) | ✅                   | Manual                |
| **Real-time read latency (p50)**   | 5–20ms               | 10–30ms               | 10–30ms               | 30–100ms (cold)       | 20–50ms               | 1–5ms                 |
| **Batch scan (10K vectors)**       | < 200ms              | < 500ms (API limit)   | < 300ms               | < 1000ms              | < 500ms               | < 50ms                |
| **Persistence**                    | ✅ On-disk + memmap   | ✅ Managed             | ✅ On-disk             | ✅ PostgreSQL storage  | ✅ On-disk (SQLite)   | ❌ (RAM only)          |
| **HNSW index quality**             | Excellent (custom impl) | Managed (opaque)   | Excellent             | Good                  | Good                  | N/A                   |
| **gRPC transport**                 | ✅                    | ❌ (HTTP only)         | ✅                     | N/A                   | ❌                     | N/A                   |
| **Sparse vector support**          | ✅ (hybrid search)    | ✅                     | ✅                     | ❌                     | ❌                     | Manual                |
| **Quantization (memory reduction)**| ✅ (scalar, product)  | Managed               | ✅                     | ❌                     | ❌                     | N/A                   |
| **Python client quality**          | Excellent            | Good                  | Good                  | psycopg2/sqlalchemy   | Good                  | numpy                 |
| **Managed cloud option**           | Qdrant Cloud         | ✅ Native              | WCS (Weaviate Cloud)  | Supabase, Neon        | ❌                     | N/A                   |
| **Cost at 10M vectors**            | Self-host: Low        | ~$700/month (p2 pod)  | Self-host: Low         | Depends on PostgreSQL | Self-host: Low         | Unsustainable (RAM)   |

### 4.2 Pinecone Analysis

Pinecone is the most mature managed vector database and powers numerous production AI applications. Its developer experience is excellent, and its managed infrastructure removes operational burden.

Critical disqualifiers for Mentra X:

1. **SaaS only**: Pinecone has no self-hosted option. All data (student knowledge states, behavioral profiles) must be transmitted to Pinecone's servers. This raises data sovereignty and privacy concerns for student behavioral data.
2. **Cost at scale**: Pinecone's p2 pod pricing at 10M vectors is ~$700/month. A self-hosted Qdrant instance on equivalent hardware costs ~$50/month in cloud compute.
3. **Vendor dependency**: A Pinecone outage or pricing change directly disrupts the tutoring pipeline. No migration path without full data re-embedding.
4. **Index namespace limits**: Pinecone's namespace model for per-user isolation has limits that require careful management at scale.

**Verdict**: Excellent technology but vendor lock-in, data sovereignty concerns, and cost model are blockers. Self-hosting requirement is non-negotiable given student data sensitivity.

### 4.3 Weaviate Analysis

Weaviate is a strong competitor with a rich module ecosystem (built-in vectorizers, generative modules) and a sophisticated GraphQL query interface. It has excellent HNSW implementation and supports both semantic and keyword hybrid search natively.

- **Operational weight**: Weaviate's Docker image is significantly heavier than Qdrant's (~1.2GB vs ~150MB for Qdrant). Its dependency on Java's JVM heritage (Go rewrite is newer) means higher memory baseline.
- **Schema definition overhead**: Weaviate requires explicit class/property schema definitions in its configuration — more similar to a traditional database. This adds friction for the flexible payload metadata in Mentra X's twin records.
- **Python client**: Weaviate's Python client (`weaviate-client`) is well-maintained but the API is more verbose than Qdrant's for the specific operations Mentra X needs (upsert, filtered search).
- **Strong competitor**: Weaviate would be an acceptable alternative. The decision for Qdrant over Weaviate is marginal and based primarily on Qdrant's lighter footprint and simpler payload model.

**Verdict**: Acceptable alternative. If Qdrant becomes unsuitable (see Future Revisions), Weaviate is the first migration target.

### 4.4 pgvector Analysis

pgvector is a PostgreSQL extension that adds vector similarity search to existing PostgreSQL instances. Its appeal is infrastructure consolidation: combine relational data and vector data in one system.

However, for Mentra X's specific requirements, pgvector has critical limitations:

1. **Mentra X uses MySQL, not PostgreSQL**: pgvector is a PostgreSQL-only extension. Adopting pgvector would require introducing a PostgreSQL instance — adding infrastructure complexity without consolidation benefit, since MySQL (ADR-001) remains the primary relational store.
2. **Performance at scale**: pgvector's HNSW implementation is good but operates within PostgreSQL's shared memory and executor framework. At 10M+ vectors with concurrent tutoring queries, PostgreSQL's MVCC overhead and shared buffer competition with relational queries would degrade latency beyond the 150ms budget.
3. **No gRPC**: pgvector queries go through the SQL wire protocol — slower than Qdrant's gRPC binary transport for high-frequency vector searches.
4. **Limited quantization**: pgvector does not support scalar or product quantization, meaning memory requirements for 10M × 1536-dim float32 vectors would be ~60GB — cost-prohibitive on single-instance PostgreSQL.

**Verdict**: Wrong database engine (PostgreSQL) for the existing stack, insufficient performance isolation from relational workload, and no quantization support. Hard reject.

### 4.5 Chroma Analysis

Chroma is a popular embedding database, particularly in prototype and RAG application development. It is lightweight, easy to run, and has a clean Python API.

- **Production readiness concerns**: Chroma's production story has historically been weaker than Qdrant's. Its distributed mode (Chroma Cloud) is newer and less battle-tested.
- **No gRPC**: HTTP-only transport adds latency overhead on the critical tutoring path.
- **No quantization**: Same memory concern as pgvector at scale.
- **Limited filtering**: Chroma's `where` filter is functional but less expressive than Qdrant's payload filter language (especially for compound conditions needed by the Weakness Intelligence Agent).
- **SQLite backing store**: Chroma's default persistence through SQLite is a bottleneck for high-frequency upserts during twin mutations.

**Verdict**: Acceptable for prototyping and local development but not production-grade for Mentra X's scale and query requirements.

### 4.6 In-Memory numpy Analysis

Storing embedding vectors in numpy arrays (or similar in-memory structures) within the application process provides the lowest possible search latency (< 5ms) but is fundamentally unsuitable:

- **No persistence**: Vectors are lost on process restart. Student Digital Twin memory would be ephemeral.
- **No scaling**: A single Flask process cannot hold 10M × 1536-dim float32 vectors (60GB RAM) in memory.
- **No filtering**: Per-user isolation requires manual array slicing — O(n) scan rather than indexed lookup.
- **No concurrent access**: Multiple Flask workers cannot share an in-memory numpy store.

**Verdict**: Useful only for unit testing with small synthetic datasets. Never for production.

---

## 5. Pros

### 5.1 HNSW Index Performance

Qdrant implements its own Hierarchical Navigable Small World (HNSW) graph index, optimized specifically for approximate nearest neighbor (ANN) search. Benchmark results on 1,536-dimensional vectors at 1M points show p50 query latency of 5–15ms, well within the 50ms Qdrant query budget for the real-time tutoring path.

### 5.2 Payload Filter Integration with HNSW

Qdrant's killer feature is its **payload filter integration with the HNSW traversal**. Unlike post-filter approaches (search globally, then filter results), Qdrant applies the payload filter during graph traversal — dramatically reducing unnecessary computation when filtering by `student_id`.

```python
# Qdrant's filter is applied DURING HNSW traversal, not after
results = client.search(
    collection_name="knowledge_state",
    query_vector=question_embedding,
    query_filter=Filter(
        must=[FieldCondition(key="student_id", match=MatchValue(value=42))]
    ),
    limit=5
)
# Only student 42's vectors are traversed — O(log n per student) not O(n total)
```

### 5.3 Quantization for Memory Efficiency

Qdrant supports **scalar quantization** (float32 → int8, 4x memory reduction) and **product quantization** (up to 64x reduction with acceptable recall degradation). For Mentra X's steady-state of 5–20M vectors at platform scale, scalar quantization maintains > 97% recall while reducing RAM from ~60GB to ~15GB.

```python
from qdrant_client.http.models import ScalarQuantizationConfig, ScalarType, QuantizationConfig

collection_config = VectorParams(
    size=1536,
    distance=Distance.COSINE,
    on_disk=True  # HNSW graph on disk for large collections
)
quantization_config = QuantizationConfig(
    scalar=ScalarQuantizationConfig(
        type=ScalarType.INT8,
        quantile=0.99,
        always_ram=True  # Keep quantized vectors in RAM; full-precision on disk
    )
)
```

### 5.4 gRPC Transport for Low Latency

Qdrant's gRPC interface provides binary serialization (Protocol Buffers) vs. JSON over HTTP. For the tutoring path where vector search is called multiple times per session, gRPC reduces per-query overhead by ~2–5ms — meaningful at the 50ms budget.

### 5.5 Self-Hosted with Minimal Footprint

Qdrant is distributed as a single binary (~40MB) or Docker image (~150MB with Alpine base). It has no JVM dependency, no complex cluster manager, and starts in under 2 seconds. A production deployment on a single VPS with 8GB RAM handles millions of vectors comfortably.

### 5.6 Rust Implementation

Qdrant is written in Rust, providing memory safety without garbage collection pauses. This is significant for real-time tutoring latency — Java-based systems (Elasticsearch, early Weaviate) suffer GC pause spikes that violate P99 latency requirements.

### 5.7 Named Vector Support

Qdrant supports multiple named vector fields per point. This allows storing a `content_embedding` and a `metadata_embedding` on the same point — enabling search over either the content or the metadata independently without duplicating points.

```python
# A single knowledge point with two named vectors
client.upsert(
    collection_name="knowledge_state",
    points=[PointStruct(
        id=str(uuid4()),
        vector={
            "content": content_embedding,   # Embedding of the concept explanation
            "context": context_embedding     # Embedding of surrounding session context
        },
        payload={"student_id": 42, "topic": "dynamic_programming", ...}
    )]
)
```

---

## 6. Cons

### 6.1 Additional Infrastructure to Operate

Qdrant is a separate process/service that must be deployed, monitored, and backed up independently. Adding a third database system to the stack (MySQL, MongoDB, Qdrant) increases operational surface area.

**Mitigation**: Qdrant's single-binary deployment model minimizes operational overhead. Docker Compose makes local development straightforward. Qdrant Cloud provides a managed option for teams without DevOps capacity.

### 6.2 No Built-in Authentication (OSS)

Qdrant's open-source version does not provide authentication or TLS by default. The Qdrant Cloud and enterprise versions add API key authentication.

**Mitigation**: In production, Qdrant is deployed behind a private network (VPC). API key authentication is enabled via the `service.api_key` configuration. TLS is terminated at the reverse proxy (Nginx). External access to Qdrant ports (6333, 6334) is firewall-blocked.

### 6.3 No SQL Interface

Developers familiar with SQL must learn Qdrant's JSON filter language for payload queries. There is no SQL wrapper.

**Mitigation**: The `VectorMemoryService` abstraction layer means most developers never interact with Qdrant's filter language directly. Standard operations (search by topic, get student history) are exposed as named Python methods.

### 6.4 Backup Complexity

Qdrant's backup process (snapshots via REST API) is different from MySQL and MongoDB backup approaches. The team must maintain three separate backup strategies.

**Mitigation**: Qdrant's snapshot API (`/collections/{name}/snapshots`) is scriptable. Snapshot files are compressed and stored in the same S3-compatible storage as MySQL and MongoDB backups. The snapshot process is automated via a daily cron job.

```bash
# Daily Qdrant snapshot script
curl -X POST "http://localhost:6333/collections/knowledge_state/snapshots"
# Download and upload to S3
aws s3 cp ./qdrant_snapshots/ s3://mentrax-backups/qdrant/ --recursive
```

### 6.5 Vector Data Interpretation Requires Embedding Model Version Pinning

If the embedding model is changed (e.g., migrating from `text-embedding-3-small` to a future model), all existing vectors become incompatible — they exist in a different vector space. Full re-embedding of all collections would be required.

**Mitigation**: The embedding model is treated as a fixed infrastructure dependency. Model version is stored as metadata on every Qdrant point (`embedding_model: "text-embedding-3-small-v1"`). Any model upgrade requires a formal ADR revision and a migration plan.

---

## 7. Trade-offs

### 7.1 Specialized Store vs. Consolidated Architecture

| Trade-off Axis                          | Qdrant Choice                              | Alternative (pgvector)                    |
|-----------------------------------------|--------------------------------------------|-------------------------------------------|
| Infrastructure components               | 3 stores (MySQL + MongoDB + Qdrant)        | 2 stores (MySQL + PostgreSQL/pgvector)    |
| Vector query performance (p50)          | 5–15ms                                     | 30–100ms                                  |
| Memory efficiency                       | Quantization (4-64x reduction)             | None                                      |
| Developer familiarity                   | New API to learn                           | SQL (familiar)                            |
| Self-hosting cost                       | Low (single Qdrant process)                | Medium (full PostgreSQL instance)         |
| Operational isolation (from LMS writes) | Complete (separate process)                | None (shared PostgreSQL I/O)              |

The trade-off of introducing a third database system is accepted because the performance and capability gap between a purpose-built vector database and a relational-database vector extension is too large to ignore given Mentra X's real-time tutoring latency requirements.

### 7.2 HNSW (ANN) vs. Exact Search

Qdrant's HNSW index performs **approximate** nearest neighbor search — it is possible (with < 3% probability at default settings) for a truly relevant result to be missed. Exact search (`exact: true` in Qdrant) guarantees recall but is O(n) and too slow for real-time use.

This trade-off is accepted: a 97%+ recall rate on semantic similarity search for tutoring context is operationally equivalent to exact search. Students do not perceive the difference between "the 5 most similar past explanations" and "5 of the top 6 most similar past explanations."

---

## 8. Consequences

### 8.1 Agent Access Pattern

All Mastra agents access Qdrant exclusively through `VectorMemoryService`:

```
Mastra Agent → VectorMemoryService → QdrantClient → Qdrant (gRPC/HTTP)
```

No direct qdrant-client calls in agent code. This ensures:
- Consistent payload schemas
- Mandatory student_id filtering
- Centralized latency monitoring
- Swappable vector store backend for testing (mock implementation)

### 8.2 Digital Twin Mutation Protocol

Every twin state mutation follows this protocol:

1. Mastra agent generates new state data (e.g., knowledge state update after session)
2. Agent calls `VectorMemoryService.upsert_knowledge_state(student_id, content, metadata)`
3. `VectorMemoryService` embeds content via OpenAI `text-embedding-3-small`
4. `VectorMemoryService` upserts point to Qdrant with `student_id` payload filter
5. Simultaneously, twin mutation is logged to MongoDB `twin_mutation_audit` collection (ADR-002)
6. Twin mutation summary is written to MySQL `student_twin_states` table (ADR-001) for structured queries

### 8.3 Performance Monitoring Obligations

| Metric                              | Alert Threshold                |
|-------------------------------------|--------------------------------|
| Search latency p50 (per collection) | > 50ms                         |
| Search latency p99 (per collection) | > 150ms                        |
| Upsert latency p99                  | > 500ms                        |
| Collection size (vectors)           | > 10M (trigger capacity review)|
| Disk usage                          | > 75% of allocated storage     |
| HNSW indexing queue depth           | > 10,000 pending               |

---

## 9. Five-Collection Architecture Rationale

### 9.1 Collection Design Philosophy

The five Qdrant collections are not arbitrary — they reflect the **semantic access patterns** of the six Mastra agents. Each collection is purpose-built for a specific query pattern, with payload schemas designed to maximize filter specificity and minimize cross-collection joins.

A single monolithic collection was considered and rejected: merging all twin data into one collection requires compound filters on `student_id` + `data_type`, which reduces HNSW traversal efficiency and makes payload schemas ambiguous.

### 9.2 Collection Specifications

---

#### Collection 1: `knowledge_state`

**Owner**: Weakness Intelligence Agent, Adaptive Content Agent, Doubt Resolution Agent

**Purpose**: Store every concept-level knowledge point for every student — what they understood, misunderstood, or were exposed to.

**Query Pattern**: *"Find the 5 knowledge points most semantically similar to the current question, for student X, where confidence < 0.6"*

**Vector Content**: Embedding of the concept explanation or student response text

**Payload Schema**:
```json
{
  "student_id": 42,
  "topic": "dynamic_programming",
  "subtopic": "memoization",
  "course_id": 7,
  "lesson_id": 103,
  "knowledge_type": "concept | misconception | gap | mastered",
  "confidence_score": 0.45,
  "source": "quiz_attempt | session_response | agent_assessment",
  "source_id": "quiz_attempt_789",
  "embedding_model": "text-embedding-3-small-v1",
  "session_id": "sess_abc123",
  "recorded_at": "2026-06-28T12:34:56Z",
  "is_active": true,
  "revision": 3
}
```

**Index Configuration**: HNSW (m=16, ef_construct=100), Cosine distance, Scalar quantization INT8

**Expected Scale**: 200–1,000 points per student; 2M–10M at platform scale

---

#### Collection 2: `learning_dna`

**Owner**: Adaptive Content Agent, Orchestrator Agent

**Purpose**: Store behavioral embeddings that capture the student's learning style — how they prefer to receive information, their error patterns, engagement signals.

**Query Pattern**: *"What are the 3 most similar past learning style signals to the current session context for student X?"*

**Vector Content**: Embedding of session behavioral summary (pacing, hint-request frequency, error type, time-of-day, response latency patterns)

**Payload Schema**:
```json
{
  "student_id": 42,
  "session_id": "sess_abc123",
  "learning_signals": {
    "modality_preference": "visual | text | code | diagram",
    "pacing": "fast | medium | slow",
    "hint_requests_per_session": 3,
    "avg_response_latency_sec": 12.4,
    "error_correction_pattern": "immediate | delayed | ignored",
    "time_of_day": "morning | afternoon | evening | night",
    "engagement_score": 0.82
  },
  "dna_version": 2,
  "computed_at": "2026-06-28T13:00:00Z",
  "embedding_model": "text-embedding-3-small-v1",
  "is_active": true
}
```

**Index Configuration**: HNSW (m=12, ef_construct=80), Cosine distance

**Expected Scale**: 50–300 points per student (one per significant session); 500K–3M at platform scale

---

#### Collection 3: `explanation_history`

**Owner**: Doubt Resolution Agent

**Purpose**: Store every AI-generated explanation delivered to a student, enabling the Doubt Resolution Agent to retrieve relevant past explanations before generating new ones — ensuring consistency and avoiding contradictions.

**Query Pattern**: *"Find the 3 explanations about recursion that were most positively received by student X in the past 30 days"*

**Vector Content**: Embedding of the explanation text itself

**Payload Schema**:
```json
{
  "student_id": 42,
  "session_id": "sess_abc123",
  "request_id": "req_uuid_789",
  "topic": "recursion",
  "question_text": "What is the base case in recursion?",
  "explanation_text": "The base case is the condition where...",
  "explanation_type": "concept | example | analogy | code",
  "student_rating": 5,
  "student_rating_text": "That made sense!",
  "enkrypt_validation_passed": true,
  "explanation_quality_score": 0.91,
  "model_used": "gpt-4o",
  "delivered_at": "2026-06-28T12:36:00Z",
  "embedding_model": "text-embedding-3-small-v1",
  "is_active": true
}
```

**Index Configuration**: HNSW (m=16, ef_construct=100), Cosine distance, Scalar quantization INT8

**Expected Scale**: 100–2,000 points per student (all explanations); 1M–20M at platform scale (largest collection)

---

#### Collection 4: `session_summaries`

**Owner**: Orchestrator Agent, Weakness Intelligence Agent

**Purpose**: Store end-of-session AI-generated summaries capturing what was covered, what difficulties arose, and what the recommended next actions are.

**Query Pattern**: *"Find the 3 sessions most similar to the current session topic for student X, to inform continuity context"*

**Vector Content**: Embedding of the full session summary narrative

**Payload Schema**:
```json
{
  "student_id": 42,
  "session_id": "sess_abc123",
  "course_id": 7,
  "topics_covered": ["dynamic_programming", "memoization", "tabulation"],
  "primary_weakness_identified": "confuses top-down vs bottom-up DP",
  "session_duration_minutes": 47,
  "agent_interactions": 12,
  "overall_performance": "improving | steady | declining",
  "performance_score": 0.67,
  "recommended_next_topics": ["space_complexity_dp", "DP_on_trees"],
  "twin_mutations_count": 8,
  "session_ended_at": "2026-06-28T13:21:00Z",
  "embedding_model": "text-embedding-3-small-v1",
  "is_active": true
}
```

**Index Configuration**: HNSW (m=12, ef_construct=80), Cosine distance

**Expected Scale**: 30–200 points per student (one per session); 300K–2M at platform scale

---

#### Collection 5: `opportunity_embeddings`

**Owner**: Opportunity Pathfinder Agent

**Purpose**: Store embeddings of career opportunities (jobs, scholarships, competitions, open-source projects) and student career profiles, enabling semantic matching between student profile and opportunities.

**Query Pattern**: *"Find the 10 opportunities most semantically aligned with student X's current skill profile and career aspirations"*

**Vector Content**: Embedding of opportunity description text OR student career profile summary

**Payload Schema (Opportunity documents)**:
```json
{
  "document_type": "opportunity",
  "opportunity_id": "opp_uuid_001",
  "title": "Junior ML Engineer",
  "organization": "TechCorp",
  "opportunity_type": "job | scholarship | competition | internship | open_source",
  "required_skills": ["Python", "PyTorch", "Data Analysis"],
  "min_experience_years": 0,
  "application_deadline": "2026-09-01",
  "location": "Remote",
  "relevance_tags": ["machine_learning", "nlp", "computer_vision"],
  "embedding_model": "text-embedding-3-small-v1",
  "indexed_at": "2026-06-28T00:00:00Z",
  "is_active": true,
  "student_id": null
}
```

**Payload Schema (Student career profile documents)**:
```json
{
  "document_type": "student_profile",
  "student_id": 42,
  "career_aspirations": "AI engineer focused on NLP systems",
  "top_skills": ["Python", "Flask", "NLP basics"],
  "skill_gap_areas": ["PyTorch", "cloud deployment"],
  "project_highlights": ["Built a sentiment analysis CLI tool"],
  "opportunity_type_preference": ["internship", "open_source"],
  "location_preference": "Remote or Bangalore",
  "embedding_model": "text-embedding-3-small-v1",
  "profile_version": 5,
  "updated_at": "2026-06-28T14:00:00Z",
  "student_id": 42
}
```

**Filtering Logic**: When student profile is the query vector, filter `document_type == "opportunity"`. When text query is used for exploration, filter by `opportunity_type`, `location`, `required_skills` overlap.

**Index Configuration**: HNSW (m=16, ef_construct=100), Cosine distance

**Expected Scale**: 10,000–100,000 opportunity documents (platform-wide); 1 student profile per student

---

### 9.3 Collection Size Summary

| Collection               | Points per Student | Points per 10K Users | Total @ 10K Users |
|--------------------------|--------------------|----------------------|-------------------|
| `knowledge_state`        | 500–1,000          | 5M–10M               | 5M–10M            |
| `learning_dna`           | 50–300             | 500K–3M              | 500K–3M           |
| `explanation_history`    | 500–2,000          | 5M–20M               | 5M–20M            |
| `session_summaries`      | 30–200             | 300K–2M              | 300K–2M           |
| `opportunity_embeddings` | 1 profile          | 10K profiles + 50K opportunities | ~60K–150K |

---

## 10. Implementation Notes

### 10.1 Collection Initialization

```python
# services/vector_memory/setup.py

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    VectorParams, Distance, HnswConfigDiff,
    QuantizationConfig, ScalarQuantizationConfig, ScalarType,
    PayloadSchemaType
)

COLLECTIONS = {
    "knowledge_state": {"size": 1536, "m": 16, "ef_construct": 100},
    "learning_dna": {"size": 1536, "m": 12, "ef_construct": 80},
    "explanation_history": {"size": 1536, "m": 16, "ef_construct": 100},
    "session_summaries": {"size": 1536, "m": 12, "ef_construct": 80},
    "opportunity_embeddings": {"size": 1536, "m": 16, "ef_construct": 100},
}

def initialize_collections(client: QdrantClient):
    for name, config in COLLECTIONS.items():
        if not client.collection_exists(name):
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=config["size"],
                    distance=Distance.COSINE,
                    on_disk=False,  # HNSW in RAM for low latency
                ),
                hnsw_config=HnswConfigDiff(
                    m=config["m"],
                    ef_construct=config["ef_construct"],
                    full_scan_threshold=10000,
                    max_indexing_threads=0,  # Auto
                    on_disk=False
                ),
                quantization_config=QuantizationConfig(
                    scalar=ScalarQuantizationConfig(
                        type=ScalarType.INT8,
                        quantile=0.99,
                        always_ram=True
                    )
                )
            )
            # Create payload indexes for filter performance
            client.create_payload_index(name, "student_id", PayloadSchemaType.INTEGER)
            client.create_payload_index(name, "is_active", PayloadSchemaType.BOOL)
            client.create_payload_index(name, "topic", PayloadSchemaType.KEYWORD)
```

### 10.2 VectorMemoryService Core Interface

```python
# services/vector_memory/service.py

from uuid import uuid4
from typing import Optional
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, PointStruct

class VectorMemoryService:
    
    def __init__(self, client: QdrantClient, embedder):
        self._client = client
        self._embedder = embedder  # OpenAI embedding wrapper
    
    def search_knowledge_state(
        self,
        student_id: int,
        query_text: str,
        top_k: int = 5,
        confidence_threshold: Optional[float] = None
    ) -> list[dict]:
        query_vector = self._embedder.embed(query_text)
        
        must_conditions = [
            FieldCondition(key="student_id", match=MatchValue(value=student_id)),
            FieldCondition(key="is_active", match=MatchValue(value=True)),
        ]
        if confidence_threshold:
            from qdrant_client.http.models import Range
            must_conditions.append(
                FieldCondition(key="confidence_score", range=Range(lt=confidence_threshold))
            )
        
        results = self._client.search(
            collection_name="knowledge_state",
            query_vector=query_vector,
            query_filter=Filter(must=must_conditions),
            limit=top_k,
            with_payload=True
        )
        return [{"score": r.score, **r.payload} for r in results]
    
    def upsert_knowledge_point(
        self,
        student_id: int,
        content_text: str,
        metadata: dict
    ) -> str:
        point_id = str(uuid4())
        vector = self._embedder.embed(content_text)
        
        self._client.upsert(
            collection_name="knowledge_state",
            points=[PointStruct(
                id=point_id,
                vector=vector,
                payload={"student_id": student_id, "is_active": True, **metadata}
            )]
        )
        return point_id
```

---

## 11. Future Revisions

| Trigger Condition                                            | Recommended Action                                                        |
|--------------------------------------------------------------|---------------------------------------------------------------------------|
| Embedding model change (new OpenAI model)                    | Full re-embedding required; planned maintenance window; ADR revision      |
| Collection exceeds 20M vectors                               | Enable on-disk HNSW; add Qdrant cluster nodes                            |
| Real-time latency p99 exceeds 150ms                          | Enable product quantization; review HNSW m and ef parameters             |
| Hybrid search needed (keyword + semantic)                    | Enable Qdrant sparse vectors + BM25 for hybrid retrieval                  |
| Multi-modal embeddings (image, audio)                        | Add named vector fields per modality; re-evaluate embedding model choice  |
| Team adopts PostgreSQL (ADR-001 revision)                    | Re-evaluate pgvector as a consolidation option                            |
| Qdrant Cloud cost exceeds self-hosted at scale               | Migrate to self-hosted replica set on dedicated instances                 |
| Real-time collaborative learning features                    | Evaluate Qdrant's distributed cluster mode for horizontal scaling         |

---

## 12. References

- [Qdrant — Official Documentation](https://qdrant.tech/documentation/)
- [Qdrant — HNSW Configuration Guide](https://qdrant.tech/documentation/concepts/indexing/#hnsw-index)
- [Qdrant — Scalar Quantization](https://qdrant.tech/documentation/guides/quantization/)
- [Qdrant — Payload Filters](https://qdrant.tech/documentation/concepts/filtering/)
- [Qdrant — Named Vectors](https://qdrant.tech/documentation/concepts/collections/#collection-with-multiple-vectors)
- [OpenAI — text-embedding-3-small](https://platform.openai.com/docs/guides/embeddings)
- [HNSW Paper — Malkov & Yashunin (2018)](https://arxiv.org/abs/1603.09320)
- [Mentra X — ADR-001: MySQL as Primary Relational Database](./ADR-001-MySQL.md)
- [Mentra X — ADR-004: Mastra as Multi-Agent Orchestration Framework](./ADR-004-Mastra.md)
- [Mentra X — Student Digital Twin Specification](../Architecture/digital-twin-spec.md)

---

*This document is part of the Mentra X Architecture Decision Record series. All ADRs are stored in `D:\AI-Student Platform\Docs\ADR\` and version-controlled alongside the codebase.*
