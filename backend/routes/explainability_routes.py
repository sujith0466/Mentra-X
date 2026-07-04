import logging
from functools import wraps
from flask import Blueprint, jsonify, session, current_app, request
from backend.services.explainability.explanation_service import ExplanationService
from backend.services.evaluation.evaluation_engine import EvaluationEngine
from backend.services.evaluation.evaluation_report import EvaluationReportGenerator

logger = logging.getLogger(__name__)

explainability_bp = Blueprint('explainability_bp', __name__)

def login_required_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_app.config.get('TESTING') and 'user_id' not in session and 'user' not in session:
            return jsonify({'status': 'error', 'message': 'Unauthorized. Authentication required.'}), 401
        return f(*args, **kwargs)
    return decorated_function

@explainability_bp.route('/api/explainability/workflow/<workflow_id>', methods=['GET'])
@login_required_api
def get_workflow_explanation(workflow_id: str):
    """Returns safe user-facing explainability summary without exposing raw chain-of-thought."""
    data = ExplanationService.get_explanation(workflow_id)
    if not data:
        return jsonify({'status': 'error', 'message': f'No explainability record found for workflow {workflow_id}'}), 404
    return jsonify({'status': 'success', 'data': data}), 200

@explainability_bp.route('/api/explainability/decision_graph/<workflow_id>', methods=['GET'])
@login_required_api
def get_workflow_decision_graph(workflow_id: str):
    """Returns the Directed Acyclic Graph (DAG) representation of the workflow execution."""
    data = ExplanationService.get_explanation(workflow_id)
    if not data or not data.get("decision_graph"):
        return jsonify({'status': 'error', 'message': f'Decision graph not available for workflow {workflow_id}'}), 404
    return jsonify({'status': 'success', 'decision_graph': data["decision_graph"]}), 200

@explainability_bp.route('/api/explainability/evaluation/<workflow_id>', methods=['GET'])
@login_required_api
def get_workflow_evaluations(workflow_id: str):
    """Returns evaluation metrics (faithfulness, hallucination, latency, safety, cost) for the workflow."""
    evals = EvaluationEngine.get_evaluations(workflow_id)
    if not evals:
        return jsonify({'status': 'error', 'message': f'No evaluations found for workflow {workflow_id}'}), 404
    return jsonify({'status': 'success', 'workflow_id': workflow_id, 'evaluations': evals}), 200

@explainability_bp.route('/api/explainability/citations/<workflow_id>', methods=['GET'])
@login_required_api
def get_workflow_citations(workflow_id: str):
    """Returns structured citations to Student Twin facts, Assessment records, and Qdrant memory."""
    data = ExplanationService.get_explanation(workflow_id)
    if not data or "citations" not in data:
        return jsonify({'status': 'error', 'message': f'No citations found for workflow {workflow_id}'}), 404
    return jsonify({'status': 'success', 'workflow_id': workflow_id, 'citations': data["citations"]}), 200

@explainability_bp.route('/api/explainability/report', methods=['GET'])
@login_required_api
def get_evaluation_report():
    """Returns aggregated statistical evaluation reports across workflows and providers."""
    wf_id = request.args.get('workflow_id')
    prov = request.args.get('provider')
    ver = request.args.get('prompt_version')
    report = EvaluationReportGenerator.generate_report(workflow_id=wf_id, provider=prov, prompt_version=ver)
    return jsonify({'status': 'success', 'report': report}), 200
