from datetime import datetime

from flask import Blueprint, request, jsonify, session

from backend.services.ai.interview_service import generate_questions, evaluate_answer
from backend.services.mongo_service import safe_insert

interview_api_bp = Blueprint('interview_api_bp', __name__, url_prefix='/api/interview')


def _unauthorized():
    return jsonify({'success': False, 'error': 'Unauthorized'}), 401


def _bad_request(message: str):
    return jsonify({'success': False, 'error': message}), 400


@interview_api_bp.route('/start', methods=['POST'])
def start_interview():
    """Starts a new interview session and returns generated questions."""
    if 'user_id' not in session:
        return _unauthorized()

    data = request.get_json(silent=True) or {}
    role = data.get('role', 'backend')

    questions = generate_questions(role)

    session['interview_state'] = {
        'role': role,
        'started_at': datetime.utcnow().isoformat(),
        'questions': questions,
        'evaluations': [],
        'total_questions': len(questions),
    }

    public_questions = [
        {'id': q['id'], 'type': q['type'], 'question': q['question']}
        for q in questions
    ]

    payload = {
        'message': f'Interview started for role: {role}',
        'questions': public_questions,
        'total_questions': len(public_questions),
    }
    return jsonify({
        'success': True,
        'data': payload,
        'status': 'success',
        **payload,
    })


@interview_api_bp.route('/answer', methods=['POST'])
def submit_answer():
    """Evaluates a single answer and stores the result in the session."""
    if 'user_id' not in session:
        return _unauthorized()

    state = session.get('interview_state')
    if not state:
        return _bad_request('No active interview session found. Please start an interview first.')

    data = request.get_json(silent=True) or {}
    question_index = data.get('question_index')
    user_answer = data.get('answer', '')

    try:
        question_index = int(question_index)
    except (TypeError, ValueError):
        return _bad_request('Invalid question_index provided.')

    if question_index < 0 or question_index >= state['total_questions']:
        return _bad_request(f'Question index {question_index} out of bounds.')

    questions = state['questions']
    target_q = questions[question_index]

    if any(e['id'] == target_q['id'] for e in state['evaluations']):
        return _bad_request(f'You have already answered question {question_index}.')

    eval_result = evaluate_answer(target_q, user_answer)

    evaluation_record = {
        'id': target_q['id'],
        'question': target_q['question'],
        'answer': user_answer,
        'score': eval_result['score'],
        'feedback': eval_result['feedback'],
        'improvement': eval_result['improvement'],
    }

    state['evaluations'].append(evaluation_record)
    session['interview_state'] = state
    session.modified = True

    result_payload = {
        'score': eval_result['score'],
        'feedback': eval_result['feedback'],
        'improvement': eval_result['improvement'],
    }
    return jsonify({
        'success': True,
        'data': {'result': result_payload},
        'status': 'success',
        'result': result_payload,
    })


@interview_api_bp.route('/complete', methods=['POST'])
def complete_interview():
    """Completes the interview, averages score, logs summary, and clears session."""
    if 'user_id' not in session:
        return _unauthorized()

    state = session.get('interview_state')
    user_id = session.get('user_id')

    if not state:
        return _bad_request('No active interview session to complete.')

    evals = state['evaluations']
    if not evals:
        return _bad_request('No questions were answered.')

    total_score = sum(e['score'] for e in evals)
    avg_score = round(total_score / len(evals), 1)

    summary = {
        'role': state['role'],
        'started_at': state['started_at'],
        'completed_at': datetime.utcnow().isoformat(),
        'final_score': avg_score,
        'total_answered': len(evals),
        'total_questions': state['total_questions'],
        'evaluations': evals,
    }

    try:
        safe_insert('interview_sessions', {
            'user_id': user_id,
            'role': summary['role'],
            'final_score': summary['final_score'],
            'total_answered': summary['total_answered'],
            'evaluations_count': len(summary['evaluations']),
        })
    except Exception as exc:
        print(f'Failed to log to MongoDB: {exc}')

    session.pop('interview_state', None)

    return jsonify({
        'success': True,
        'data': {'summary': summary},
        'status': 'success',
        'summary': summary,
    })
