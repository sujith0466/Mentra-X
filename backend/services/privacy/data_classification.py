import logging
from enum import Enum
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class DataClassification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    PII = "PII"
    SENSITIVE_PII = "SENSITIVE_PII"

# Central registry of data models and their attribute classifications
MODEL_DATA_CLASSIFICATIONS: Dict[str, Dict[str, DataClassification]] = {
    "User": {
        "id": DataClassification.PUBLIC,
        "name": DataClassification.PII,
        "email": DataClassification.PII,
        "password": DataClassification.SENSITIVE_PII,
        "password_hash": DataClassification.SENSITIVE_PII,
        "role": DataClassification.PUBLIC,
        "wallet_balance": DataClassification.CONFIDENTIAL,
        "referral_code": DataClassification.INTERNAL,
        "created_at": DataClassification.INTERNAL,
    },
    "Enrollment": {
        "id": DataClassification.PUBLIC,
        "user_id": DataClassification.INTERNAL,
        "course_id": DataClassification.PUBLIC,
        "progress": DataClassification.CONFIDENTIAL,
        "enrolled_date": DataClassification.INTERNAL,
    },
    "QuizAttempt": {
        "id": DataClassification.PUBLIC,
        "user_id": DataClassification.INTERNAL,
        "quiz_id": DataClassification.PUBLIC,
        "score_percentage": DataClassification.CONFIDENTIAL,
        "passed": DataClassification.CONFIDENTIAL,
        "submitted_at": DataClassification.INTERNAL,
    },
    "StudentTwinRecord": {
        "id": DataClassification.PUBLIC,
        "user_id": DataClassification.INTERNAL,
        "twin_version": DataClassification.INTERNAL,
        "learning_dna": DataClassification.SENSITIVE_PII,
        "academic_state": DataClassification.CONFIDENTIAL,
        "skill_state": DataClassification.CONFIDENTIAL,
        "career_state": DataClassification.CONFIDENTIAL,
        "updated_at": DataClassification.INTERNAL,
    },
    "AssessmentSession": {
        "id": DataClassification.PUBLIC,
        "session_id": DataClassification.INTERNAL,
        "user_id": DataClassification.INTERNAL,
        "exam_track": DataClassification.INTERNAL,
        "status": DataClassification.INTERNAL,
        "started_at": DataClassification.INTERNAL,
    }
}

class DataClassificationService:
    """
    Centralized Data Classification Service.
    Maps attributes to classification tiers (PUBLIC, INTERNAL, CONFIDENTIAL, PII, SENSITIVE_PII)
    and provides data masking and redaction capabilities.
    """
    @classmethod
    def get_field_classification(cls, model_name: str, field_name: str) -> DataClassification:
        return MODEL_DATA_CLASSIFICATIONS.get(model_name, {}).get(field_name, DataClassification.INTERNAL)

    @classmethod
    def get_fields_by_classification(cls, model_name: str, classification: DataClassification) -> List[str]:
        mapping = MODEL_DATA_CLASSIFICATIONS.get(model_name, {})
        return [field for field, classif in mapping.items() if classif == classification]

    @classmethod
    def mask_dict_by_classification(
        cls,
        model_name: str,
        data: Dict[str, Any],
        max_allowed_level: DataClassification = DataClassification.CONFIDENTIAL
    ) -> Dict[str, Any]:
        """
        Masks or redacts fields exceeding the max_allowed_level.
        """
        levels = [
            DataClassification.PUBLIC,
            DataClassification.INTERNAL,
            DataClassification.CONFIDENTIAL,
            DataClassification.PII,
            DataClassification.SENSITIVE_PII
        ]
        max_idx = levels.index(max_allowed_level) if max_allowed_level in levels else 2
        
        result = {}
        for k, v in data.items():
            classif = cls.get_field_classification(model_name, k)
            classif_idx = levels.index(classif) if classif in levels else 1
            if classif_idx > max_idx:
                result[k] = "[REDACTED]"
            else:
                result[k] = v
        return result
