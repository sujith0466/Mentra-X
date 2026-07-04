import pytest
from backend.models import db
from backend.services.dashboard import (
    SwarmStatusMetrics,
    RuntimeHealthMetrics,
    AIQualityMetrics,
    PromptAnalyticsMetrics,
    ProviderMetrics,
    StudentIntelligenceMetrics,
    ExplainabilityMetrics,
    PrivacyMetrics,
    ObservabilityMetrics,
    OverviewMetrics,
    DashboardAggregator,
    DashboardService
)

@pytest.fixture
def app():
    from backend.app import app as flask_app
    flask_app.config['TESTING'] = True
    with flask_app.app_context():
        db.create_all()
        yield flask_app

def test_dashboard_dtos():
    """Test instantiation and serialization of all structured Dashboard DTO schemas."""
    swarm = SwarmStatusMetrics(active_workflows=2, running_agents=6)
    assert swarm.to_dict()["active_workflows"] == 2
    
    runtime = RuntimeHealthMetrics(overall_status="HEALTHY")
    assert runtime.to_dict()["overall_status"] == "HEALTHY"
    
    qual = AIQualityMetrics(faithfulness=0.95)
    assert qual.to_dict()["faithfulness"] == 0.95
    
    prompt = PromptAnalyticsMetrics(active_version="2.0.0")
    assert prompt.to_dict()["active_version"] == "2.0.0"
    
    provider = ProviderMetrics()
    assert "Mastra" in provider.to_dict()["providers"]
    
    intel = StudentIntelligenceMetrics(avg_confidence=0.88)
    assert intel.to_dict()["avg_confidence"] == 0.88
    
    expl = ExplainabilityMetrics(total_explanations=10)
    assert expl.to_dict()["total_explanations"] == 10
    
    priv = PrivacyMetrics(active_consents=5)
    assert priv.to_dict()["active_consents"] == 5
    
    obs = ObservabilityMetrics(trace_count=100)
    assert obs.to_dict()["trace_count"] == 100
    
    over = OverviewMetrics(swarm=swarm, runtime=runtime)
    d = over.to_dict()
    assert d["swarm"]["active_workflows"] == 2
    assert d["runtime"]["overall_status"] == "HEALTHY"
    assert "timestamp" in d

def test_dashboard_aggregator(app):
    """Test DashboardAggregator pulling telemetry via Facades without direct DB queries."""
    over = DashboardAggregator.get_overview()
    assert isinstance(over, OverviewMetrics)
    assert over.swarm.avg_latency_ms > 0
    assert over.runtime.overall_status in ["HEALTHY", "DEGRADED", "CRITICAL"]
    assert over.quality.hallucination >= 0.0
    assert over.providers.providers["Mastra"]["success_rate"] > 0
    assert over.prompts.total_versions >= 1
    assert over.privacy.audit_chain_integrity == "VERIFIED"

def test_dashboard_service_facade(app):
    """Test DashboardService API methods returning JSON-serializable dictionaries."""
    overview_data = DashboardService.get_overview_data()
    assert isinstance(overview_data, dict)
    assert "swarm" in overview_data
    assert "quality" in overview_data
    
    runtime_data = DashboardService.get_runtime_data()
    assert "overall_status" in runtime_data
    
    providers_data = DashboardService.get_providers_data()
    assert "providers" in providers_data
    
    prompts_data = DashboardService.get_prompts_data()
    assert "active_version" in prompts_data
    
    eval_data = DashboardService.get_evaluation_data()
    assert "quality" in eval_data
    assert "explainability" in eval_data
    
    priv_data = DashboardService.get_privacy_data()
    assert "active_consents" in priv_data
    
    obs_data = DashboardService.get_observability_data()
    assert "trace_count" in obs_data
    
    swarm_data = DashboardService.get_swarm_data()
    assert "active_workflows" in swarm_data
    
    intel_data = DashboardService.get_student_intelligence_data()
    assert "avg_confidence" in intel_data
