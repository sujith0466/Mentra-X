import os

class QdrantConfig:
    ENABLE_QDRANT = os.getenv("ENABLE_QDRANT", "true").lower() == "true"
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_GRPC_PORT = int(os.getenv("QDRANT_GRPC_PORT", "6334"))
    QDRANT_COLLECTION_PREFIX = os.getenv("QDRANT_COLLECTION_PREFIX", "mentra")
    
    # Optional API key for cloud deployments
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
    
    # Embedding Configuration
    EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local").lower()
    LOCAL_EMBEDDING_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
    
    @classmethod
    def get_url(cls) -> str:
        return f"http://{cls.QDRANT_HOST}:{cls.QDRANT_PORT}"

    @classmethod
    def is_configured(cls) -> bool:
        return bool(cls.ENABLE_QDRANT and cls.QDRANT_HOST and cls.QDRANT_PORT)
