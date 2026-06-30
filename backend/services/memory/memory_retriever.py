import logging
from typing import List, Dict, Any
from qdrant_client.http.models import FieldCondition, MatchValue

from backend.services.memory.memory_repository import MemoryRepository
from backend.services.memory.embedding_provider import get_embedding_provider, EmbeddingProvider

logger = logging.getLogger(__name__)

class MemoryRetriever:
    """
    Handles semantic search, embeddings generation, and strictly enforces user_id isolation.
    """
    def __init__(self, repository: MemoryRepository = None, embedding_provider: EmbeddingProvider = None):
        self.repository = repository or MemoryRepository()
        self.embedding_provider = embedding_provider or get_embedding_provider()

    def _enforce_user_filter(self, user_id: int) -> FieldCondition:
        return FieldCondition(
            key="user_id",
            match=MatchValue(value=user_id)
        )

    def retrieve(self, collection_name: str, query_text: str, user_id: int, limit: int = 5, additional_filters: List[FieldCondition] = None) -> List[Dict[str, Any]]:
        """
        Embeds the query text and retrieves Top-K points, enforcing strict user_id isolation.
        """
        if not user_id:
            raise ValueError("user_id is mandatory for all semantic retrievals.")

        query_vector = self.embedding_provider.embed_text(query_text)
        
        filters = [self._enforce_user_filter(user_id)]
        if additional_filters:
            filters.extend(additional_filters)
            
        results = self.repository.search_points(
            collection_name=collection_name,
            query_vector=query_vector,
            filter_conditions=filters,
            limit=limit
        )
        
        return results
