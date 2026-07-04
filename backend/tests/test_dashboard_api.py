import pytest
from backend.models import db

@pytest.fixture
def client():
    from backend.app import app as flask_app
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        with flask_app.app_context():
            db.create_all()
            yield client

def test_dashboard_api_endpoints(client):
    """Test all 9 authenticated admin API endpoints for the Enterprise AI Operations Dashboard."""
    endpoints = [
        '/api/v1/dashboard/overview',
        '/api/v1/dashboard/runtime',
        '/api/v1/dashboard/providers',
        '/api/v1/dashboard/prompts',
        '/api/v1/dashboard/evaluation',
        '/api/v1/dashboard/privacy',
        '/api/v1/dashboard/observability',
        '/api/v1/dashboard/swarm',
        '/api/v1/dashboard/student_intelligence'
    ]
    
    for ep in endpoints:
        resp = client.get(ep)
        assert resp.status_code == 200, f"Endpoint {ep} failed with status {resp.status_code}"
        json_data = resp.get_json()
        assert json_data is not None, f"Endpoint {ep} returned None json"
        assert json_data.get('status') == 'success', f"Endpoint {ep} returned non-success status: {json_data.get('status')}"
        assert 'data' in json_data, f"Endpoint {ep} missing data field"

def test_dashboard_overview_structure(client):
    """Test specific structure of the overview endpoint payload."""
    resp = client.get('/api/v1/dashboard/overview')
    assert resp.status_code == 200
    data = resp.get_json()['data']
    assert 'swarm' in data
    assert 'runtime' in data
    assert 'quality' in data
    assert 'providers' in data
    assert 'prompts' in data
    assert 'privacy' in data

def test_dashboard_auth_protection():
    """Test that dashboard API endpoints enforce authentication when not in testing mode."""
    from backend.app import app as flask_app
    flask_app.config['TESTING'] = False
    with flask_app.test_client() as c:
        resp = c.get('/api/v1/dashboard/overview')
        assert resp.status_code == 401
    flask_app.config['TESTING'] = True
