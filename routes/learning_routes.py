"""
Learning Routes — Phase B

Blueprints for:
  GET /api/learning-path   — Smart Learning Path 2.0 (Feature 6)
  GET /api/weekly-report   — Weekly AI Report        (Feature 7)

These are JSON-only API endpoints that require an authenticated session.
"""

from flask import Blueprint, jsonify, session

learning_routes_bp = Blueprint(
    'learning_intelligence', __name__, url_prefix='/api'
)


def _require_user():
    """Return user_id from session or None."""
    return session.get('user_id')


# ───────────────────────────────────────────────────────────────
# GET /api/learning-path
# ───────────────────────────────────────────────────────────────

@learning_routes_bp.route('/learning-path', methods=['GET'])
def learning_path():
    """
    Generate a personalised learning path for the logged-in student.

    Response JSON:
        {
            "success": true,
            "next_courses": [{"title": "...", "reason": "..."}, ...],
            "difficulty": "easy|medium|hard",
            "estimated_time": "X weeks",
            "completed_courses": int,
            "average_progress": float,
            "known_skills": [str, ...]
        }
    """
    user_id = _require_user()
    if not user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required. Please log in.'
        }), 401

    try:
        from services.learning.path_generator import generate_learning_path
        result = generate_learning_path(user_id)

        # Optional: log to MongoDB
        try:
            from services.mongo_service import safe_insert
            safe_insert('learning_path_log', {
                'user_id': user_id,
                'difficulty': result['difficulty'],
                'suggestions_count': len(result['next_courses']),
            })
        except Exception:
            pass

        return jsonify({
            'success': True,
            'data': result,
            **result,
        })

    except Exception as e:
        print(f"Error in /api/learning-path: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while generating the learning path.'
        }), 500


# ───────────────────────────────────────────────────────────────
# GET /api/weekly-report
# ───────────────────────────────────────────────────────────────

@learning_routes_bp.route('/weekly-report', methods=['GET'])
def weekly_report():
    """
    Generate a weekly AI learning report for the logged-in student.

    Response JSON:
        {
            "success": true,
            "summary": "...",
            "course_progress": [...],
            "coding_activity": {...},
            "quiz_activity": {...},
            "lessons_completed": int,
            "weak_topics": [str, ...],
            "recommendations": [str, ...],
            "streak_days": int,
            "generated_at": "ISO timestamp"
        }
    """
    user_id = _require_user()
    if not user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required. Please log in.'
        }), 401

    try:
        from services.learning.weekly_report import generate_weekly_report
        result = generate_weekly_report(user_id)

        # Optional: log to MongoDB
        try:
            from services.mongo_service import safe_insert
            safe_insert('weekly_report_log', {
                'user_id': user_id,
                'weak_topics_count': len(result['weak_topics']),
                'recommendations_count': len(result['recommendations']),
            })
        except Exception:
            pass

        return jsonify({
            'success': True,
            'data': result,
            **result,
        })

    except Exception as e:
        print(f"Error in /api/weekly-report: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while generating the weekly report.'
        }), 500



@learning_routes_bp.route('/dashboard/overview', methods=['GET'])
def dashboard_overview():
    """
    Unified dashboard data API that aggregates core learning + career context.
    """
    user_id = _require_user()
    if not user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required. Please log in.'
        }), 401

    try:
        from services.career.job_score import calculate_score
        from services.learning.path_generator import generate_learning_path
        from services.learning.weekly_report import generate_weekly_report
        from services.learning.streak_xp import get_streak, calculate_xp

        overview = {
            'job_score': calculate_score(user_id),
            'learning_path': generate_learning_path(user_id),
            'weekly_report': generate_weekly_report(user_id),
            'streak': get_streak(user_id),
            'xp': calculate_xp(user_id),
        }
        return jsonify({
            'success': True,
            'data': overview,
            **overview,
        })
    except Exception as e:
        print(f"Error in /api/dashboard/overview: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while preparing dashboard overview.'
        }), 500
