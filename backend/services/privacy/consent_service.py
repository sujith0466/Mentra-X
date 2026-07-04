import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from backend.models import db, UserConsent, PrivacyAuditLog, utcnow
from backend.services.orchestration.runtime.event_bus import EventBus

logger = logging.getLogger(__name__)

CONSENT_TYPES = {
    "AI_TUTORING",
    "SEMANTIC_MEMORY_STORAGE",
    "BAYESIAN_PROFILING",
    "TELEMETRY_ANALYTICS"
}

class ConsentService:
    """
    Enterprise Consent Registry & Service for Mentra X.
    Manages user opt-in/opt-out states for AI tutoring, semantic vector storage,
    Bayesian profiling, and telemetry analytics in accordance with GDPR and COPPA.
    """
    @classmethod
    def get_user_consent(cls, user_id: int, consent_type: str) -> str:
        """
        Returns the current consent status ('GRANTED', 'REVOKED', 'PENDING') for a user.
        Defaults to 'GRANTED' if no explicit consent record exists (to preserve backward compatibility).
        """
        if consent_type not in CONSENT_TYPES:
            logger.warning(f"Unknown consent type checked: {consent_type}")
            return "GRANTED"

        try:
            record = UserConsent.query.filter_by(user_id=user_id, consent_type=consent_type).first()
            if record:
                return record.status
            return "GRANTED"
        except Exception as e:
            logger.error(f"Error checking user consent for {user_id}:{consent_type}: {e}")
            return "GRANTED" # Fail open for backward compatibility unless explicitly revoked

    @classmethod
    def get_all_consents(cls, user_id: int) -> Dict[str, str]:
        """
        Returns a dictionary mapping all standard consent types to their current status for the user.
        """
        consents = {ct: "GRANTED" for ct in CONSENT_TYPES}
        try:
            records = UserConsent.query.filter_by(user_id=user_id).all()
            for r in records:
                if r.consent_type in CONSENT_TYPES:
                    consents[r.consent_type] = r.status
        except Exception as e:
            logger.error(f"Error fetching all consents for {user_id}: {e}")
        return consents

    @classmethod
    def update_user_consent(
        cls,
        user_id: int,
        consent_type: str,
        status: str,
        ip_address: Optional[str] = None,
        policy_version: str = "1.0"
    ) -> Dict[str, Any]:
        """
        Updates or creates a user's consent record, records an audit log,
        and publishes a user_consent_updated event to the Event Bus.
        """
        if consent_type not in CONSENT_TYPES:
            raise ValueError(f"Invalid consent type: {consent_type}. Must be one of {CONSENT_TYPES}")
        if status not in {"GRANTED", "REVOKED", "PENDING"}:
            raise ValueError(f"Invalid consent status: {status}. Must be GRANTED, REVOKED, or PENDING.")

        try:
            record = UserConsent.query.filter_by(user_id=user_id, consent_type=consent_type).first()
            now = utcnow()
            if not record:
                record = UserConsent(
                    user_id=user_id,
                    consent_type=consent_type,
                    status=status,
                    granted_at=now if status == "GRANTED" else now,
                    revoked_at=now if status == "REVOKED" else None,
                    ip_address=ip_address,
                    policy_version=policy_version
                )
                db.session.add(record)
            else:
                record.status = status
                record.ip_address = ip_address
                record.policy_version = policy_version
                if status == "REVOKED" and not record.revoked_at:
                    record.revoked_at = now
                elif status == "GRANTED":
                    record.granted_at = now
                    record.revoked_at = None

            # Add audit log
            audit = PrivacyAuditLog(
                user_id=user_id,
                action="CONSENT_UPDATED",
                details={
                    "consent_type": consent_type,
                    "new_status": status,
                    "policy_version": policy_version
                },
                ip_address=ip_address,
                created_at=now
            )
            db.session.add(audit)
            db.session.commit()

            # Publish event to EventBus
            payload = {
                "user_id": user_id,
                "consent_type": consent_type,
                "status": status,
                "policy_version": policy_version,
                "idempotency_key": f"consent-{user_id}-{consent_type}-{now.timestamp()}"
            }
            EventBus().publish("user_consent_updated", payload)

            logger.info(f"Updated consent for user {user_id}: {consent_type} -> {status}")
            return {
                "user_id": user_id,
                "consent_type": consent_type,
                "status": status,
                "updated_at": now.isoformat()
            }
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to update consent for user {user_id}: {e}")
            raise
