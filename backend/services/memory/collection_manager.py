import logging
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams
from backend.services.memory.config import QdrantConfig
from backend.services.memory.qdrant_client import MemoryClient
from backend.services.memory.collection_schema import CollectionRegistry

logger = logging.getLogger(__name__)

class CollectionManager:
    def __init__(self, client: QdrantClient = None):
        self.client = client or MemoryClient.get_client()
        self.prefix = QdrantConfig.QDRANT_COLLECTION_PREFIX

    def get_prefixed_name(self, name: str) -> str:
        return f"{self.prefix}_{name}" if self.prefix else name

    def initialize_collections(self) -> bool:
        """Idempotently initialize all collections defined in the schema registry."""
        existing_collections_res = self.client.get_collections()
        existing_collections = [c.name for c in existing_collections_res.collections]

        for name, schema in CollectionRegistry.get_all_collections().items():
            prefixed_name = self.get_prefixed_name(name)
            
            if prefixed_name not in existing_collections:
                logger.info(f"Creating missing collection: {prefixed_name}")
                self.client.create_collection(
                    collection_name=prefixed_name,
                    vectors_config=VectorParams(
                        size=schema["dimension"],
                        distance=schema["distance"]
                    )
                )
            else:
                logger.info(f"Collection {prefixed_name} already exists. Verifying schema...")
                collection_info = self.client.get_collection(prefixed_name)
                # Verify dimensions
                vector_config = collection_info.config.params.vectors
                # Handle cases where vectors is a NamedVectorStruct or dict-like depending on qdrant-client version
                size = getattr(vector_config, "size", None)
                if size is None and hasattr(vector_config, "values"): # Support multiple named vectors format fallback
                    # In simple single vector collections, config.params.vectors is a VectorParams object.
                    pass 
                
                if size is not None and size != schema["dimension"]:
                    logger.error(f"Dimension mismatch for {prefixed_name}. Expected {schema['dimension']}, got {size}")
                    raise ValueError(f"Dimension mismatch for {prefixed_name}")
                    
        return True
