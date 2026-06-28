# Mentra X — Feature Flag System

**Version:** 1.0  
**Owner:** Sujith Kumar AI  
**Location:** `backend/feature_flags.py`

---

## Overview

Mentra X uses a centralized feature flag system to control which AI capabilities are active at runtime. This enables:

- **Incremental rollout** — activate Phase N features without redeploying
- **Safe degradation** — disable a broken AI layer while the LMS continues working
- **A/B testing** — enable features for a subset of users
- **Demo control** — enable all features for judge demo; disable for maintenance
- **Environment isolation** — different flags for dev, staging, production

---

## Flag Definitions

### Core AI Flags

| Flag | Type | Default | Phase | Description |
|---|---|---|---|---|
| `ENABLE_DIGITAL_TWIN` | bool | `false` | Phase 1 | Activates StudentTwin model, twin routes, health score computation |
| `ENABLE_ASSESSMENT_ENGINE` | bool | `false` | Phase 2 | Activates adaptive assessment flow and diagnostic quiz |
| `ENABLE_QDRANT` | bool | `false` | Phase 3 | Activates Qdrant vector memory; falls back to MySQL JSON if disabled |
| `ENABLE_MASTRA` | bool | `false` | Phase 4 | Activates full Mastra agent swarm; falls back to simple chatbot if disabled |
| `ENABLE_ADAPTIVE_TEACHING` | bool | `false` | Phase 5 | Activates TutorDecisionEngine; uses static level 2 if disabled |
| `ENABLE_ENKRYPT` | bool | `false` | Phase 6 | Activates Enkrypt validation; all responses pass through if disabled |
| `ENABLE_CONTINUOUS_LEARNING` | bool | `false` | Phase 7 | Activates decay engine and background scheduler |
| `ENABLE_WEAKNESS_INTELLIGENCE` | bool | `false` | Phase 8 | Activates weakness cron and cluster analysis |
| `ENABLE_OPPORTUNITY_ENGINE` | bool | `false` | Phase 8 | Activates opportunity matching and opportunity feed |
| `ENABLE_ANALYTICS` | bool | `false` | Phase 8 | Activates insight engine and weekly reports |

### Experience Flags

| Flag | Type | Default | Phase | Description |
|---|---|---|---|---|
| `ENABLE_DEVELOPER_PANEL` | bool | `false` | Phase 9 | Activates agent trace panel and observability UI |
| `ENABLE_TWIN_DASHBOARD` | bool | `false` | Phase 9 | Activates Digital Twin visualization pages |
| `ENABLE_KNOWLEDGE_MAP` | bool | `false` | Phase 9 | Activates concept mastery heatmap |
| `ENABLE_REVISION_CALENDAR` | bool | `false` | Phase 9 | Activates spaced repetition calendar UI |
| `ENABLE_OPPORTUNITY_FEED` | bool | `false` | Phase 9 | Activates opportunity feed UI |

### Infrastructure Flags

| Flag | Type | Default | Description |
|---|---|---|---|
| `ENABLE_REDIS_CACHE` | bool | `false` | Activates Redis hot-twin cache; Qdrant direct if disabled |
| `ENABLE_OBSERVABILITY` | bool | `false` | Activates structured agent execution logging |
| `ENABLE_RATE_LIMITING` | bool | `true` | Activates API rate limiting (always on in production) |
| `ENABLE_SCHEDULER` | bool | `false` | Activates APScheduler background jobs |
| `ENABLE_MONGODB_AUDIT` | bool | `true` | Activates MongoDB audit logging; graceful fallback if disabled |

---

## Implementation

### `backend/feature_flags.py`

```python
import os
from dataclasses import dataclass, field
from functools import lru_cache


@dataclass(frozen=True)
class FeatureFlags:
    """
    Central feature flag registry for Mentra X.
    All flags are read from environment variables at startup.
    Immutable after initialization (frozen=True).
    """

    # Phase 1: Digital Twin
    ENABLE_DIGITAL_TWIN: bool = field(
        default_factory=lambda: _bool_env("ENABLE_DIGITAL_TWIN", False)
    )

    # Phase 2: Assessment
    ENABLE_ASSESSMENT_ENGINE: bool = field(
        default_factory=lambda: _bool_env("ENABLE_ASSESSMENT_ENGINE", False)
    )

    # Phase 3: Qdrant Memory
    ENABLE_QDRANT: bool = field(
        default_factory=lambda: _bool_env("ENABLE_QDRANT", False)
    )

    # Phase 4: Mastra
    ENABLE_MASTRA: bool = field(
        default_factory=lambda: _bool_env("ENABLE_MASTRA", False)
    )

    # Phase 5: Adaptive Intelligence
    ENABLE_ADAPTIVE_TEACHING: bool = field(
        default_factory=lambda: _bool_env("ENABLE_ADAPTIVE_TEACHING", False)
    )

    # Phase 6: Enkrypt
    ENABLE_ENKRYPT: bool = field(
        default_factory=lambda: _bool_env("ENABLE_ENKRYPT", False)
    )

    # Phase 7: Continuous Learning
    ENABLE_CONTINUOUS_LEARNING: bool = field(
        default_factory=lambda: _bool_env("ENABLE_CONTINUOUS_LEARNING", False)
    )

    # Phase 8: Intelligence Layer
    ENABLE_WEAKNESS_INTELLIGENCE: bool = field(
        default_factory=lambda: _bool_env("ENABLE_WEAKNESS_INTELLIGENCE", False)
    )
    ENABLE_OPPORTUNITY_ENGINE: bool = field(
        default_factory=lambda: _bool_env("ENABLE_OPPORTUNITY_ENGINE", False)
    )
    ENABLE_ANALYTICS: bool = field(
        default_factory=lambda: _bool_env("ENABLE_ANALYTICS", False)
    )

    # Phase 9: Experience
    ENABLE_DEVELOPER_PANEL: bool = field(
        default_factory=lambda: _bool_env("ENABLE_DEVELOPER_PANEL", False)
    )
    ENABLE_TWIN_DASHBOARD: bool = field(
        default_factory=lambda: _bool_env("ENABLE_TWIN_DASHBOARD", False)
    )
    ENABLE_KNOWLEDGE_MAP: bool = field(
        default_factory=lambda: _bool_env("ENABLE_KNOWLEDGE_MAP", False)
    )

    # Infrastructure
    ENABLE_REDIS_CACHE: bool = field(
        default_factory=lambda: _bool_env("ENABLE_REDIS_CACHE", False)
    )
    ENABLE_OBSERVABILITY: bool = field(
        default_factory=lambda: _bool_env("ENABLE_OBSERVABILITY", False)
    )
    ENABLE_RATE_LIMITING: bool = field(
        default_factory=lambda: _bool_env("ENABLE_RATE_LIMITING", True)
    )
    ENABLE_SCHEDULER: bool = field(
        default_factory=lambda: _bool_env("ENABLE_SCHEDULER", False)
    )
    ENABLE_MONGODB_AUDIT: bool = field(
        default_factory=lambda: _bool_env("ENABLE_MONGODB_AUDIT", True)
    )


def _bool_env(key: str, default: bool) -> bool:
    val = os.getenv(key, str(default)).strip().lower()
    return val in ("true", "1", "yes", "on")


@lru_cache(maxsize=1)
def get_flags() -> FeatureFlags:
    """Returns the singleton FeatureFlags instance. Cached after first call."""
    return FeatureFlags()
```

### Usage in Routes

```python
from backend.feature_flags import get_flags

@twin_bp.route('/api/v1/twin/profile')
def twin_profile():
    flags = get_flags()
    if not flags.ENABLE_DIGITAL_TWIN:
        return jsonify({
            "success": False,
            "error": {
                "code": "TWIN_010",
                "message": "Digital Twin feature is not yet enabled.",
                "recovery": "Contact the administrator or set ENABLE_DIGITAL_TWIN=true."
            }
        }), 503
    ...
```

### Usage in Services

```python
from backend.feature_flags import get_flags

class MemoryService:
    def get_learning_dna(self, user_id: str) -> LearningDNA:
        flags = get_flags()

        if not flags.ENABLE_QDRANT:
            # Graceful fallback: read from MySQL twin JSON
            return self._get_dna_from_mysql(user_id)

        if flags.ENABLE_REDIS_CACHE:
            cached = self.redis.get(f"dna:{user_id}")
            if cached:
                return LearningDNA.from_json(cached)

        return self._get_dna_from_qdrant(user_id)
```

---

## Environment Variables

Add to `.env`:

```env
# Phase 1 — Digital Twin
ENABLE_DIGITAL_TWIN=false

# Phase 2 — Assessment Engine
ENABLE_ASSESSMENT_ENGINE=false

# Phase 3 — Qdrant Memory
ENABLE_QDRANT=false

# Phase 4 — Mastra Swarm
ENABLE_MASTRA=false

# Phase 5 — Adaptive Intelligence
ENABLE_ADAPTIVE_TEACHING=false

# Phase 6 — Enkrypt Safety
ENABLE_ENKRYPT=false

# Phase 7 — Continuous Learning
ENABLE_CONTINUOUS_LEARNING=false
ENABLE_SCHEDULER=false

# Phase 8 — Intelligence
ENABLE_WEAKNESS_INTELLIGENCE=false
ENABLE_OPPORTUNITY_ENGINE=false
ENABLE_ANALYTICS=false

# Phase 9 — Experience
ENABLE_DEVELOPER_PANEL=false
ENABLE_TWIN_DASHBOARD=false
ENABLE_KNOWLEDGE_MAP=false

# Infrastructure
ENABLE_REDIS_CACHE=false
ENABLE_OBSERVABILITY=false
ENABLE_RATE_LIMITING=true
ENABLE_MONGODB_AUDIT=true
```

---

## Rollout Strategy

### Development

Enable flags one at a time as each phase is completed:

```env
ENABLE_DIGITAL_TWIN=true          # After Phase 1 complete
ENABLE_ASSESSMENT_ENGINE=true     # After Phase 2 complete
ENABLE_QDRANT=true               # After Phase 3 complete
...
```

### Demo Environment

Enable all flags for judge demo:

```env
# Demo .env — all AI features enabled
ENABLE_DIGITAL_TWIN=true
ENABLE_ASSESSMENT_ENGINE=true
ENABLE_QDRANT=true
ENABLE_MASTRA=true
ENABLE_ADAPTIVE_TEACHING=true
ENABLE_ENKRYPT=true
ENABLE_CONTINUOUS_LEARNING=true
ENABLE_WEAKNESS_INTELLIGENCE=true
ENABLE_OPPORTUNITY_ENGINE=true
ENABLE_ANALYTICS=true
ENABLE_DEVELOPER_PANEL=true
ENABLE_TWIN_DASHBOARD=true
ENABLE_KNOWLEDGE_MAP=true
ENABLE_REDIS_CACHE=true
ENABLE_OBSERVABILITY=true
ENABLE_SCHEDULER=true
```

### Production Rollout

Feature flags allow **canary releases**:
1. Enable flag for 5% of users (by user_id modulo)
2. Monitor error rates and latency
3. Expand to 25% → 50% → 100%

```python
def is_feature_enabled_for_user(flag_name: str, user_id: int) -> bool:
    """Canary rollout: enable feature for % of users."""
    flags = get_flags()
    base_enabled = getattr(flags, flag_name, False)
    if not base_enabled:
        return False

    # Read canary percentage from env (e.g., ENABLE_QDRANT_CANARY_PCT=25)
    canary_pct = int(os.getenv(f"{flag_name}_CANARY_PCT", "100"))
    return (user_id % 100) < canary_pct
```

---

## Fallback Behaviour

Every feature flag has a defined fallback:

| Flag | When Disabled Fallback |
|---|---|
| `ENABLE_DIGITAL_TWIN` | 503 response on `/api/v1/twin/*` endpoints |
| `ENABLE_QDRANT` | Read/write from MySQL `student_twins.learning_dna` JSON |
| `ENABLE_MASTRA` | Route to legacy `ai_routes.py` chatbot |
| `ENABLE_ENKRYPT` | Responses pass through unvalidated (warn in logs) |
| `ENABLE_ADAPTIVE_TEACHING` | Default to teaching level 2 for all students |
| `ENABLE_REDIS_CACHE` | Read directly from Qdrant on every request |
| `ENABLE_SCHEDULER` | Background jobs don't run (decay, sync disabled) |
| `ENABLE_MONGODB_AUDIT` | Audit logs written to application log file only |

---

## Adding a New Feature Flag

1. Add to `FeatureFlags` dataclass in `backend/feature_flags.py`
2. Add to `.env` with default value `false`
3. Add to `.env.example` with documentation comment
4. Add to the flag table in this document
5. Implement fallback behaviour in the relevant service/route
6. Add to the rollout strategy section
