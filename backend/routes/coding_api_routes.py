from flask import Blueprint, request, jsonify, session
from backend.services.coding.executor import execute_code
from backend.services.coding.test_runner import run_tests
from backend.models import CodingChallenge, CodingSubmission, db
from backend.services.mongo_service import safe_insert
from backend.services.learning.streak_xp import update_streak
from datetime import datetime, timezone

coding_api_bp = Blueprint('coding_api', __name__, url_prefix='/api')

@coding_api_bp.route('/run-code', methods=['POST'])
def api_run_code():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'error': 'Unauthorized'}), 401
        
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'error': 'Invalid payload'}), 400
        
    code = data.get('code', '')
    language = data.get('language', 'python')
    input_str = data.get('input', '')
    
    result = execute_code(language, code, input_str)
    
    return jsonify({
        'status': 'success' if result['success'] else 'error',
        'output': result['output'],
        'error': result['error']
    })

@coding_api_bp.route('/submit-code', methods=['POST'])
def api_submit_code():
    if 'user_id' not in session:
         return jsonify({'status': 'error', 'error': 'Unauthorized'}), 401
         
    data = request.get_json()
    if not data:
         return jsonify({'status': 'error', 'error': 'Invalid payload'}), 400
         
    user_id = session.get('user_id')
    problem_id = data.get('problem_id')
    code = data.get('code', '')
    language = data.get('language', 'python')
    
    challenge = CodingChallenge.query.get(problem_id)
    if not challenge:
        return jsonify({'status': 'error', 'error': 'Challenge not found'}), 404
        
    test_cases = challenge.get_test_cases()
    evaluation = run_tests(code, language, test_cases)
    
    # Save to coding_submissions table
    submission = CodingSubmission(
        user_id=user_id,
        challenge_id=problem_id,
        code_submitted=code,
        execution_output=evaluation.get('execution_output') or evaluation.get('error') or '',
        passed_tests=int(evaluation.get('passed_tests') or 0),
        score=float(evaluation.get('score') or 0.0),
        submitted_at=datetime.utcnow()
    )
    db.session.add(submission)
    
    # Update skills
    from services.ai.coding.coding_challenge_service import update_skill_progress_for_challenge
    if evaluation.get('score', 0) > 0:
        update_skill_progress_for_challenge(user_id, challenge, evaluation['score'])
        
    db.session.commit()
    update_streak(user_id)

    # MongoDB Logging for extended fields
    safe_insert("coding_logs", {
        "user_id": user_id,
        "challenge_id": challenge.id,
        "language": language,
        "action": "submit",
        "passed_tests": evaluation.get("passed_tests", 0),
        "score": evaluation.get("score", 0),
        "error": evaluation.get("error")
    })
    
    return jsonify({
        'status': 'success',
        'passed_tests': evaluation['passed_tests'],
        'total_tests': evaluation['total_tests'],
        'score': evaluation['score'],
        'output': evaluation.get('execution_output') or '',
        'error': evaluation.get('error') or '',
        'results': evaluation.get('results', [])
    })


