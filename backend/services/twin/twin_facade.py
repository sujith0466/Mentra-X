import logging
from backend.services.twin.twin_builder import build_initial_twin
from backend.services.twin.twin_mutator import mutate_knowledge, mutate_learning_dna

logger = logging.getLogger(__name__)

class TwinFacade:
    """
    TwinFacade provides a strict boundary for all Digital Twin operations.
    It encapsulates twin building, fetching, and safe mutation.
    """

    @staticmethod
    def get_twin(user_id: int):
        """
        Retrieves the twin, initializing it if necessary.
        """
        try:
            return build_initial_twin(user_id)
        except Exception as e:
            logger.error(f"Failed to get twin for user {user_id}: {e}")
            raise

    @staticmethod
    def mutate_knowledge_state(user_id: int, concept: str, new_score: float, agent_name: str = "System"):
        """
        Safely updates the twin's knowledge state for a given concept.
        """
        try:
            success = mutate_knowledge(user_id, concept, new_score, "KNOWLEDGE_UPDATE", agent_name)
            return {"success": success}
        except Exception as e:
            logger.error(f"Failed to mutate knowledge state for user {user_id}: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def mutate_learning_dna(user_id: int, new_dna: dict, agent_name: str = "System"):
        """
        Safely updates the twin's learning DNA.
        """
        try:
            success = mutate_learning_dna(user_id, new_dna, "DNA_UPDATE", agent_name)
            return {"success": success}
        except Exception as e:
            logger.error(f"Failed to mutate learning DNA for user {user_id}: {e}")
            return {"success": False, "error": str(e)}
