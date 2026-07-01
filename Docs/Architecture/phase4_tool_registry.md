# Phase 4 Mastra Tool Registry

The following tools will be registered with Mastra. This Registry acts as the Single Source of Truth for Swarm tools.

## 1. get_digital_twin
- **Purpose**: Fetch the holistic profile of the student (skills, progression, intent).
- **Version**: 1.0.0
- **Owner**: TwinServiceTeam
- **Permissions**: `twin:read`
- **Read / Write**: Read
- **Mutable / Immutable**: Immutable
- **Cacheable**: Yes (TTL: 60s)
- **Supports Streaming**: No
- **Supports Parallel Execution**: Yes
- **Deterministic**: Yes
- **Needs Verification**: No
- **Produces Events**: None
- **Consumes Events**: None
- **Input Schema**: `{ "user_id": "int" }`
- **Output Schema**: `StudentTwinDTO` (JSON)
- **Facade Used**: `TwinFacade.get_twin(user_id)`
- **Underlying Service**: `TwinBuilder`
- **Failure Behaviour**: Fallback to base empty twin schema.
- **Retry Policy**: 1 retry (Exponential backoff)
- **Timeout**: 1500ms
- **Expected Latency**: 20ms
- **Estimated Cost**: 0 (Local execution)
- **Audit Required**: No

## 2. retrieve_semantic_memory
- **Purpose**: Fetch contextual Qdrant logs (doubts, concepts, DNA).
- **Version**: 1.1.0
- **Owner**: MemoryServiceTeam
- **Permissions**: `memory:read`
- **Read / Write**: Read
- **Mutable / Immutable**: Immutable
- **Cacheable**: Yes (TTL: 120s)
- **Supports Streaming**: No
- **Supports Parallel Execution**: Yes
- **Deterministic**: Yes
- **Needs Verification**: No
- **Produces Events**: None
- **Consumes Events**: None
- **Input Schema**: `{ "user_id": "int", "query": "str", "collection": "str", "limit": "int" }`
- **Output Schema**: `List[MemoryPointDTO]`
- **Facade Used**: `MemoryFacade.retrieve_context(collection, query, user_id, limit)`
- **Underlying Service**: `MemoryRetriever`
- **Failure Behaviour**: Return empty context list `[]`. Do not crash agent.
- **Retry Policy**: 2 retries (with exponential backoff)
- **Timeout**: 3000ms
- **Expected Latency**: 80ms
- **Estimated Cost**: ~0.0001 (Embedding cost)
- **Audit Required**: No

## 3. mutate_digital_twin (via Event Bus)
- **Purpose**: Safely adjust continuous attributes (e.g. `frustration_index`, `engagement_score`).
- **Version**: 1.0.0
- **Owner**: TwinServiceTeam
- **Permissions**: `twin:write`
- **Read / Write**: Write
- **Mutable / Immutable**: Mutable
- **Cacheable**: No
- **Supports Streaming**: No
- **Supports Parallel Execution**: No (Sequential per user to prevent race conditions)
- **Deterministic**: Yes
- **Needs Verification**: Yes
- **Produces Events**: `TwinUpdated`
- **Consumes Events**: None
- **Input Schema**: `{ "user_id": "int", "deltas": { "metric": "float" } }`
- **Output Schema**: `{ "success": "bool", "event_id": "str" }`
- **Facade Used**: Target of `TwinUpdated` Event
- **Underlying Service**: `TwinMutator`
- **Failure Behaviour**: Log failure, abort mutation, return `success: false`.
- **Retry Policy**: 0 retries (idempotency handled downstream)
- **Timeout**: 2000ms
- **Expected Latency**: 45ms
- **Estimated Cost**: 0 (Local execution)
- **Audit Required**: Yes

## 4. store_semantic_memory (via Event Bus)
- **Purpose**: Write newly learned concepts or recurring doubts to Qdrant.
- **Version**: 1.0.0
- **Owner**: MemoryServiceTeam
- **Permissions**: `memory:write`
- **Read / Write**: Write
- **Mutable / Immutable**: Mutable
- **Cacheable**: No
- **Supports Streaming**: No
- **Supports Parallel Execution**: Yes
- **Deterministic**: Yes
- **Needs Verification**: Yes
- **Produces Events**: `MemoryStored`
- **Consumes Events**: None
- **Input Schema**: `{ "user_id": "int", "type": "enum(doubt, concept, dna)", "text": "str" }`
- **Output Schema**: `{ "success": "bool", "event_id": "str" }`
- **Facade Used**: Target of `MemoryStored` Event
- **Underlying Service**: `MemoryMutator`
- **Failure Behaviour**: Enqueue for async retry (max 3). Return `success: true (deferred)`.
- **Retry Policy**: 3 retries (Background async queue)
- **Timeout**: 5000ms
- **Expected Latency**: 60ms
- **Estimated Cost**: ~0.0001 (Embedding cost)
- **Audit Required**: Yes

## 5. start_assessment_session
- **Purpose**: Spin up a Bayesian tracking session when the agent realizes the student needs testing.
- **Version**: 1.0.0
- **Owner**: AssessmentServiceTeam
- **Permissions**: `assessment:write`
- **Read / Write**: Write
- **Mutable / Immutable**: Mutable
- **Cacheable**: No
- **Supports Streaming**: No
- **Supports Parallel Execution**: No
- **Deterministic**: Yes
- **Needs Verification**: No
- **Produces Events**: `AssessmentStarted`
- **Consumes Events**: None
- **Input Schema**: `{ "user_id": "int", "track": "str" }`
- **Output Schema**: `AssessmentSessionDTO`
- **Facade Used**: `AssessmentFacade.start(user_id, track)`
- **Underlying Service**: `AssessmentPipeline`
- **Failure Behaviour**: Abort and prompt user to refresh.
- **Retry Policy**: 0 retries
- **Timeout**: 3000ms
- **Expected Latency**: 35ms
- **Estimated Cost**: 0 (Local execution)
- **Audit Required**: Yes
