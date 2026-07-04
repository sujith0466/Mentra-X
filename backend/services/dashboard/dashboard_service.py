import logging
from typing import Dict, Any
from backend.services.dashboard.dashboard_aggregator import DashboardAggregator

logger = logging.getLogger(__name__)

class DashboardService:
    """
    Service layer facade for the Enterprise AI Operations Dashboard.
    Provides clean dictionary responses ready for REST API serialization and UI widget rendering.
    """

    @classmethod
    def get_overview_data(cls) -> Dict[str, Any]:
        try:
            return DashboardAggregator.get_overview().to_dict()
        except Exception as e:
            logger.error(f"Error in DashboardService.get_overview_data: {e}")
            return {}

    @classmethod
    def get_runtime_data(cls) -> Dict[str, Any]:
        try:
            return DashboardAggregator.get_runtime_health().to_dict()
        except Exception as e:
            logger.error(f"Error in DashboardService.get_runtime_data: {e}")
            return {}

    @classmethod
    def get_providers_data(cls) -> Dict[str, Any]:
        try:
            return DashboardAggregator.get_provider_metrics().to_dict()
        except Exception as e:
            logger.error(f"Error in DashboardService.get_providers_data: {e}")
            return {}

    @classmethod
    def get_prompts_data(cls) -> Dict[str, Any]:
        try:
            return DashboardAggregator.get_prompt_analytics().to_dict()
        except Exception as e:
            logger.error(f"Error in DashboardService.get_prompts_data: {e}")
            return {}

    @classmethod
    def get_evaluation_data(cls) -> Dict[str, Any]:
        try:
            qual = DashboardAggregator.get_ai_quality().to_dict()
            expl = DashboardAggregator.get_explainability_metrics().to_dict()
            return {
                "quality": qual,
                "explainability": expl
            }
        except Exception as e:
            logger.error(f"Error in DashboardService.get_evaluation_data: {e}")
            return {}

    @classmethod
    def get_privacy_data(cls) -> Dict[str, Any]:
        try:
            return DashboardAggregator.get_privacy_metrics().to_dict()
        except Exception as e:
            logger.error(f"Error in DashboardService.get_privacy_data: {e}")
            return {}

    @classmethod
    def get_observability_data(cls) -> Dict[str, Any]:
        try:
            return DashboardAggregator.get_observability_metrics().to_dict()
        except Exception as e:
            logger.error(f"Error in DashboardService.get_observability_data: {e}")
            return {}

    @classmethod
    def get_swarm_data(cls) -> Dict[str, Any]:
        try:
            return DashboardAggregator.get_swarm_status().to_dict()
        except Exception as e:
            logger.error(f"Error in DashboardService.get_swarm_data: {e}")
            return {}

    @classmethod
    def get_student_intelligence_data(cls) -> Dict[str, Any]:
        try:
            return DashboardAggregator.get_student_intelligence().to_dict()
        except Exception as e:
            logger.error(f"Error in DashboardService.get_student_intelligence_data: {e}")
            return {}
