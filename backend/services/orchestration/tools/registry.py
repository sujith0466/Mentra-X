import logging
from typing import Dict, Any, Callable, Optional
from pydantic import BaseModel
from backend.services.observability.decorators import trace_tool_call

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
        Automatically instruments the tool function with OpenTelemetry and metrics.
        """
        name = definition.name
        if name in self._tools:
            logger.warning(f"Tool {name} is already registered. Overwriting.")
        
        if not getattr(func, "_is_instrumented", False):
            instrumented_func = trace_tool_call(tool_name=name)(func)
            instrumented_func._is_instrumented = True
        else:
            instrumented_func = func

        self._tools[name] = {
            "definition": definition,
            "func": instrumented_func
        }
        logger.info(f"Registered tool: {name} v{definition.version}")

    def execute_tool(self, name: str, *args, **kwargs) -> Any:
        """
        Executes a registered tool by name with automatic instrumentation.
        """
        tool = self.get_tool(name)
        if not tool or "func" not in tool:
            raise ValueError(f"Tool {name} not found in ToolRegistry.")
        return tool["func"](*args, **kwargs)

    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        return self._tools.get(name)

    def get_all_tools(self) -> Dict[str, Dict[str, Any]]:
        return self._tools

    def clear(self):
        """For testing purposes."""
        self._tools.clear()
