import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class PromptRegistry:
    """
    Loads agent prompts dynamically from the filesystem.
    """
    _instance = None
    _prompts = {}
    _prompt_dir = os.path.join(os.path.dirname(__file__))

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PromptRegistry, cls).__new__(cls)
            cls._instance._load_prompts()
        return cls._instance

    def _load_prompts(self):
        for filename in os.listdir(self._prompt_dir):
            if filename.endswith(".md"):
                name = filename[:-3]
                path = os.path.join(self._prompt_dir, filename)
                with open(path, "r", encoding="utf-8") as f:
                    self._prompts[name] = f.read()
        logger.info(f"Loaded {len(self._prompts)} prompts from {self._prompt_dir}")

    def get_prompt(self, agent_name: str) -> str:
        """
        Gets the prompt for an agent. Normalizes name (e.g., TutorAgent -> tutor).
        """
        key = agent_name.lower().replace("agent", "")
        if key not in self._prompts:
            # Fallback to an empty or default prompt if not found
            logger.warning(f"Prompt for {agent_name} ({key}.md) not found.")
            return "You are a helpful AI assistant."
        return self._prompts[key]

    def reload(self):
        """Reloads prompts from disk."""
        self._prompts.clear()
        self._load_prompts()
