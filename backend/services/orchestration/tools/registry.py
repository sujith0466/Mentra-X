import logging
from typing import Dict, Any, Callable, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class ToolDefinition(BaseModel):
    name: str
    description: str
    version: str
    owner: str
    permissions: str
    is_mutable: bool
    supports_streaming: bool
    supports_parallel: bool
    deterministic: bool
    needs_verification: bool
    produces_events: list[str]
    consumes_events: list[str]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    timeout_ms: int
    retry_count: int

class ToolRegistry:
    """
    Single Source of Truth for all tools available to the Mastra Cognitive Swarm.
    Tools must be explicitly registered here. Agents discover capabilities via this registry.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance._tools: Dict[str, Dict[str, Any]] = {}
        return cls._instance

    def register_tool(self, definition: ToolDefinition, func: Callable):
        """
        Registers a tool implementation alongside its strict definition.
        """
        name = definition.name
        if name in self._tools:
            logger.warning(f"Tool {name} is already registered. Overwriting.")
        
        self._tools[name] = {
            "definition": definition,
            "func": func
        }
        logger.info(f"Registered tool: {name} v{definition.version}")

    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        return self._tools.get(name)

    def get_all_tools(self) -> Dict[str, Dict[str, Any]]:
        return self._tools

    def clear(self):
        """For testing purposes."""
        self._tools.clear()
