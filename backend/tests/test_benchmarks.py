import pytest
from backend.models import db
from backend.services.evaluation.benchmark_runner import BenchmarkRunner, BenchmarkCase

@pytest.fixture
def app():
    from backend.app import app as flask_app
    flask_app.config['TESTING'] = True
    with flask_app.app_context():
        db.create_all()
        try:
            from backend.models import ensure_privacy_schema
            ensure_privacy_schema(db.session)
        except Exception:
            pass
        yield flask_app

def test_benchmark_suite_execution(app):
    with app.app_context():
        cases = [
            BenchmarkCase(
                case_id="math-basic-01",
                prompt="Explain linear equations and provide an example.",
                expected_context={"retrieved_memories": [{"content": "Linear equations form y = mx + b"}]}
            ),
            BenchmarkCase(
                case_id="code-basic-02",
                prompt="Write a Python function to compute Fibonacci numbers.",
                expected_context={"twin_state": {"learning_style": "practical"}}
            )
        ]
        
        providers = ["MockProvider", "MastraProvider", "OpenRouterProvider"]
        result = BenchmarkRunner.run_suite(cases, providers=providers)
        
        assert result["total_evaluations"] == len(cases) * len(providers)
        assert len(result["comparison_summary"]) == 3
        
        for prov in providers:
            assert prov in result["comparison_summary"]
            summary = result["comparison_summary"][prov]
            assert summary["average_quality_score"] > 0.0
            assert summary["average_latency_ms"] > 0.0
            assert summary["total_tokens"] > 0
            assert summary["total_cost_usd"] > 0.0
            
        # Verify OpenRouter simulated latency > MockProvider simulated latency
        mock_lat = result["comparison_summary"]["MockProvider"]["average_latency_ms"]
        open_lat = result["comparison_summary"]["OpenRouterProvider"]["average_latency_ms"]
        assert open_lat > mock_lat
