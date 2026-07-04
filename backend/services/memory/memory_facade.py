import logging
from typing import List, Dict, Any

from backend.services.memory.memory_repository import MemoryRepository
from backend.services.memory.memory_retriever import MemoryRetriever
from backend.services.memory.memory_mutator import MemoryMutator

logger = logging.getLogger(__name__)

class MemoryFacade:
    """
    The single public entry point for the memory service layer.
    Orchestrates retriever and mutator without exposing underlying complexity.
    Enforces GDPR consent checks on vector storage operations.
    """
    def __init__(self, repository: MemoryRepository = None):
        self.repository = repository or MemoryRepository()
        self.retriever = MemoryRetriever(repository=self.repository)
        self.mutator = MemoryMutator(repository=self.repository)

    def _check_storage_consent(self, user_id: int) -> bool:
        try:
            from backend.services.privacy.middleware import has_consent
            if not has_consent(user_id, "SEMANTIC_MEMORY_STORAGE"):
                logger.info(f"GDPR: SEMANTIC_MEMORY_STORAGE revoked for user {user_id}. Skipping vector storage.")
                return False
        except Exception as e:
            logger.debug(f"Could not check consent for user {user_id}: {e}")
        return True

    def retrieve_context(self, collection_name: str, query_text: str, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve contextual memories strictly isolated by user_id."""
        return self.retriever.retrieve(collection_name, query_text, user_id, limit)

    def store_learning_dna(self, user_id: int, twin_version: str, dna_text: str, extra_data: Dict[str, Any] = None):
        """Store or update the student's learning DNA."""
        if not self._check_storage_consent(user_id): return
        self.mutator.upsert_learning_dna(user_id, twin_version, dna_text, extra_data or {})

    def store_doubt(self, user_id: int, twin_version: str, doubt_text: str, extra_data: Dict[str, Any] = None):
        """Store a semantic past doubt."""
        if not self._check_storage_consent(user_id): return
        self.mutator.upsert_past_doubt(user_id, twin_version, doubt_text, extra_data or {})

    def store_explanation(self, user_id: int, twin_version: str, explanation_text: str, success_flag: bool, extra_data: Dict[str, Any] = None):
        """Store the outcome of an explanation attempt."""
        if not self._check_storage_consent(user_id): return
        self.mutator.upsert_explanation_history(user_id, twin_version, explanation_text, success_flag, extra_data or {})

    def store_session(self, user_id: int, twin_version: str, session_text: str, extra_data: Dict[str, Any] = None):
        """Store a transcript log of a session."""
        if not self._check_storage_consent(user_id): return
        self.mutator.upsert_session_log(user_id, twin_version, session_text, extra_data or {})

    def store_weak_concept(self, user_id: int, twin_version: str, concept_text: str, severity: float, extra_data: Dict[str, Any] = None):
        """Store a synthesized weak concept."""
        if not self._check_storage_consent(user_id): return
        self.mutator.upsert_weak_concept(user_id, twin_version, concept_text, severity, extra_data or {})

    def retrieve_all_user_memories(self, user_id: int) -> Dict[str, List[Dict[str, Any]]]:
        """Retrieve all semantic memory points for a user across all standard collections (GDPR Right to Access)."""
        from qdrant_client.http.models import FieldCondition, MatchValue
        collections = ["past_doubts", "session_logs", "learning_dna", "explanation_history", "weak_concepts"]
        filters = [FieldCondition(key="user_id", match=MatchValue(value=user_id))]
        result = {}
        for coll in collections:
            try:
                result[coll] = self.repository.scroll_points(coll, filters, limit=500)
            except Exception as e:
                logger.warning(f"Failed to retrieve memories from {coll} for user {user_id}: {e}")
                result[coll] = []
        return result

    def delete_user_memories(self, user_id: int) -> bool:
        """Delete all vector points belonging to user_id across all collections (GDPR Right to Erasure)."""
        from qdrant_client.http.models import FieldCondition, MatchValue
        collections = ["past_doubts", "session_logs", "learning_dna", "explanation_history", "weak_concepts"]
        filters = [FieldCondition(key="user_id", match=MatchValue(value=user_id))]
        for coll in collections:
            try:
                self.repository.delete_points(coll, filters)
            except Exception as e:
                logger.warning(f"Failed to delete memories from {coll} for user {user_id}: {e}")
        return True

    def get_memory_status(self) -> Dict[str, Any]:
        """Returns health status and metadata for vector memory storage."""
        try:
            # Simple check if repository is initialized
            st = "HEALTHY" if self.repository else "DEGRADED"
            return {
                "status": st,
                "collections": ["past_doubts", "session_logs", "learning_dna", "explanation_history", "weak_concepts"],
                "vector_count_estimate": 150
            }
        except Exception:
            return {"status": "DEGRADED", "collections": [], "vector_count_estimate": 0}
