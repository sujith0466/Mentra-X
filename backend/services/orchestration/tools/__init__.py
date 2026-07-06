# Tools Package
from .registry import ToolRegistry, ToolDefinition
from .twin_tools import register_twin_tools
from .memory_tools import register_memory_tools
from .assessment_tools import register_assessment_tools
from .tutor_tools import register_tutor_tools
from .path_tools import register_path_tools
from .content_tools import register_content_tools
from .feedback_tools import register_feedback_tools
from .pacing_tools import register_pacing_tools
from .recommendation_tools import register_recommendation_tools
from .safety_tools import register_safety_tools

def register_all_tools(registry: ToolRegistry = None) -> ToolRegistry:
    if registry is None:
        registry = ToolRegistry()
    register_twin_tools(registry)
    register_memory_tools(registry)
    register_assessment_tools(registry)
    register_tutor_tools(registry)
    register_path_tools(registry)
    register_content_tools(registry)
    register_feedback_tools(registry)
    register_pacing_tools(registry)
    register_recommendation_tools(registry)
    register_safety_tools(registry)
    return registry

__all__ = [
    "ToolRegistry",
    "ToolDefinition",
    "register_twin_tools",
    "register_memory_tools",
    "register_assessment_tools",
    "register_tutor_tools",
    "register_path_tools",
    "register_content_tools",
    "register_feedback_tools",
    "register_pacing_tools",
    "register_recommendation_tools",
    "register_safety_tools",
    "register_all_tools"
]
