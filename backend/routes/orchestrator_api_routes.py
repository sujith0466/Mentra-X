"""
REST API endpoint for the Multi-Agent Orchestrator.

POST /api/orchestrator
{
    "message": "I have a Python error",
    "context": {
        "page": "dashboard",
        "course": "Flask Fullstack",
        "domain": "Web Development"
    }
}
"""
from flask import Blueprint, request, jsonify, session
from backend.services.ai.orchestrator import route_to_agent, detect_intent, get_available_agents
from backend.services.career.job_score import calculate_score

orchestrator_api_bp = Blueprint('orchestrator_api', __name__, url_prefix='/api')


def _success(data: dict, **legacy):
    payload = {'success': True, 'data': data}
    payload.update(legacy)
    return jsonify(payload)


def _error(message: str, status: int = 400):
    return jsonify({'success': False, 'error': message}), status


def _run_orchestrator(message: str, context: dict | None):
    context = context or {}
    payload = route_to_agent(
        message,
        user_id=session.get('user_id'),
        current_page=context.get('page'),
        course_name=context.get('course'),
        domain=context.get('domain'),
    )
    agent = payload.get('agent', 'mentor')
    return {
        'answer': payload.get('response', ''),
        'agent': agent,
        'agent_label': payload.get('agent_label', 'Mentor AI'),
        'intent': payload.get('intent', 'general'),
        'suggestions': payload.get('suggestions', []),
        'meta': payload.get('data', {}),
        'next_action': payload.get('next_action'),
        'priority': payload.get('priority', 'medium'),
    }


@orchestrator_api_bp.route('/orchestrator', methods=['POST'])
def api_orchestrator():
    """Route a user message through the multi-agent orchestrator."""
    if 'user_id' not in session:
        return _error('Unauthorized', 401)

    data = request.get_json(silent=True) or {}
    message = (data.get('message') or '').strip()
    if not message:
        return _error('Message is required', 400)

    chat_data = _run_orchestrator(message, data.get('context') or {})
    return _success(
        chat_data,
        status='success',
        agent=chat_data['agent'],
        agent_label=chat_data['agent_label'],
        intent=chat_data['intent'],
        response=chat_data['answer'],
        suggestions=chat_data['suggestions'],
        answer=chat_data['answer'],
        meta=chat_data.get('meta', {}),
        next_action=chat_data.get('next_action'),
        priority=chat_data.get('priority', 'medium'),
    )


@orchestrator_api_bp.route('/chat', methods=['POST'])
def api_chat():
    """Unified chat endpoint backed by the orchestrator."""
    if 'user_id' not in session:
        return _error('Unauthorized', 401)

    data = request.get_json(silent=True) or {}
    message = (data.get('message') or data.get('question') or '').strip()
    if not message:
        return _error('Message is required', 400)

    context = data.get('context')
    if not isinstance(context, dict):
        context = {
            'page': data.get('current_page'),
            'course': data.get('course_name'),
            'domain': data.get('domain'),
        }

    chat_data = _run_orchestrator(message, context)
    return _success(chat_data, deprecated_routes=['/api/chatbot', '/api/chatbot/ask'])


@orchestrator_api_bp.route('/orchestrator/detect-intent', methods=['POST'])
def api_detect_intent():
    """Lightweight endpoint that only returns the detected intent/agent."""
    data = request.get_json(silent=True) or {}
    message = (data.get('message') or '').strip()
    if not message:
        return _error('Message is required', 400)

    intent = detect_intent(message)
    return _success({'intent': intent, 'message': message}, status='success', intent=intent, message=message)


@orchestrator_api_bp.route('/orchestrator/agents', methods=['GET'])
def api_list_agents():
    """Return metadata for all registered agents."""
    agents = get_available_agents()
    return _success({'agents': agents}, status='success', agents=agents)


@orchestrator_api_bp.route('/job-score', methods=['GET'])
def api_job_score():
    """Return Mentra score for the authenticated user."""
    if 'user_id' not in session:
        return _error('Unauthorized', 401)

    score_payload = calculate_score(session['user_id'])
    return _success(score_payload, **score_payload)
