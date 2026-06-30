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
    """
    def __init__(self, repository: MemoryRepository = None):
        self.repository = repository or MemoryRepository()
        self.retriever = MemoryRetriever(repository=self.repository)
        self.mutator = MemoryMutator(repository=self.repository)

    def retrieve_context(self, collection_name: str, query_text: str, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve contextual memories strictly isolated by user_id."""
        return self.retriever.retrieve(collection_name, query_text, user_id, limit)

    def store_learning_dna(self, user_id: int, twin_version: str, dna_text: str, extra_data: Dict[str, Any] = None):
        """Store or update the student's learning DNA."""
        self.mutator.upsert_learning_dna(user_id, twin_version, dna_text, extra_data or {})

    def store_doubt(self, user_id: int, twin_version: str, doubt_text: str, extra_data: Dict[str, Any] = None):
        """Store a semantic past doubt."""
        self.mutator.upsert_past_doubt(user_id, twin_version, doubt_text, extra_data or {})

    def store_explanation(self, user_id: int, twin_version: str, explanation_text: str, success_flag: bool, extra_data: Dict[str, Any] = None):
        """Store the outcome of an explanation attempt."""
        self.mutator.upsert_explanation_history(user_id, twin_version, explanation_text, success_flag, extra_data or {})

    def store_session(self, user_id: int, twin_version: str, session_text: str, extra_data: Dict[str, Any] = None):
        """Store a transcript log of a session."""
        self.mutator.upsert_session_log(user_id, twin_version, session_text, extra_data or {})

    def store_weak_concept(self, user_id: int, twin_version: str, concept_text: str, severity: float, extra_data: Dict[str, Any] = None):
        """Store a synthesized weak concept."""
        self.mutator.upsert_weak_concept(user_id, twin_version, concept_text, severity, extra_data or {})
