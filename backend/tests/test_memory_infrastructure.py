from unittest.mock import patch, MagicMock
from backend.services.memory.config import QdrantConfig
from backend.services.memory.qdrant_client import MemoryClient

def test_qdrant_config():
    assert QdrantConfig.QDRANT_HOST == "localhost"
    assert QdrantConfig.QDRANT_PORT == 6333
    assert QdrantConfig.is_configured()

@patch('backend.services.memory.qdrant_client.QdrantClient')
def test_qdrant_client_initialization(mock_qdrant):
    mock_instance = MagicMock()
    mock_qdrant.return_value = mock_instance
    
    # Reset singleton for testing
    MemoryClient._instance = None
    
    client = MemoryClient.get_client()
    assert client is not None
    mock_qdrant.assert_called_once_with(
        url="http://localhost:6333",
        api_key=None,
        timeout=10.0,
        prefer_grpc=True
    )

@patch('backend.services.memory.qdrant_client.QdrantClient')
def test_qdrant_health_check(mock_qdrant):
    mock_instance = MagicMock()
    mock_qdrant.return_value = mock_instance
    
    # Reset singleton for testing
    MemoryClient._instance = None
    
    is_healthy = MemoryClient.check_health()
    assert is_healthy is True
    mock_instance.get_collections.assert_called_once()
