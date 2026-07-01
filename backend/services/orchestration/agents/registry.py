import logging
from typing import Dict, Any, Type
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class AgentMetadata(BaseModel):
    name: str
    description: str
    version: str
    enabled: bool
    priority: int
    allowed_tools: list[str]
    allowed_collections: list[str]
    max_tokens: int
    temperature: float
    timeout_ms: int
    retry_count: int

class AgentBase:
    """
    Base class for all Mastra Swarm agents.
    """
    metadata: AgentMetadata

    def __init__(self):
        pass
        
    def execute(self, unified_context: Dict[str, Any], query: str) -> Dict[str, Any]:
        raise NotImplementedError("Agents must implement the execute method.")

class AgentRegistry:
    """
    Plugin-based Agent Registry. Allows dynamic discovery of agents.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
            cls._instance._agents: Dict[str, AgentBase] = {}
        return cls._instance

    def register_agent(self, agent: AgentBase):
        name = agent.metadata.name
        if name in self._agents:
            logger.warning(f"Agent {name} already registered. Overwriting.")
        
        self._agents[name] = agent
        logger.info(f"Registered agent: {name} v{agent.metadata.version}")

    def discover_agents(self) -> list[AgentMetadata]:
        """
        Returns metadata for all enabled agents.
        """
        return [
            agent.metadata 
            for agent in self._agents.values() 
            if agent.metadata.enabled
        ]

    def get_agent(self, name: str) -> AgentBase:
        if name not in self._agents:
            raise ValueError(f"Agent {name} not found in registry.")
        return self._agents[name]

    def agent_capabilities(self, name: str) -> dict:
        agent = self.get_agent(name)
        return {
            "tools": agent.metadata.allowed_tools,
            "collections": agent.metadata.allowed_collections
        }

    def health_check(self, name: str) -> bool:
        """
        Ping the underlying agent representation to ensure availability.
        """
        try:
            self.get_agent(name)
            return True
        except Exception:
            return False

    def clear(self):
        """For testing purposes."""
        self._agents.clear()
