"""
Mentra X — Autonomous Learning Intelligence Routes (Phase 9)

Exposes REST API endpoints for:
- GET /api/v1/autonomous/overview
- GET /api/v1/autonomous/mission
- GET /api/v1/autonomous/schedule
- GET /api/v1/autonomous/revisions
- GET /api/v1/autonomous/habits
- GET /api/v1/autonomous/interventions
- GET /api/v1/autonomous/predictions
- POST /api/v1/autonomous/mission/complete
"""

from flask import Blueprint, jsonify, request, session
from functools import wraps
from backend.services.autonomous.autonomous_facade import AutonomousLearningFacade

autonomous_bp = Blueprint('autonomous', __name__, url_prefix='/api/v1/autonomous')
facade = AutonomousLearningFacade()


def get_current_user_id():
    user_id = session.get('user_id')
    if not user_id:
        user_id = request.args.get('student_id', type=int)
    if not user_id and request.is_json:
        user_id = request.json.get('user_id') or request.json.get('student_id')
    return user_id or 1  # default demo student ID for seamless offline/dev mode


@autonomous_bp.route('/overview', methods=['GET'])
def get_autonomous_overview():
    user_id = get_current_user_id()
    result = facade.get_autonomous_overview(user_id)
    if result.get("success"):
        return jsonify(result), 200
    return jsonify(result), 500


@autonomous_bp.route('/mission', methods=['GET'])
def get_mission():
    user_id = get_current_user_id()
    result = facade.get_autonomous_overview(user_id)
    if result.get("success"):
        return jsonify({"success": True, "data": result["data"]["daily_mission"]}), 200
    return jsonify(result), 500


@autonomous_bp.route('/schedule', methods=['GET'])
def get_schedule():
    user_id = get_current_user_id()
    result = facade.get_autonomous_overview(user_id)
    if result.get("success"):
        return jsonify({"success": True, "data": result["data"]["adaptive_schedule"]}), 200
    return jsonify(result), 500


@autonomous_bp.route('/revisions', methods=['GET'])
def get_revisions():
    user_id = get_current_user_id()
    result = facade.get_autonomous_overview(user_id)
    if result.get("success"):
        return jsonify({"success": True, "data": result["data"]["revision_queue"]}), 200
    return jsonify(result), 500


@autonomous_bp.route('/habits', methods=['GET'])
def get_habits():
    user_id = get_current_user_id()
    result = facade.get_autonomous_overview(user_id)
    if result.get("success"):
        return jsonify({"success": True, "data": result["data"]["habit_insight"]}), 200
    return jsonify(result), 500


@autonomous_bp.route('/interventions', methods=['GET'])
def get_interventions():
    user_id = get_current_user_id()
    result = facade.get_autonomous_overview(user_id)
    if result.get("success"):
        return jsonify({"success": True, "data": result["data"]["active_interventions"]}), 200
    return jsonify(result), 500


@autonomous_bp.route('/predictions', methods=['GET'])
def get_predictions():
    user_id = get_current_user_id()
    result = facade.get_autonomous_overview(user_id)
    if result.get("success"):
        return jsonify({"success": True, "data": result["data"]["success_forecast"]}), 200
    return jsonify(result), 500


@autonomous_bp.route('/mission/complete', methods=['POST'])
def complete_mission():
    user_id = get_current_user_id()
    task_id = request.json.get('task_id', '') if request.is_json else ''
    result = facade.complete_mission_task(user_id, task_id)
    return jsonify(result), 200
