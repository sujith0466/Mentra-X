"""
Mentra X — Opportunity Intelligence REST API Blueprint (Phase 10)

Exposes endpoints under `/api/v1/opportunity/*`:
  • GET  /api/v1/opportunity/overview
  • GET  /api/v1/opportunity/feed
  • GET  /api/v1/opportunity/timeline
  • POST /api/v1/opportunity/status
"""

from flask import Blueprint, jsonify, request
from backend.services.opportunity.opportunity_brain import OpportunityIntelligenceBrain

opportunity_bp = Blueprint("opportunity_bp", __name__, url_prefix="/api/v1/opportunity")
_opportunity_brain = OpportunityIntelligenceBrain()


def _get_current_user_id() -> int:
    # Check JWT or fallback to default authenticated student 1
    uid = request.args.get("user_id", type=int)
    if uid:
        return uid
    return 1


@opportunity_bp.route("/overview", methods=["GET"])
def get_opportunity_overview():
    try:
        user_id = _get_current_user_id()
        overview = _opportunity_brain.get_opportunity_overview(user_id)
        return jsonify({
            "status": "success",
            "data": overview.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@opportunity_bp.route("/feed", methods=["GET"])
def get_opportunity_feed():
    try:
        user_id = _get_current_user_id()
        overview = _opportunity_brain.get_opportunity_overview(user_id)
        return jsonify({
            "status": "success",
            "data": [item.to_dict() for item in overview.recommended_feed]
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@opportunity_bp.route("/timeline", methods=["GET"])
def get_opportunity_timeline():
    try:
        user_id = _get_current_user_id()
        overview = _opportunity_brain.get_opportunity_overview(user_id)
        return jsonify({
            "status": "success",
            "data": [item.to_dict() for item in overview.timeline]
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@opportunity_bp.route("/status", methods=["POST"])
def update_opportunity_status():
    try:
        payload = request.get_json(silent=True) or {}
        user_id = int(payload.get("user_id", _get_current_user_id()))
        opportunity_id = str(payload.get("opportunity_id", ""))
        new_status = str(payload.get("status", "SAVED"))

        if not opportunity_id:
            return jsonify({
                "status": "error",
                "message": "opportunity_id is required"
            }), 400

        entry = _opportunity_brain.update_opportunity_status(
            user_id=user_id,
            opportunity_id=opportunity_id,
            new_status=new_status
        )
        return jsonify({
            "status": "success",
            "data": entry.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
