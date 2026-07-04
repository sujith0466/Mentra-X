import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class DecisionNode:
    """Represents a single node in the workflow execution DAG."""
    def __init__(
        self,
        node_id: str,
        node_type: str,
        label: str,
        latency_ms: float = 0.0,
        status: str = "SUCCESS",
        trace_id: Optional[str] = None,
        confidence: float = 1.0,
        retry_count: int = 0
    ):
        self.node_id = node_id
        self.node_type = node_type # workflow, agent, tool, memory, assessment, verification, response
        self.label = label
        self.latency_ms = latency_ms
        self.status = status
        self.trace_id = trace_id or "trace-default-0000"
        self.confidence = confidence
        self.retry_count = retry_count
        self.children: List[str] = []

    def add_child(self, child_id: str):
        if child_id not in self.children:
            self.children.append(child_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "label": self.label,
            "latency_ms": self.latency_ms,
            "status": self.status,
            "trace_id": self.trace_id,
            "confidence": self.confidence,
            "retry_count": self.retry_count,
            "children": self.children
        }


class DecisionGraphBuilder:
    """
    Constructs a Directed Acyclic Graph (DAG) representing workflow execution:
    workflow -> agent -> tool -> memory lookup -> assessment lookup -> verification -> response.
    """
    def __init__(self, workflow_id: str, trace_id: Optional[str] = None):
        self.workflow_id = workflow_id
        self.trace_id = trace_id or f"trace-{workflow_id}"
        self.nodes: Dict[str, DecisionNode] = {}
        
        # Initialize root workflow node
        self.root_id = f"wf-{workflow_id}"
        self.add_node(self.root_id, "workflow", f"Workflow: {workflow_id}", trace_id=self.trace_id)

    def add_node(
        self,
        node_id: str,
        node_type: str,
        label: str,
        parent_id: Optional[str] = None,
        latency_ms: float = 0.0,
        status: str = "SUCCESS",
        trace_id: Optional[str] = None,
        confidence: float = 1.0,
        retry_count: int = 0
    ) -> DecisionNode:
        node = DecisionNode(
            node_id=node_id,
            node_type=node_type,
            label=label,
            latency_ms=latency_ms,
            status=status,
            trace_id=trace_id or self.trace_id,
            confidence=confidence,
            retry_count=retry_count
        )
        self.nodes[node_id] = node
        
        if parent_id and parent_id in self.nodes:
            self.nodes[parent_id].add_child(node_id)
        elif parent_id is None and node_id != self.root_id and self.root_id in self.nodes:
            self.nodes[self.root_id].add_child(node_id)
            
        return node

    def build_from_workflow_events(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Dynamically builds DAG nodes from recorded execution_events."""
        last_parent = self.root_id
        
        for idx, ev in enumerate(events):
            ev_type = ev.get("event_type", "agent_action")
            agent_name = ev.get("agent_name", "Orchestrator")
            status = ev.get("status", "SUCCESS")
            latency = float(ev.get("latency_ms", 15.0))
            retry = int(ev.get("retry_count", 0))
            conf = float(ev.get("confidence", 0.95))
            
            agent_node_id = f"agent-{idx}-{agent_name}"
            self.add_node(
                node_id=agent_node_id,
                node_type="agent",
                label=f"Agent: {agent_name}",
                parent_id=last_parent,
                latency_ms=latency,
                status=status,
                confidence=conf,
                retry_count=retry
            )
            last_parent = agent_node_id
            
            tool_name = ev.get("tool_name")
            if tool_name:
                tool_node_id = f"tool-{idx}-{tool_name}"
                self.add_node(
                    node_id=tool_node_id,
                    node_type="tool",
                    label=f"Tool: {tool_name}",
                    parent_id=agent_node_id,
                    latency_ms=latency * 0.4,
                    status=status
                )
                
                # Check for memory or assessment lookups
                if "memory" in tool_name.lower() or "qdrant" in tool_name.lower():
                    mem_id = f"mem-{idx}"
                    self.add_node(mem_id, "memory", "Memory Lookup: Qdrant", parent_id=tool_node_id, latency_ms=5.0)
                elif "assessment" in tool_name.lower() or "quiz" in tool_name.lower():
                    ass_id = f"ass-{idx}"
                    self.add_node(ass_id, "assessment", "Assessment Lookup", parent_id=tool_node_id, latency_ms=8.0)

        # Add terminal verification and response nodes
        verif_id = f"verif-{len(events)}"
        self.add_node(verif_id, "verification", "Verification Agent Check", parent_id=last_parent, latency_ms=10.0, confidence=0.98)
        resp_id = f"resp-{len(events)}"
        self.add_node(resp_id, "response", "Final AI Response Delivered", parent_id=verif_id, latency_ms=2.0)
        
        return self.to_dict()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "trace_id": self.trace_id,
            "root_id": self.root_id,
            "node_count": len(self.nodes),
            "nodes": {nid: n.to_dict() for nid, n in self.nodes.items()}
        }
