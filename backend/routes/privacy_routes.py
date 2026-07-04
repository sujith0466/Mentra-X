import logging
from flask import Blueprint, request, jsonify, session
from backend.services.privacy.consent_service import ConsentService
from backend.services.privacy.privacy_service import PrivacyService
from backend.services.privacy.middleware import require_consent

logger = logging.getLogger(__name__)

privacy_bp = Blueprint("privacy_bp", __name__, url_prefix="/api/privacy")

def _get_user_id() -> int:
    uid = request.args.get("user_id") or request.headers.get("X-User-ID")
    if not uid and request.is_json and request.json:
        uid = request.json.get("user_id")
    if not uid:
        uid = session.get("user_id")
    if not uid:
        raise ValueError("user_id is required for privacy operations.")
    return int(uid)

@privacy_bp.route("/consent", methods=["GET"])
def get_user_consents():
    """Returns all explicit or default GDPR consent statuses for a user."""
    try:
        user_id = _get_user_id()
        consents = ConsentService.get_all_consents(user_id)
        return jsonify({"user_id": user_id, "consents": consents}), 200
    except ValueError as ve:
        return jsonify({"error": "Bad Request", "message": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error in get_user_consents: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@privacy_bp.route("/consent", methods=["PUT"])
def update_user_consent_route():
    """Updates a user's consent status for a specified consent_type."""
    try:
        user_id = _get_user_id()
        data = request.json or {}
        consent_type = data.get("consent_type")
        status = data.get("status")
        policy_version = data.get("policy_version", "1.0")
        ip_address = request.remote_addr

        if not consent_type or not status:
            return jsonify({"error": "Bad Request", "message": "consent_type and status are required."}), 400

        result = ConsentService.update_user_consent(
            user_id=user_id,
            consent_type=consent_type,
            status=status,
            ip_address=ip_address,
            policy_version=policy_version
        )
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": "Bad Request", "message": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error in update_user_consent_route: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@privacy_bp.route("/export", methods=["GET"])
def export_user_data_route():
    """GDPR Right to Access & Portability (Article 15 & 20). Returns user data export bundle."""
    try:
        user_id = _get_user_id()
        bundle = PrivacyService.export_user_data(user_id, ip_address=request.remote_addr)
        return jsonify(bundle), 200
    except ValueError as ve:
        return jsonify({"error": "Not Found", "message": str(ve)}), 404
    except Exception as e:
        logger.error(f"Error in export_user_data_route: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@privacy_bp.route("/erase", methods=["POST"])
def erase_user_data_route():
    """GDPR Right to Erasure / Right to Be Forgotten (Article 17). Executes data purge cascade."""
    try:
        user_id = _get_user_id()
        success = PrivacyService.erase_user_data(user_id, ip_address=request.remote_addr)
        if not success:
            return jsonify({"error": "Not Found", "message": f"User {user_id} not found."}), 404
        return jsonify({"message": "User account and all associated data have been permanently erased.", "user_id": user_id}), 200
    except ValueError as ve:
        return jsonify({"error": "Bad Request", "message": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error in erase_user_data_route: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@privacy_bp.route("/rectify", methods=["PUT"])
def rectify_user_data_route():
    """GDPR Right to Rectification (Article 16). Corrects inaccurate profile or twin profiling metrics."""
    try:
        user_id = _get_user_id()
        data = request.json or {}
        result = PrivacyService.rectify_user_data(user_id, data, ip_address=request.remote_addr)
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": "Not Found", "message": str(ve)}), 404
    except Exception as e:
        logger.error(f"Error in rectify_user_data_route: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@privacy_bp.route("/anonymize", methods=["POST"])
def anonymize_user_route():
    """Data minimization engine: replaces user PII with irreversible SHA-256 hashes."""
    try:
        user_id = _get_user_id()
        success = PrivacyService.anonymize_user(user_id, ip_address=request.remote_addr)
        if not success:
            return jsonify({"error": "Not Found", "message": f"User {user_id} not found."}), 404
        return jsonify({"message": f"User {user_id} has been anonymized successfully."}), 200
    except ValueError as ve:
        return jsonify({"error": "Bad Request", "message": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error in anonymize_user_route: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@privacy_bp.route("/retention/enforce", methods=["POST"])
def enforce_retention_route():
    """Triggers automated retention lifecycle enforcement (purges old assessment scratch-pads)."""
    try:
        res = PrivacyService.enforce_retention_policies()
        return jsonify(res), 200
    except Exception as e:
        logger.error(f"Error in enforce_retention_route: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@privacy_bp.route("/test-protected", methods=["GET"])
@require_consent("AI_TUTORING")
def test_protected_route():
    return "Access Granted", 200
