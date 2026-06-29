from flask import Blueprint, request, jsonify, session
from functools import wraps
from backend.services.assessment.assessment_facade import AssessmentFacade

assessment_bp = Blueprint('assessment', __name__, url_prefix='/api/v1/assessment')
facade = AssessmentFacade()

def login_required_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized', 'message': 'Please login first'}), 401
        return f(*args, **kwargs)
    return decorated_function

@assessment_bp.route('/start', methods=['POST'])
@login_required_api
def start_assessment():
    """
    Initializes a new adaptive assessment session.
    Expects JSON: {"exam_track": "JEE"}
    """
    data = request.get_json() or {}
    exam_track = data.get('exam_track')
    
    payload, status_code = facade.start(session['user_id'], exam_track)
    return jsonify(payload), status_code

@assessment_bp.route('/answer', methods=['POST'])
@login_required_api
def submit_answer():
    """
    Submits an answer and returns the next question or completion signal.
    """
    data = request.get_json() or {}
    session_id = data.get('session_id')
    question_id = data.get('question_id')
    submitted_answer = data.get('submitted_answer')
    current_difficulty = data.get('current_difficulty')
    
    payload, status_code = facade.answer(
        user_id=session['user_id'],
        session_id=session_id,
        question_id=question_id,
        submitted_answer=submitted_answer,
        current_difficulty=current_difficulty
    )
    return jsonify(payload), status_code

@assessment_bp.route('/complete', methods=['POST'])
@login_required_api
def complete_assessment():
    """
    Finalizes the session and computes Bayesian Knowledge State and Learning DNA.
    """
    data = request.get_json() or {}
    session_id = data.get('session_id')
    
    payload, status_code = facade.complete(session['user_id'], session_id)
    return jsonify(payload), status_code

@assessment_bp.route('/session/<session_id>', methods=['GET'])
@login_required_api
def get_session_status(session_id):
    """
    Retrieves the status of an ongoing session.
    """
    payload, status_code = facade.get_session(session['user_id'], session_id)
    return jsonify(payload), status_code
