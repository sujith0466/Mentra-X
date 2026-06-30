import pytest
from unittest.mock import MagicMock

from backend.services.memory.collection_manager import CollectionManager
from backend.services.memory.collection_schema import CollectionRegistry
from qdrant_client.http.models import CollectionsResponse, CollectionDescription

@pytest.fixture
def mock_qdrant_client():
    client = MagicMock()
    return client

def test_collection_creation(mock_qdrant_client):
    # Mock no existing collections
    mock_qdrant_client.get_collections.return_value = CollectionsResponse(collections=[])
    
    manager = CollectionManager(client=mock_qdrant_client)
    manager.prefix = "test"
    
    result = manager.initialize_collections()
    assert result is True
    
    # Verify create_collection was called for each collection in the registry
    assert mock_qdrant_client.create_collection.call_count == len(CollectionRegistry.get_all_collections())
    
    # Check that prefixed names were used
    calls = mock_qdrant_client.create_collection.call_args_list
    created_names = [call.kwargs['collection_name'] for call in calls]
    assert "test_learning_dna" in created_names

def test_existing_collection_detection_and_validation(mock_qdrant_client):
    # Mock an existing collection
    mock_qdrant_client.get_collections.return_value = CollectionsResponse(
        collections=[CollectionDescription(name="test_learning_dna")]
    )
    
    # Mock get_collection to return matching dimensions without Pydantic validation
    mock_info = MagicMock()
    mock_info.config.params.vectors.size = 384
    mock_qdrant_client.get_collection.return_value = mock_info
    
    manager = CollectionManager(client=mock_qdrant_client)
    manager.prefix = "test"
    
    manager.initialize_collections()
    
    # Should create len - 1 collections
    assert mock_qdrant_client.create_collection.call_count == len(CollectionRegistry.get_all_collections()) - 1
    
def test_dimension_mismatch_detection(mock_qdrant_client):
    mock_qdrant_client.get_collections.return_value = CollectionsResponse(
        collections=[CollectionDescription(name="test_learning_dna")]
    )
    
    # Mock get_collection to return wrong dimensions
    mock_info = MagicMock()
    mock_info.config.params.vectors.size = 1536  # Mismatch (1536 instead of 384)
    mock_qdrant_client.get_collection.return_value = mock_info
    
    manager = CollectionManager(client=mock_qdrant_client)
    manager.prefix = "test"
    
    with pytest.raises(ValueError, match="Dimension mismatch for test_learning_dna"):
        manager.initialize_collections()
