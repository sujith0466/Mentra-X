import logging
from functools import wraps
from flask import Blueprint, jsonify, session, current_app, request
from backend.services.dashboard import DashboardService

logger = logging.getLogger(__name__)

dashboard_bp = Blueprint('dashboard_bp', __name__)

def admin_required_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_app.config.get('TESTING'):
            if 'user_id' not in session and 'user' not in session:
                return jsonify({'status': 'error', 'message': 'Unauthorized. Authentication required.'}), 401
            try:
                from backend.models import User
                uid = session.get('user_id') or (session.get('user', {}).get('id') if isinstance(session.get('user'), dict) else None)
                user = User.query.get(uid) if uid else None
                if not user or getattr(user, 'role', '') != 'admin':
                    return jsonify({'status': 'error', 'message': 'Forbidden. Admin privileges required.'}), 403
            except Exception as e:
                logger.error(f"Error verifying admin role in API: {e}")
                return jsonify({'status': 'error', 'message': 'Forbidden. Admin privileges required.'}), 403
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route('/api/v1/dashboard/overview', methods=['GET'])
@admin_required_api
def get_dashboard_overview():
    """Returns aggregated executive overview telemetry for AI Operations command center."""
    data = DashboardService.get_overview_data()
    return jsonify({'status': 'success', 'data': data}), 200

@dashboard_bp.route('/api/v1/dashboard/runtime', methods=['GET'])
@admin_required_api
def get_dashboard_runtime():
    """Returns persistent runtime and component health status."""
    data = DashboardService.get_runtime_data()
    return jsonify({'status': 'success', 'data': data}), 200

@dashboard_bp.route('/api/v1/dashboard/providers', methods=['GET'])
@admin_required_api
def get_dashboard_providers():
    """Returns AI model provider performance comparisons and cost telemetry."""
    data = DashboardService.get_providers_data()
    return jsonify({'status': 'success', 'data': data}), 200

@dashboard_bp.route('/api/v1/dashboard/prompts', methods=['GET'])
@admin_required_api
def get_dashboard_prompts():
    """Returns versioned prompt analytics, governance status, and rollback readiness."""
    data = DashboardService.get_prompts_data()
    return jsonify({'status': 'success', 'data': data}), 200

@dashboard_bp.route('/api/v1/dashboard/evaluation', methods=['GET'])
@admin_required_api
def get_dashboard_evaluation():
    """Returns quality benchmark percentiles and explainability analytics."""
    data = DashboardService.get_evaluation_data()
    return jsonify({'status': 'success', 'data': data}), 200

@dashboard_bp.route('/api/v1/dashboard/privacy', methods=['GET'])
@admin_required_api
def get_dashboard_privacy():
    """Returns GDPR consent states, data subject rights operations, and retention metrics."""
    data = DashboardService.get_privacy_data()
    return jsonify({'status': 'success', 'data': data}), 200

@dashboard_bp.route('/api/v1/dashboard/observability', methods=['GET'])
@admin_required_api
def get_dashboard_observability():
    """Returns latency histograms, error rates, and OpenTelemetry trace metrics."""
    data = DashboardService.get_observability_data()
    return jsonify({'status': 'success', 'data': data}), 200

@dashboard_bp.route('/api/v1/dashboard/swarm', methods=['GET'])
@admin_required_api
def get_dashboard_swarm():
    """Returns Cognitive Swarm workflow execution states and event queue throughput."""
    data = DashboardService.get_swarm_data()
    return jsonify({'status': 'success', 'data': data}), 200

@dashboard_bp.route('/api/v1/dashboard/student_intelligence', methods=['GET'])
@admin_required_api
def get_dashboard_student_intelligence():
    """Returns aggregated student learning DNA and digital twin analytics (no PII)."""
    data = DashboardService.get_student_intelligence_data()
    return jsonify({'status': 'success', 'data': data}), 200
