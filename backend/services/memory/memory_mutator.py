import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, Any

from backend.services.memory.memory_repository import MemoryRepository
from backend.services.memory.embedding_provider import get_embedding_provider, EmbeddingProvider

logger = logging.getLogger(__name__)

class MemoryMutator:
    """
    Handles data formatting, payload standardization, embedding, and saving to the repository.
    """
    def __init__(self, repository: MemoryRepository = None, embedding_provider: EmbeddingProvider = None):
        self.repository = repository or MemoryRepository()
        self.embedding_provider = embedding_provider or get_embedding_provider()

    def _build_standard_payload(
        self,
        user_id: int,
        twin_version: str,
        source: str,
        event_type: str,
        confidence: float,
        extra_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Construct a payload adhering to the standard requirements."""
        payload = {
            "user_id": user_id,
            "twin_version": twin_version,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "source": source,
            "event_type": event_type,
            "confidence": confidence,
        }
        payload.update(extra_data)
        return payload

    def upsert_learning_dna(self, user_id: int, twin_version: str, text: str, extra_data: Dict[str, Any]):
        vector = self.embedding_provider.embed_text(text)
        payload = self._build_standard_payload(user_id, twin_version, "twin_engine", "dna_update", 0.9, extra_data)
        # Using a deterministic ID per user for DNA to ensure we overwrite/update rather than append
        point_id = str(uuid.uuid5(uuid.NAMESPACE_OID, f"dna_{user_id}"))
        self.repository.upsert_point("learning_dna", point_id, vector, payload)

    def upsert_past_doubt(self, user_id: int, twin_version: str, doubt_text: str, extra_data: Dict[str, Any]):
        vector = self.embedding_provider.embed_text(doubt_text)
        payload = self._build_standard_payload(user_id, twin_version, "assessment_engine", "doubt_logged", 1.0, extra_data)
        point_id = str(uuid.uuid4())
        self.repository.upsert_point("past_doubts", point_id, vector, payload)

    def upsert_explanation_history(self, user_id: int, twin_version: str, explanation_text: str, success_flag: bool, extra_data: Dict[str, Any]):
        vector = self.embedding_provider.embed_text(explanation_text)
        extra_data["success_flag"] = success_flag
        payload = self._build_standard_payload(user_id, twin_version, "mastra_engine", "explanation_logged", 0.8, extra_data)
        point_id = str(uuid.uuid4())
        self.repository.upsert_point("explanation_history", point_id, vector, payload)

    def upsert_session_log(self, user_id: int, twin_version: str, session_text: str, extra_data: Dict[str, Any]):
        vector = self.embedding_provider.embed_text(session_text)
        payload = self._build_standard_payload(user_id, twin_version, "lms_core", "session_transcribed", 1.0, extra_data)
        point_id = str(uuid.uuid4())
        self.repository.upsert_point("session_logs", point_id, vector, payload)

    def upsert_weak_concept(self, user_id: int, twin_version: str, concept_text: str, severity: float, extra_data: Dict[str, Any]):
        vector = self.embedding_provider.embed_text(concept_text)
        extra_data["severity_score"] = severity
        payload = self._build_standard_payload(user_id, twin_version, "assessment_engine", "weak_concept_logged", 0.9, extra_data)
        point_id = str(uuid.uuid4())
        self.repository.upsert_point("weak_concepts", point_id, vector, payload)
