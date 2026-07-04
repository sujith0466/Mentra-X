from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

@dataclass
class SwarmStatusMetrics:
    active_workflows: int = 0
    running_agents: int = 0
    waiting_workflows: int = 0
    failed_workflows: int = 0
    retrying_workflows: int = 0
    avg_latency_ms: float = 0.0
    event_throughput_min: float = 0.0
    queue_depth: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class RuntimeHealthMetrics:
    workflow_store_status: str = "HEALTHY"
    event_bus_status: str = "HEALTHY"
    runtime_status: str = "HEALTHY"
    prompt_repo_status: str = "HEALTHY"
    memory_status: str = "HEALTHY"
    qdrant_status: str = "HEALTHY"
    database_status: str = "HEALTHY"
    overall_status: str = "HEALTHY"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AIQualityMetrics:
    faithfulness: float = 0.0
    hallucination: float = 1.0  # 1.0 means no hallucination
    relevance: float = 0.0
    quality: float = 0.0
    safety: float = 1.0
    confidence: float = 0.0
    trend_data: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class PromptAnalyticsMetrics:
    active_version: str = "1.0.0"
    total_versions: int = 1
    approval_status: str = "APPROVED"
    rollback_available: bool = False
    avg_latency_ms: float = 0.0
    total_tokens: int = 0
    avg_cost_usd: float = 0.0
    success_rate: float = 1.0
    last_deployed_at: Optional[str] = None
    prompts: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ProviderMetrics:
    providers: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "Mastra": {"requests": 0, "errors": 0, "tokens": 0, "cost": 0.0, "latency": 0.0, "success_rate": 100.0},
        "OpenRouter": {"requests": 0, "errors": 0, "tokens": 0, "cost": 0.0, "latency": 0.0, "success_rate": 100.0},
        "MockProvider": {"requests": 0, "errors": 0, "tokens": 0, "cost": 0.0, "latency": 0.0, "success_rate": 100.0}
    })

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class StudentIntelligenceMetrics:
    avg_confidence: float = 0.0
    twin_completeness: float = 0.0
    assessment_completion_rate: float = 0.0
    memory_growth_count: int = 0
    weak_concept_distribution: Dict[str, int] = field(default_factory=dict)
    learning_progression_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ExplainabilityMetrics:
    total_explanations: int = 0
    avg_confidence: float = 0.0
    citation_sources: Dict[str, int] = field(default_factory=dict)
    counterfactual_count: int = 0
    recent_workflows: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class PrivacyMetrics:
    active_consents: int = 0
    revoked_consents: int = 0
    export_requests: int = 0
    erasure_requests: int = 0
    audit_chain_integrity: str = "VERIFIED"
    retention_jobs_run: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ObservabilityMetrics:
    trace_count: int = 0
    span_count: int = 0
    error_rate: float = 0.0
    req_latency_ms: float = 0.0
    tool_latency_ms: float = 0.0
    agent_latency_ms: float = 0.0
    db_latency_ms: float = 0.0
    vector_latency_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class OverviewMetrics:
    swarm: SwarmStatusMetrics = field(default_factory=SwarmStatusMetrics)
    runtime: RuntimeHealthMetrics = field(default_factory=RuntimeHealthMetrics)
    quality: AIQualityMetrics = field(default_factory=AIQualityMetrics)
    providers: ProviderMetrics = field(default_factory=ProviderMetrics)
    prompts: PromptAnalyticsMetrics = field(default_factory=PromptAnalyticsMetrics)
    privacy: PrivacyMetrics = field(default_factory=PrivacyMetrics)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "swarm": self.swarm.to_dict(),
            "runtime": self.runtime.to_dict(),
            "quality": self.quality.to_dict(),
            "providers": self.providers.to_dict(),
            "prompts": self.prompts.to_dict(),
            "privacy": self.privacy.to_dict(),
            "timestamp": self.timestamp
        }
