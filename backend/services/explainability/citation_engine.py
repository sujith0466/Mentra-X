import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class Citation:
    """Represents a structured source citation supporting an AI response."""
    def __init__(
        self,
        source_type: str, # TWIN_FACT, ASSESSMENT_RECORD, MEMORY_ENTRY, LEARNING_CONCEPT
        reference_id: str,
        snippet: str,
        relevance_score: float = 0.90,
        url_or_path: Optional[str] = None
    ):
        self.source_type = source_type
        self.reference_id = str(reference_id)
        self.snippet = snippet
        self.relevance_score = round(max(0.0, min(1.0, relevance_score)), 2)
        self.url_or_path = url_or_path or f"internal://{source_type.lower()}/{self.reference_id}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_type": self.source_type,
            "reference_id": self.reference_id,
            "snippet": self.snippet,
            "relevance_score": self.relevance_score,
            "url_or_path": self.url_or_path
        }


class CitationEngine:
    """
    Compiles structured citations referencing Student Twin facts, Assessment records,
    Qdrant Memory entries, and Learning concepts to ground AI responses.
    """
    def __init__(self):
        self._citations: List[Citation] = []

    def add_citation(
        self,
        source_type: str,
        reference_id: str,
        snippet: str,
        relevance_score: float = 0.90,
        url_or_path: Optional[str] = None
    ) -> Citation:
        cit = Citation(
            source_type=source_type,
            reference_id=reference_id,
            snippet=snippet,
            relevance_score=relevance_score,
            url_or_path=url_or_path
        )
        self._citations.append(cit)
        return cit

    def extract_from_workflow_context(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Automatically extracts citations from workflow context or memory/twin results."""
        # Check memories
        memories = context.get("retrieved_memories") or context.get("memories", [])
        for idx, mem in enumerate(memories):
            if isinstance(mem, dict):
                ref_id = mem.get("id") or f"mem-{idx}"
                snippet = mem.get("content") or mem.get("text") or "Retrieved semantic memory item"
                score = float(mem.get("score") or mem.get("relevance", 0.85))
                self.add_citation("MEMORY_ENTRY", str(ref_id), str(snippet)[:150], score)

        # Check Twin facts
        twin_data = context.get("twin_state") or context.get("student_twin")
        if isinstance(twin_data, dict):
            user_id = twin_data.get("user_id", "current")
            learning_style = twin_data.get("learning_style", "general")
            self.add_citation(
                "TWIN_FACT",
                f"twin-{user_id}",
                f"Student learning style identified as {learning_style}.",
                0.95
            )

        # Check Assessment records
        assessments = context.get("assessment_results") or context.get("quiz_data", [])
        for idx, ass in enumerate(assessments):
            if isinstance(ass, dict):
                ass_id = ass.get("quiz_id") or ass.get("assessment_id") or f"ass-{idx}"
                score = ass.get("score", 0)
                self.add_citation(
                    "ASSESSMENT_RECORD",
                    str(ass_id),
                    f"Assessment attempt completed with score: {score}%.",
                    0.90
                )

        return self.to_list()

    def to_list(self) -> List[Dict[str, Any]]:
        return [c.to_dict() for c in self._citations]
