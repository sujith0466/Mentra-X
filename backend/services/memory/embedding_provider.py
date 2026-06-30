import logging
from abc import ABC, abstractmethod
from typing import List

from backend.services.memory.config import QdrantConfig

logger = logging.getLogger(__name__)

class EmbeddingProvider(ABC):
    """Abstract Base Class for generating vector embeddings."""
    
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass
    
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        pass


class LocalEmbeddingProvider(EmbeddingProvider):
    """
    Local embedding provider using sentence-transformers.
    Implements a lazy-loading singleton for the model to minimize memory overhead.
    """
    _model_instance = None
    
    def __init__(self, model_name: str = None, device: str = "cpu"):
        self.model_name = model_name or QdrantConfig.LOCAL_EMBEDDING_MODEL
        self.device = device
        
    @classmethod
    def _get_model(cls, model_name: str, device: str):
        """Lazy load and return the singleton model instance."""
        if cls._model_instance is None:
            logger.info(f"Loading local embedding model: {model_name} on {device}")
            from sentence_transformers import SentenceTransformer
            cls._model_instance = SentenceTransformer(model_name, device=device)
        return cls._model_instance

    def embed_text(self, text: str) -> List[float]:
        """Generate deterministic embedding for a single text."""
        model = self._get_model(self.model_name, self.device)
        # normalize_embeddings=True can help ensure deterministic/comparable vectors
        embedding = model.encode(text, normalize_embeddings=True)
        return embedding.tolist()
        
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate deterministic embeddings for a batch of texts."""
        model = self._get_model(self.model_name, self.device)
        embeddings = model.encode(texts, normalize_embeddings=True)
        return [emb.tolist() for emb in embeddings]


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """
    Future stub for OpenAI embeddings.
    """
    def __init__(self):
        logger.warning("OpenAIEmbeddingProvider is a stub and not fully implemented yet.")
        
    def embed_text(self, text: str) -> List[float]:
        raise NotImplementedError("OpenAI embeddings are not yet enabled for this phase.")
        
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError("OpenAI embeddings are not yet enabled for this phase.")


def get_embedding_provider() -> EmbeddingProvider:
    """Factory function to get the configured embedding provider."""
    provider_type = QdrantConfig.EMBEDDING_PROVIDER
    if provider_type == "local":
        return LocalEmbeddingProvider()
    elif provider_type == "openai":
        return OpenAIEmbeddingProvider()
    else:
        logger.warning(f"Unknown embedding provider '{provider_type}', falling back to local.")
        return LocalEmbeddingProvider()
