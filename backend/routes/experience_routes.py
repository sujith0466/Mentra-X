"""
Experience Routes â€” Phase C

Blueprints for:
  POST /api/flashcards     â€” Feature 9: Notes -> Flashcards
  POST /api/doubt-solver   â€” Feature 10: AI Doubt Solver
  GET  /api/study-plan     â€” Feature 11: Study Planner
  GET  /api/streak         â€” Feature 12: Learning Streak
  GET  /api/xp             â€” Feature 12: XP System

These endpoints require an authenticated user to function correctly, though
some like flashcards and doubt solver are purely text-transforms.
"""

from flask import Blueprint, request, jsonify, session

experience_routes_bp = Blueprint(
    'experience_routes', __name__, url_prefix='/api'
)

def _get_user_id():
    return session.get('user_id')

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# POST /api/flashcards
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

@experience_routes_bp.route('/flashcards', methods=['POST'])
def create_flashcards():
    """
    Generate Q/A flashcards out of provided notes.
    Request JSON: {"notes_text": "..."}
    """
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    data = request.get_json(silent=True) or {}
    notes = data.get('notes_text', '')
    
    if not notes:
        return jsonify({'success': False, 'error': 'notes_text is required.'}), 400
        
    try:
        from services.learning.flashcard_generator import generate_flashcards
        cards = generate_flashcards(notes)
        return jsonify({'success': True, 'data': {'flashcards': cards}, 'flashcards': cards})
    except Exception as e:
        print(f"Error in /api/flashcards: {e}")
        return jsonify({'success': False, 'error': 'An error occurred generating flashcards.'}), 500

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# POST /api/doubt-solver
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

@experience_routes_bp.route('/doubt-solver', methods=['POST'])
def resolve_doubt():
    """
    Identify and resolve technical doubts using rule-based answering.
    Request JSON: {"question_text": "..."}
    """
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    data = request.get_json(silent=True) or {}
    question = data.get('question_text', '')
    
    if not question:
        return jsonify({'success': False, 'error': 'question_text is required.'}), 400
        
    try:
        from services.ai.doubt_solver import solve_doubt
        answer = solve_doubt(question)
        return jsonify({'success': True, 'data': answer, **answer})
    except Exception as e:
        print(f"Error in /api/doubt-solver: {e}")
        return jsonify({'success': False, 'error': 'An error occurred resolving doubt.'}), 500

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# GET /api/study-plan
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

@experience_routes_bp.route('/study-plan', methods=['GET'])
def study_plan():
    """
    Generate personalized daily tasks and weekly goals.
    """
    user_id = _get_user_id()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not logged in.'}), 401
    
    try:
        from services.learning.study_planner import generate_study_plan
        plan = generate_study_plan(user_id)
        return jsonify({'success': True, 'data': plan, **plan})
    except Exception as e:
        print(f"Error in /api/study-plan: {e}")
        return jsonify({'success': False, 'error': 'An error occurred creating study plan.'}), 500

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# GET /api/streak
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

@experience_routes_bp.route('/streak', methods=['GET'])
def get_streak():
    """
    Trigger a streak update matching today's date and return stats.
    """
    user_id = _get_user_id()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not logged in.'}), 401
        
    try:
        from services.learning.streak_xp import get_streak
        # Calling this will update if today is new, or just return max
        streak_data = get_streak(user_id)
        return jsonify({'success': True, 'data': {'streak': streak_data}, 'streak': streak_data})
    except Exception as e:
        print(f"Error in /api/streak: {e}")
        return jsonify({'success': False, 'error': 'An error occurred updating streak.'}), 500

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# GET /api/xp
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

@experience_routes_bp.route('/xp', methods=['GET'])
def get_xp():
    """
    Calculate and return the user's latest XP and Level dynamically.
    """
    user_id = _get_user_id()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not logged in.'}), 401
        
    try:
        from services.learning.streak_xp import calculate_xp
        xp_data = calculate_xp(user_id)
        return jsonify({'success': True, 'data': {'xp_data': xp_data}, 'xp_data': xp_data})
    except Exception as e:
        print(f"Error in /api/xp: {e}")
        return jsonify({'success': False, 'error': 'An error occurred calculating XP.'}), 500


