import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class ReasoningStep:
    """
    Represents a single safe, user-facing reasoning step within an AI workflow.
    Strictly excludes internal chain-of-thought tokens or raw LLM scratchpads.
    """
    def __init__(
        self,
        step_id: int,
        agent_name: str,
        action_summary: str,
        tool_invoked: Optional[str] = None,
        outcome_status: str = "SUCCESS",
        timestamp: Optional[str] = None
    ):
        self.step_id = step_id
        self.agent_name = agent_name
        self.action_summary = self._sanitize_summary(action_summary)
        self.tool_invoked = tool_invoked
        self.outcome_status = outcome_status
        self.timestamp = timestamp or datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _sanitize_summary(text: str) -> str:
        """Strips out potential internal CoT markers or sensitive system tags."""
        if not text:
            return "Executed reasoning step."
        # Strip common CoT tags if present
        for tag in ["<thought>", "</thought>", "<thinking>", "</thinking>", "System Prompt:", "Chain of Thought:"]:
            text = text.replace(tag, "")
        return text.strip()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "agent_name": self.agent_name,
            "action_summary": self.action_summary,
            "tool_invoked": self.tool_invoked,
            "outcome_status": self.outcome_status,
            "timestamp": self.timestamp
        }


class ReasoningTrace:
    """
    Aggregates a sequence of ReasoningSteps for a workflow.
    """
    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id
        self.steps: List[ReasoningStep] = []

    def add_step(
        self,
        agent_name: str,
        action_summary: str,
        tool_invoked: Optional[str] = None,
        outcome_status: str = "SUCCESS"
    ) -> ReasoningStep:
        step = ReasoningStep(
            step_id=len(self.steps) + 1,
            agent_name=agent_name,
            action_summary=action_summary,
            tool_invoked=tool_invoked,
            outcome_status=outcome_status
        )
        self.steps.append(step)
        return step

    def get_safe_summary(self) -> str:
        """Returns a high-level narrative summary of the workflow reasoning."""
        if not self.steps:
            return "No reasoning steps recorded."
        summary_lines = [f"Workflow {self.workflow_id} executed {len(self.steps)} key steps:"]
        for s in self.steps:
            tool_info = f" (via tool `{s.tool_invoked}`)" if s.tool_invoked else ""
            summary_lines.append(f"- Step {s.step_id} [{s.agent_name}]: {s.action_summary}{tool_info} [{s.outcome_status}]")
        return "\n".join(summary_lines)

    def to_list(self) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self.steps]
