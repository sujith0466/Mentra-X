import logging
from typing import Dict, Any, List, Optional
from backend.services.privacy.data_classification import DataClassification, DataClassificationService

logger = logging.getLogger(__name__)

POLICY_CONFIG = {
    "default_retention_days": 30,
    "retention_rules": {
        "AssessmentSession": {"retention_days": 30, "field": "started_at", "status_filter": ["completed", "abandoned"]},
        "ContactMessage": {"retention_days": 90, "field": "created_at"},
    },
    "export_rules": {
        "allowed_classifications": [
            DataClassification.PUBLIC,
            DataClassification.INTERNAL,
            DataClassification.CONFIDENTIAL,
            DataClassification.PII,
            DataClassification.SENSITIVE_PII
        ],
        "include_models": ["User", "Enrollment", "QuizAttempt", "StudentTwinRecord"]
    },
    "deletion_rules": {
        "cascade_models": ["Enrollment", "QuizAttempt", "StudentTwinRecord", "UserXP"],
        "anonymize_fields": {
            "User": {
                "name": "Anonymized Student",
                "email_prefix": "anon_",
                "email_domain": "@mentra.research"
            }
        }
    },
    "consent_rules": {
        "required_for_storage": "SEMANTIC_MEMORY_STORAGE",
        "required_for_profiling": "BAYESIAN_PROFILING",
        "required_for_tutoring": "AI_TUTORING"
    }
}

class PrivacyDecision:
    def __init__(self, allowed: bool, reason: str, applied_rules: List[str], metadata: Optional[Dict[str, Any]] = None):
        self.allowed = allowed
        self.reason = reason
        self.applied_rules = applied_rules
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "allowed": self.allowed,
            "reason": self.reason,
            "applied_rules": self.applied_rules,
            "metadata": self.metadata
        }

class PrivacyPolicyEngine:
    """
    Centralized Privacy Policy Engine evaluating:
    Consent Rules -> Retention Rules -> Export Rules -> Deletion Rules -> Privacy Decision.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or POLICY_CONFIG

    def evaluate_consent_rule(self, user_id: int, consent_type: str, has_consent_bool: bool) -> PrivacyDecision:
        if has_consent_bool:
            return PrivacyDecision(True, f"Consent granted for {consent_type}", ["consent_rules"])
        return PrivacyDecision(False, f"Consent revoked or missing for {consent_type}", ["consent_rules"])

    def evaluate_retention_rule(self, model_name: str) -> Dict[str, Any]:
        return self.config.get("retention_rules", {}).get(model_name, {"retention_days": self.config.get("default_retention_days", 30)})

    def evaluate_export_rule(self, model_name: str, record_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Filters record attributes using data classification rules."""
        allowed = self.config.get("export_rules", {}).get("allowed_classifications", [])
        exportable = {}
        for k, v in record_dict.items():
            classif = DataClassificationService.get_field_classification(model_name, k)
            if classif in allowed:
                exportable[k] = v
        return exportable

    def evaluate_deletion_rule(self, model_name: str) -> Dict[str, Any]:
        return {"cascade": model_name in self.config.get("deletion_rules", {}).get("cascade_models", [])}

    def evaluate_operation(self, operation: str, user_id: int, context: Dict[str, Any]) -> PrivacyDecision:
        applied = []
        if "consent_type" in context:
            applied.append("consent_rules")
            if not context.get("has_consent", True):
                return PrivacyDecision(False, "Blocked by Consent Rules", applied)
        
        if operation == "EXPORT":
            applied.append("export_rules")
            return PrivacyDecision(True, "Export approved by Policy Engine", applied, {"models": self.config["export_rules"]["include_models"]})
        elif operation == "ERASE":
            applied.append("deletion_rules")
            return PrivacyDecision(True, "Erasure approved by Policy Engine", applied, {"cascade_models": self.config["deletion_rules"]["cascade_models"]})
        elif operation == "RETENTION":
            applied.append("retention_rules")
            return PrivacyDecision(True, "Retention enforced by Policy Engine", applied, self.config["retention_rules"])
            
        return PrivacyDecision(True, "Operation approved", applied)
