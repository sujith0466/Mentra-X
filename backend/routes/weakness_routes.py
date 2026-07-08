"""
Mentra X — Weakness Intelligence API Routes (Phase 8 Milestone 4)

Provides enterprise REST endpoints for retrieving student weakness/strength profiles,
pre-test vulnerability scans, misconception taxonomy reports, multi-step remediation plans,
and closed-loop verification mutations.
"""

import logging
from flask import Blueprint, jsonify, request, current_app
from backend.services.adaptive.weakness_diagnostic_engine import WeaknessDiagnosticEngine
from backend.services.adaptive.vulnerability_engine import VulnerabilityEngine
from backend.services.adaptive.remediation_engine import RemediationEngine

logger = logging.getLogger(__name__)

weakness_bp = Blueprint("weakness", __name__, url_prefix="/api/weakness")

_diag_engine = WeaknessDiagnosticEngine()
_vuln_engine = VulnerabilityEngine(_diag_engine)
_rem_engine = RemediationEngine(_diag_engine, _vuln_engine)


@weakness_bp.route("/profile/<int:user_id>", methods=["GET"])
def get_weakness_profile(user_id):
    """
    Retrieves the complete Weakness Intelligence Profile for a student,
    including diagnosed weaknesses, strength intelligence, confidence scores, and timelines.
    """
    try:
        profile = _diag_engine.diagnose_student(user_id)
        return jsonify({
            "status": "success",
            "profile": profile.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error fetching weakness profile for user {user_id}: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@weakness_bp.route("/vulnerabilities/<int:user_id>/<int:quiz_id>", methods=["GET"])
def scan_quiz_vulnerabilities(user_id, quiz_id):
    """
    Executes a pre-test vulnerability scan before a student attempts a quiz.
    Returns vulnerable concepts and recommended warm-up drills if high-risk gaps exist.
    """
    try:
        scan_report = _vuln_engine.scan_vulnerabilities_before_quiz(user_id, quiz_id)
        return jsonify({
            "status": "success",
            "vulnerability_scan": scan_report
        }), 200
    except Exception as e:
        logger.error(f"Error executing vulnerability scan for user {user_id}, quiz {quiz_id}: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@weakness_bp.route("/misconceptions/<int:user_id>", methods=["GET"])
def get_student_misconceptions(user_id):
    """
    Retrieves student's historical misconception reports mapped to standard pedagogy taxonomy.
    """
    try:
        reports = _vuln_engine.get_student_misconceptions(user_id)
        return jsonify({
            "status": "success",
            "misconception_reports": reports
        }), 200
    except Exception as e:
        logger.error(f"Error fetching misconceptions for user {user_id}: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@weakness_bp.route("/remediation/<int:user_id>/<concept_id>", methods=["GET"])
def get_remediation_plan(user_id, concept_id):
    """
    Generates or retrieves a structured 4-step remediation plan for a specific concept weakness.
    """
    try:
        plan = _rem_engine.generate_remediation_plan(user_id, concept_id)
        return jsonify({
            "status": "success",
            "remediation_plan": plan
        }), 200
    except Exception as e:
        logger.error(f"Error generating remediation plan for user {user_id}, concept {concept_id}: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@weakness_bp.route("/remediation/quiz/<int:user_id>/<concept_id>", methods=["POST"])
def generate_remediation_quiz(user_id, concept_id):
    """
    Generates a customized diagnostic drill tailored to cure the student's misconception taxonomy.
    """
    try:
        quiz = _rem_engine.generate_custom_quiz(user_id, concept_id)
        return jsonify({
            "status": "success",
            "custom_quiz": quiz
        }), 200
    except Exception as e:
        logger.error(f"Error generating remediation quiz for user {user_id}, concept {concept_id}: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@weakness_bp.route("/remediation/verify", methods=["POST"])
def verify_remediation():
    """
    Executes closed-loop verification. Mutates Digital Twin mastery upon successful verification.
    Expected JSON payload: {"user_id": int, "concept_id": str, "passed": bool, "new_score": float}
    """
    try:
        data = request.get_json(force=True) or {}
        user_id = int(data.get("user_id", 0))
        concept_id = str(data.get("concept_id", ""))
        passed = bool(data.get("passed", False))
        new_score = float(data.get("new_score", 0.80 if passed else 0.50))

        if not user_id or not concept_id:
            return jsonify({"status": "error", "message": "Missing user_id or concept_id"}), 400

        success = _rem_engine.verify_remediation_completion(user_id, concept_id, passed, new_score)
        return jsonify({
            "status": "success",
            "verified": success,
            "outcome": "VERIFIED_RECOVERY" if passed else "RETRY_REQUIRED",
            "updated_score": new_score
        }), 200
    except Exception as e:
        logger.error(f"Error verifying remediation: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
