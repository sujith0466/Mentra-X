import pytest
from unittest.mock import patch, MagicMock

from backend.services.memory.config import QdrantConfig
from backend.services.memory.embedding_provider import (
    LocalEmbeddingProvider,
    OpenAIEmbeddingProvider,
    get_embedding_provider
)

def test_provider_selection_local():
    QdrantConfig.EMBEDDING_PROVIDER = "local"
    provider = get_embedding_provider()
    assert isinstance(provider, LocalEmbeddingProvider)

def test_provider_selection_openai():
    QdrantConfig.EMBEDDING_PROVIDER = "openai"
    provider = get_embedding_provider()
    assert isinstance(provider, OpenAIEmbeddingProvider)

def test_provider_selection_invalid_fallback():
    QdrantConfig.EMBEDDING_PROVIDER = "invalid_provider"
    provider = get_embedding_provider()
    assert isinstance(provider, LocalEmbeddingProvider)

def test_openai_provider_stub():
    provider = OpenAIEmbeddingProvider()
    with pytest.raises(NotImplementedError):
        provider.embed_text("test")

@patch('backend.services.memory.embedding_provider.LocalEmbeddingProvider._get_model')
def test_local_embedding_generation(mock_get_model):
    import numpy as np
    mock_model = MagicMock()
    # Mocking a deterministic response with numpy array so .tolist() works
    mock_model.encode.return_value = np.array([0.1, 0.2, 0.3])
    mock_get_model.return_value = mock_model
    
    provider = LocalEmbeddingProvider()
    result = provider.embed_text("hello world")
    
    assert isinstance(result, list)
    assert result == [0.1, 0.2, 0.3]
    mock_model.encode.assert_called_once_with("hello world", normalize_embeddings=True)

@patch('sentence_transformers.SentenceTransformer')
def test_local_provider_lazy_singleton(mock_st):
    mock_st.return_value = MagicMock()
    
    # Reset singleton
    LocalEmbeddingProvider._model_instance = None
    
    provider = LocalEmbeddingProvider(model_name="test-model", device="cpu")
    
    # Model shouldn't be loaded on init
    mock_st.assert_not_called()
    assert LocalEmbeddingProvider._model_instance is None
    
    # First get_model should load
    model1 = LocalEmbeddingProvider._get_model("test-model", "cpu")
    mock_st.assert_called_once_with("test-model", device="cpu")
    
    # Second get_model should use cached instance
    model2 = LocalEmbeddingProvider._get_model("test-model", "cpu")
    assert mock_st.call_count == 1
    assert model1 is model2
