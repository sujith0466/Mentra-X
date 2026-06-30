from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class MemoryRetrieveRequest:
    collection_name: str
    query_text: str
    limit: int = 5

    @classmethod
    def from_dict(cls, data: dict):
        if not data.get("collection_name"):
            raise ValueError("MEMORY_INVALID_COLLECTION")
        if not data.get("query_text"):
            raise ValueError("query_text is required")
        return cls(
            collection_name=data.get("collection_name"),
            query_text=data.get("query_text"),
            limit=int(data.get("limit", 5))
        )

@dataclass
class MemoryRetrieveResponse:
    results: List[Dict[str, Any]]
    
    def to_dict(self):
        return {"results": self.results}

@dataclass
class MemoryStoreRequest:
    memory_type: str
    text: str
    twin_version: str
    confidence: float = 1.0
    extra_data: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: dict):
        valid_types = ["learning_dna", "past_doubt", "explanation_history", "session_log", "weak_concept"]
        memory_type = data.get("memory_type")
        if memory_type not in valid_types:
            raise ValueError("MEMORY_INVALID_COLLECTION")
        if not data.get("text"):
            raise ValueError("text is required")
        if not data.get("twin_version"):
            raise ValueError("twin_version is required")
            
        return cls(
            memory_type=memory_type,
            text=data.get("text"),
            twin_version=data.get("twin_version"),
            confidence=float(data.get("confidence", 1.0)),
            extra_data=data.get("extra_data", {})
        )

@dataclass
class MemoryStoreResponse:
    status: str
    message: str
    
    def to_dict(self):
        return {"status": self.status, "message": self.message}
