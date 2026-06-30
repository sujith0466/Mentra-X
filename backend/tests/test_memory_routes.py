import pytest
from unittest.mock import patch
from flask import Flask

from backend.routes.memory_routes import memory_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.secret_key = 'test'
    app.register_blueprint(memory_bp)
    
    with app.test_client() as client:
        yield client

def test_unauthorized_access(client):
    response = client.get('/api/v1/memory/health')
    assert response.status_code == 401
    
    response = client.post('/api/v1/memory/retrieve', json={})
    assert response.status_code == 401

@patch('backend.routes.memory_routes.MemoryClient.check_health')
@patch('backend.routes.memory_routes.get_embedding_provider')
def test_health_endpoint_healthy(mock_get_provider, mock_check_health, client):
    mock_check_health.return_value = True
    
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        
    response = client.get('/api/v1/memory/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['qdrant'] is True
    assert data['embeddings'] is True

@patch('backend.routes.memory_routes.MemoryClient.check_health')
@patch('backend.routes.memory_routes.get_embedding_provider')
def test_health_endpoint_unhealthy(mock_get_provider, mock_check_health, client):
    mock_check_health.return_value = False
    mock_get_provider.side_effect = Exception("Failed")
    
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        
    response = client.get('/api/v1/memory/health')
    assert response.status_code == 503
    data = response.get_json()
    assert data['message'] == 'MEMORY_QDRANT_UNAVAILABLE'
    assert data['qdrant'] is False
    assert data['embeddings'] is False

def test_status_endpoint(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        
    response = client.get('/api/v1/memory/status')
    assert response.status_code == 200
    assert 'collections' in response.get_json()

@patch('backend.routes.memory_routes.facade.retrieve_context')
def test_retrieve_endpoint(mock_retrieve, client):
    mock_retrieve.return_value = [{"id": "1", "score": 0.9, "payload": {}}]
    
    with client.session_transaction() as sess:
        sess['user_id'] = 42
        
    response = client.post('/api/v1/memory/retrieve', json={
        "collection_name": "past_doubts",
        "query_text": "hello"
    })
    
    assert response.status_code == 200
    mock_retrieve.assert_called_once_with(
        collection_name="past_doubts",
        query_text="hello",
        user_id=42,
        limit=5
    )

def test_retrieve_endpoint_invalid_payload(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 42
        
    response = client.post('/api/v1/memory/retrieve', json={
        "collection_name": ""
    })
    
    assert response.status_code == 400
    assert response.get_json()['message'] == "MEMORY_INVALID_COLLECTION"

@patch('backend.routes.memory_routes.facade.store_doubt')
def test_store_endpoint(mock_store, client):
    with client.session_transaction() as sess:
        sess['user_id'] = 42
        
    response = client.post('/api/v1/memory/store', json={
        "memory_type": "past_doubt",
        "text": "How does gravity work?",
        "twin_version": "1.0",
        "extra_data": {"source": "quiz"}
    })
    
    assert response.status_code == 201
    mock_store.assert_called_once_with(42, "1.0", "How does gravity work?", {"source": "quiz"})

def test_store_endpoint_invalid_type(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 42
        
    response = client.post('/api/v1/memory/store', json={
        "memory_type": "invalid_type",
        "text": "hello",
        "twin_version": "1.0"
    })
    
    assert response.status_code == 400
    assert response.get_json()['message'] == "MEMORY_INVALID_COLLECTION"
