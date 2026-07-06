"""
Mentra X — Adaptive Learning Intelligence Package (Phase 6 Layer 6)

This package contains the core intelligence engines for:
- Pedagogical level selection & avoidance constraint evaluation (TutorDecisionEngine)
- Real-time learning style inference (LearningStyleDetector)
- Level-templated LLM prompt construction (DynamicPromptBuilder)
- Unifying tool execution bundle (PersonalizationEngine)
- Dynamic curriculum sequencing & study velocity planning (DynamicRoadmapGenerator, GoalPlanner)
- Study material ranking & prerequisite dependency evaluation (ContentRankingEngine, PrerequisiteEngine)
- Real-time incremental hints & Socratic guiding feedback (ProgressiveHintEngine, SocraticFeedbackEngine)
- Cognitive fatigue detection & Ebbinghaus spaced repetition scheduling (FatigueDetector, SpacedRepetitionScheduler)
- Unified multi-service recommendation feed generation (UnifiedRecommendationEngine)
"""

from .dto import PersonalizationBundleDTO, TutorDecisionDTO, AvoidanceConstraintsDTO
from .tutor_decision_engine import TutorDecisionEngine
from .learning_style_detector import LearningStyleDetector
from .dynamic_prompt_builder import DynamicPromptBuilder
from .personalization_engine import PersonalizationEngine
from .path_optimizer import DynamicRoadmapGenerator, LessonProjectionDTO
from .goal_planner import GoalPlanner
from .content_selector import ContentRankingEngine, RankedResourceDTO
from .prerequisite_engine import PrerequisiteEngine
from .feedback_engine import ProgressiveHintEngine, ProgressiveHintDTO, SocraticFeedbackEngine, SocraticFeedbackDTO
from .pacing_engine import FatigueDetector, FatigueStatusDTO, SpacedRepetitionScheduler, ReviewScheduleDTO
from .recommendation_engine import UnifiedRecommendationEngine, UnifiedRecommendationFeedDTO, ActionableRecommendationDTO

__all__ = [
    "PersonalizationBundleDTO",
    "TutorDecisionDTO",
    "AvoidanceConstraintsDTO",
    "TutorDecisionEngine",
    "LearningStyleDetector",
    "DynamicPromptBuilder",
    "PersonalizationEngine",
    "DynamicRoadmapGenerator",
    "LessonProjectionDTO",
    "GoalPlanner",
    "ContentRankingEngine",
    "RankedResourceDTO",
    "PrerequisiteEngine",
    "ProgressiveHintEngine",
    "ProgressiveHintDTO",
    "SocraticFeedbackEngine",
    "SocraticFeedbackDTO",
    "FatigueDetector",
    "FatigueStatusDTO",
    "SpacedRepetitionScheduler",
    "ReviewScheduleDTO",
    "UnifiedRecommendationEngine",
    "UnifiedRecommendationFeedDTO",
    "ActionableRecommendationDTO"
]
