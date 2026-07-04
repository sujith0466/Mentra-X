import logging
from typing import List, Dict, Any
from datetime import datetime, timezone
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Filter, FieldCondition

from backend.services.memory.config import QdrantConfig
from backend.services.memory.qdrant_client import MemoryClient

logger = logging.getLogger(__name__)

class MemoryRepository:
    """
    Low-level data access layer for Qdrant.
    Handles upsert, delete, and retrieve operations without business logic.
    """
    def __init__(self, client: QdrantClient = None):
        self.client = client or MemoryClient.get_client()
        self.prefix = QdrantConfig.QDRANT_COLLECTION_PREFIX

    def _get_prefixed_name(self, name: str) -> str:
        return f"{self.prefix}_{name}" if self.prefix else name

    def upsert_point(self, collection_name: str, point_id: str, vector: List[float], payload: Dict[str, Any]):
        """Upsert a single point into a collection."""
        prefixed_name = self._get_prefixed_name(collection_name)
        
        # Enforce standard payload fields if not fully provided (basic fallback)
        payload.setdefault('created_at', datetime.utcnow().isoformat())
        payload.setdefault('updated_at', datetime.utcnow().isoformat())
        
        point = PointStruct(id=point_id, vector=vector, payload=payload)
        
        try:
            self.client.upsert(
                collection_name=prefixed_name,
                points=[point]
            )
        except Exception as e:
            logger.error(f"Failed to upsert point {point_id} to {prefixed_name}: {e}")
            raise

    def search_points(self, collection_name: str, query_vector: List[float], filter_conditions: List[FieldCondition], limit: int = 5) -> List[Dict[str, Any]]:
        """Search points using vector similarity and strict filters."""
        prefixed_name = self._get_prefixed_name(collection_name)
        
        query_filter = Filter(must=filter_conditions) if filter_conditions else None
        
        try:
            results = self.client.search(
                collection_name=prefixed_name,
                query_vector=query_vector,
                query_filter=query_filter,
                limit=limit
            )
            # Return reconstructed results
            return [
                {
                    "id": getattr(res, "id"),
                    "score": getattr(res, "score"),
                    "payload": getattr(res, "payload")
                }
                for res in results
            ]
        except Exception as e:
            logger.error(f"Failed to search points in {prefixed_name}: {e}")
            raise

    def delete_points(self, collection_name: str, filter_conditions: List[FieldCondition]):
        """Delete points based on filter conditions."""
        prefixed_name = self._get_prefixed_name(collection_name)
        query_filter = Filter(must=filter_conditions)
        
        try:
            self.client.delete(
                collection_name=prefixed_name,
                points_selector=query_filter
            )
        except Exception as e:
            logger.error(f"Failed to delete points from {prefixed_name}: {e}")
            raise

    def scroll_points(self, collection_name: str, filter_conditions: List[FieldCondition], limit: int = 100) -> List[Dict[str, Any]]:
        """Scroll points matching filter conditions without vector search."""
        prefixed_name = self._get_prefixed_name(collection_name)
        query_filter = Filter(must=filter_conditions) if filter_conditions else None
        try:
            results, _ = self.client.scroll(
                collection_name=prefixed_name,
                scroll_filter=query_filter,
                limit=limit
            )
            return [
                {
                    "id": getattr(res, "id"),
                    "payload": getattr(res, "payload")
                }
                for res in results
            ]
        except Exception as e:
            logger.error(f"Failed to scroll points in {prefixed_name}: {e}")
            return []
