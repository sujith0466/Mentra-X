import logging
from qdrant_client import QdrantClient
from backend.services.memory.config import QdrantConfig

logger = logging.getLogger(__name__)

class MemoryClient:
    _instance = None

    @classmethod
    def get_client(cls) -> QdrantClient:
        if cls._instance is None:
            url = QdrantConfig.get_url()
            logger.info(f"Initializing QdrantClient at {url}")
            try:
                cls._instance = QdrantClient(
                    url=url,
                    api_key=QdrantConfig.QDRANT_API_KEY or None,
                    timeout=10.0,
                    prefer_grpc=True
                )
            except Exception as e:
                logger.error(f"Failed to initialize QdrantClient: {e}")
                raise
        return cls._instance

    @classmethod
    def check_health(cls) -> bool:
        """Ping the Qdrant instance to check health."""
        try:
            client = cls.get_client()
            # Calling get_collections serves as a basic ping to check connectivity
            client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Qdrant health check failed: {e}")
            return False
