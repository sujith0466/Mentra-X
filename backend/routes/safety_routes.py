"""
Mentra X — Enkrypt Safety Layer REST Routes (Phase 7 Layer 6)

Exposes endpoints for manual safety evaluation, enterprise audit metrics,
intercept logging retrieval, and Human-In-The-Loop (HITL) queue management.
"""

import logging
from flask import Blueprint, request, jsonify
from backend.services.enkrypt.enkrypt_validator import EnkryptValidator
from backend.services.enkrypt.safety_monitor import safety_monitor

logger = logging.getLogger(__name__)

safety_bp = Blueprint("safety_bp", __name__, url_prefix="/api/safety")
validator = EnkryptValidator()


@safety_bp.route("/evaluate", methods=["POST"])
def evaluate_text():
    """
    Manually evaluates text through the 4-pipeline Enkrypt audit.
    Logs intercept events and queues HITL review for hard failures.
    """
    try:
        data = request.get_json() or {}
        text = str(data.get("text", ""))
        subject = str(data.get("subject", "physics"))
        track = str(data.get("exam_track", "JEE"))
        level = int(data.get("level", 1))
        session_id = str(data.get("session_id", "rest_session"))
        user_id = str(data.get("user_id", "rest_user"))

        res = validator.validate(text=text, subject_tag=subject, exam_track=track, level=level)
        
        safety_monitor.log_intercept(
            session_id=session_id,
            user_id=user_id,
            original_output=text,
            result=res,
            final_output=text if res.recommended_action == "APPROVE" else "",
            regeneration_count=0,
            hitl_flagged=(res.recommended_action == "HARD_FAIL")
        )

        if res.recommended_action == "HARD_FAIL":
            safety_monitor.queue_hitl(
                session_id=session_id,
                user_id=user_id,
                concept="general",
                original_query=text[:100],
                failed_output=text,
                scores={
                    "math": res.math_score,
                    "science": res.science_score,
                    "hallucination": res.hallucination_score,
                    "pedagogy": res.pedagogy_score,
                    "composite": res.composite_confidence
                }
            )

        return jsonify({"status": "success", "validation_result": res.to_dict()}), 200
    except Exception as e:
        logger.error(f"Error in evaluate_text: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@safety_bp.route("/metrics", methods=["GET"])
def get_metrics():
    """
    Returns enterprise safety metrics across all intercepts.
    """
    try:
        metrics = safety_monitor.get_metrics()
        return jsonify({"status": "success", "metrics": metrics}), 200
    except Exception as e:
        logger.error(f"Error in get_metrics: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@safety_bp.route("/intercepts", methods=["GET"])
def get_intercepts():
    """
    Returns recent intercept logs.
    """
    try:
        limit = int(request.args.get("limit", 50))
        logs = safety_monitor.get_intercepts(limit=limit)
        return jsonify({"status": "success", "intercepts": logs}), 200
    except Exception as e:
        logger.error(f"Error in get_intercepts: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@safety_bp.route("/hitl_queue", methods=["GET"])
def get_hitl_queue():
    """
    Returns HITL queue items filtered by status.
    """
    try:
        status = request.args.get("status", "pending")
        items = safety_monitor.get_hitl_queue(status=status)
        return jsonify({"status": "success", "hitl_queue": items}), 200
    except Exception as e:
        logger.error(f"Error in get_hitl_queue: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@safety_bp.route("/hitl_resolve/<int:item_id>", methods=["POST"])
def resolve_hitl(item_id):
    """
    Resolves an HITL queue item.
    """
    try:
        data = request.get_json() or {}
        notes = str(data.get("reviewer_notes", ""))
        status = str(data.get("status", "resolved"))

        success = safety_monitor.resolve_hitl_item(item_id=item_id, reviewer_notes=notes, status=status)
        if success:
            return jsonify({"status": "success", "message": f"HITL item {item_id} resolved."}), 200
        else:
            return jsonify({"status": "error", "message": f"HITL item {item_id} not found."}), 404
    except Exception as e:
        logger.error(f"Error in resolve_hitl: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
