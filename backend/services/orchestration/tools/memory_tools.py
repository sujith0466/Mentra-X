from backend.services.orchestration.tools.registry import ToolRegistry, ToolDefinition
from backend.services.memory.memory_facade import MemoryFacade
import logging

logger = logging.getLogger(__name__)

def register_memory_tools(registry: ToolRegistry):
    memory_facade = MemoryFacade()

    retrieve_memory_def = ToolDefinition(
        name="retrieve_semantic_memory",
        description="Fetch contextual Qdrant logs.",
        version="1.1.0",
        owner="MemoryServiceTeam",
        permissions="memory:read",
        is_mutable=False,
        supports_streaming=False,
        supports_parallel=True,
        deterministic=True,
        needs_verification=False,
        produces_events=[],
        consumes_events=[],
        input_schema={
            "type": "object", 
            "properties": {
                "user_id": {"type": "integer"},
                "query": {"type": "string"},
                "collection": {"type": "string"},
                "limit": {"type": "integer", "default": 5}
            }, 
            "required": ["user_id", "query", "collection"]
        },
        output_schema={"type": "array", "items": {"type": "object"}},
        timeout_ms=3000,
        retry_count=2
    )

    def retrieve_memory_impl(kwargs: dict):
        return memory_facade.retrieve_context(
            collection_name=kwargs["collection"],
            query_text=kwargs["query"],
            user_id=kwargs["user_id"],
            limit=kwargs.get("limit", 5)
        )

    registry.register_tool(retrieve_memory_def, retrieve_memory_impl)
    logger.info("Registered memory tools.")
