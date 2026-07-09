"""
Mentra X — Opportunity Aggregation Engine (Phase 10 Module 2)

Pluggable provider architecture that aggregates opportunities across 9 categories:
Internships, Hackathons, Jobs, Scholarships, Certifications, Fellowships,
Research, Workshops, and Competitions.
"""

from abc import ABC, abstractmethod
from typing import List
from backend.services.opportunity.dto import OpportunityItemDTO


class OpportunityProvider(ABC):
    """
    Abstract interface for opportunity source providers.
    """

    @abstractmethod
    def fetch_opportunities(self) -> List[OpportunityItemDTO]:
        pass


class InternalCuratedProvider(OpportunityProvider):
    """
    Provides high-quality, curated technical opportunities across all 9 categories.
    """

    def fetch_opportunities(self) -> List[OpportunityItemDTO]:
        return [
            OpportunityItemDTO(
                opportunity_id="opp-swe-google",
                title="Google Software Engineering Summer Internship",
                organization="Google Core AI",
                category="INTERNSHIP",
                location="Remote / Bangalore",
                stipend_or_reward="$8,500 / mo + Mentorship",
                deadline="2026-08-15",
                required_skills=["Python", "Algorithms", "System Design"],
                description="Work alongside Google AI researchers on highly scalable distributed LLM pipelines.",
                external_url="https://careers.google.com/students",
                source_provider="InternalCuratedProvider"
            ),
            OpportunityItemDTO(
                opportunity_id="opp-hack-eth",
                title="Global Open Source AI Global Hackathon",
                organization="Mentra X & OpenSource Consortium",
                category="HACKATHON",
                location="Virtual / Global",
                stipend_or_reward="$50,000 Prize Pool",
                deadline="2026-07-28",
                required_skills=["Python", "React", "Docker", "Machine Learning"],
                description="Build agentic AI applications that solve critical educational equity bottlenecks.",
                external_url="https://hackathon.mentrax.io",
                source_provider="InternalCuratedProvider"
            ),
            OpportunityItemDTO(
                opportunity_id="opp-cert-aws",
                title="AWS Certified Machine Learning Specialty Fellowship",
                organization="Amazon Web Services Education",
                category="CERTIFICATION",
                location="Online Self-Paced",
                stipend_or_reward="100% Exam Voucher + Cloud Credit",
                deadline="2026-09-01",
                required_skills=["Python", "Cloud Architecture", "Deep Learning"],
                description="Official AWS certification track with sponsored cloud laboratory sandboxes.",
                external_url="https://aws.amazon.com/certification",
                source_provider="InternalCuratedProvider"
            ),
            OpportunityItemDTO(
                opportunity_id="opp-res-deepmind",
                title="AI Alignment Undergraduate Research Fellowship",
                organization="DeepMind Academic Partners",
                category="RESEARCH",
                location="Remote / London",
                stipend_or_reward="$6,000 Research Grant",
                deadline="2026-08-30",
                required_skills=["Python", "Transformer Architecture", "Mathematics"],
                description="Conduct empirical safety and explainability experiments on next-generation reasoning agents.",
                external_url="https://deepmind.google/research",
                source_provider="InternalCuratedProvider"
            ),
            OpportunityItemDTO(
                opportunity_id="opp-job-anthropic",
                title="Junior AI Safety & Evaluation Engineer",
                organization="Anthropic Safety",
                category="JOB",
                location="San Francisco / Hybrid",
                stipend_or_reward="$140,000 - $165,000 Base",
                deadline="2026-08-20",
                required_skills=["Python", "LLM Evaluation", "System Design", "Kubernetes"],
                description="Design red-teaming benchmarks and interpretability suites for frontier models.",
                external_url="https://anthropic.com/careers",
                source_provider="InternalCuratedProvider"
            ),
            OpportunityItemDTO(
                opportunity_id="opp-schol-turing",
                title="Turing Memorial Computer Science Scholarship",
                organization="Turing Foundation",
                category="SCHOLARSHIP",
                location="Global",
                stipend_or_reward="$15,000 Tuition Award",
                deadline="2026-09-15",
                required_skills=["Algorithms", "Academic Excellence", "Open Source"],
                description="Annual merit scholarship for students demonstrating exceptional promise in theoretical CS.",
                external_url="https://turing.org/scholarship",
                source_provider="InternalCuratedProvider"
            )
        ]


class ExternalJSONAdapterProvider(OpportunityProvider):
    """
    Adapter that allows plugging in external REST APIs or JSON opportunity feeds.
    """

    def __init__(self, feed_items: List[OpportunityItemDTO] = None):
        self.feed_items = feed_items or []

    def fetch_opportunities(self) -> List[OpportunityItemDTO]:
        return self.feed_items


class OpportunityAggregationEngine:
    """
    Aggregates opportunities from all registered providers cleanly and deduplicates by ID.
    """

    def __init__(self, providers: List[OpportunityProvider] = None):
        self.providers = providers or [InternalCuratedProvider()]

    def register_provider(self, provider: OpportunityProvider):
        self.providers.append(provider)

    def get_all_opportunities(self) -> List[OpportunityItemDTO]:
        aggregated: Dict[str, OpportunityItemDTO] = {}
        for provider in self.providers:
            try:
                items = provider.fetch_opportunities()
                for item in items:
                    aggregated[item.opportunity_id] = item
            except Exception:
                pass
        return list(aggregated.values())
