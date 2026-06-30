import pytest
from unittest.mock import MagicMock, patch

from backend.services.memory.memory_repository import MemoryRepository
from backend.services.memory.memory_retriever import MemoryRetriever
from backend.services.memory.memory_mutator import MemoryMutator
from backend.services.memory.memory_facade import MemoryFacade

@pytest.fixture
def mock_qdrant_client():
    return MagicMock()

@pytest.fixture
def mock_embedding_provider():
    provider = MagicMock()
    provider.embed_text.return_value = [0.1, 0.2, 0.3]
    return provider

def test_repository_upsert(mock_qdrant_client):
    repo = MemoryRepository(client=mock_qdrant_client)
    repo.prefix = "test"
    
    repo.upsert_point("test_collection", "uuid-123", [0.1], {"user_id": 1})
    
    mock_qdrant_client.upsert.assert_called_once()
    args, kwargs = mock_qdrant_client.upsert.call_args
    assert kwargs["collection_name"] == "test_test_collection"
    
    points = kwargs["points"]
    assert len(points) == 1
    assert points[0].id == "uuid-123"
    assert points[0].payload["user_id"] == 1
    assert "created_at" in points[0].payload

def test_retriever_enforces_user_isolation(mock_qdrant_client, mock_embedding_provider):
    repo = MemoryRepository(client=mock_qdrant_client)
    retriever = MemoryRetriever(repository=repo, embedding_provider=mock_embedding_provider)
    
    # Must raise if no user_id is provided
    with pytest.raises(ValueError, match="user_id is mandatory"):
        retriever.retrieve("test_collection", "hello", user_id=None)
        
    # Valid retrieval
    mock_qdrant_client.search.return_value = []
    retriever.retrieve("test_collection", "hello", user_id=42)
    
    mock_qdrant_client.search.assert_called_once()
    args, kwargs = mock_qdrant_client.search.call_args
    
    # Check that filter contains user_id=42
    query_filter = kwargs["query_filter"]
    assert query_filter is not None
    assert len(query_filter.must) == 1
    assert query_filter.must[0].key == "user_id"
    assert query_filter.must[0].match.value == 42

def test_mutator_operations(mock_qdrant_client, mock_embedding_provider):
    repo = MemoryRepository(client=mock_qdrant_client)
    mutator = MemoryMutator(repository=repo, embedding_provider=mock_embedding_provider)
    
    mutator.upsert_weak_concept(user_id=1, twin_version="1.0", concept_text="Calculus", severity=0.8, extra_data={"foo": "bar"})
    
    mock_qdrant_client.upsert.assert_called_once()
    args, kwargs = mock_qdrant_client.upsert.call_args
    assert kwargs["collection_name"] == "mentra_weak_concepts"  # default prefix is 'mentra'
    payload = kwargs["points"][0].payload
    
    assert payload["user_id"] == 1
    assert payload["severity_score"] == 0.8
    assert payload["event_type"] == "weak_concept_logged"
    assert payload["foo"] == "bar"

def test_facade_orchestration():
    mock_repo = MagicMock()
    
    with patch('backend.services.memory.memory_facade.MemoryRetriever') as MockRetriever, \
         patch('backend.services.memory.memory_facade.MemoryMutator') as MockMutator:
         
        mock_retriever = MockRetriever.return_value
        mock_mutator = MockMutator.return_value
        
        facade = MemoryFacade(repository=mock_repo)
        
        # Test retrieve
        facade.retrieve_context("coll", "query", 1, limit=10)
        mock_retriever.retrieve.assert_called_once_with("coll", "query", 1, 10)
        
        # Test store
        facade.store_learning_dna(1, "1.0", "DNA", {"extra": "data"})
        mock_mutator.upsert_learning_dna.assert_called_once_with(1, "1.0", "DNA", {"extra": "data"})
