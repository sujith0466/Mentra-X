"""
AI Enhancements Routes — Phase B

Blueprints for:
  POST /api/coding-hint     — Real-Time Coding Hints (Feature 5)
  POST /api/improve-resume  — AI Resume Improver     (Feature 8)

These are JSON-only API endpoints, independent of existing routes.
"""

from flask import Blueprint, request, jsonify, session

ai_enhancements_bp = Blueprint(
    'ai_enhancements', __name__, url_prefix='/api'
)


# ───────────────────────────────────────────────────────────────
# POST /api/coding-hint
# ───────────────────────────────────────────────────────────────

@ai_enhancements_bp.route('/coding-hint', methods=['POST'])
def coding_hint():
    """
    Analyse submitted code and return educational hints.

    Request JSON:
        {
            "code": "for i in range(10)\\n  print(i)",
            "language": "python"          # optional, default: python
        }

    Response JSON:
        {
            "success": true,
            "hints": ["...", "..."],
            "language": "python",
            "total_hints": 2
        }
    """
    # Auth check (soft — allow unauthenticated for demo, but log user_id)
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            'success': False,
            'error': 'Invalid JSON payload. Send {"code": "...", "language": "python"}.'
        }), 400

    code = (data.get('code') or '').strip()
    language = (data.get('language') or 'python').strip()

    if not code:
        return jsonify({
            'success': False,
            'error': 'Code cannot be empty.'
        }), 400

    try:
        from services.ai.coding_hints import generate_hint
        result = generate_hint(code, language)

        # Optional: log to MongoDB
        try:
            from services.mongo_service import safe_insert
            safe_insert('coding_hints_log', {
                'user_id': session.get('user_id'),
                'language': language,
                'total_hints': result['total_hints'],
            })
        except Exception:
            pass  # Mongo is optional

        return jsonify({
            'success': True,
            'data': result,
            **result,
        })

    except Exception as e:
        print(f"Error in /api/coding-hint: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while generating hints.'
        }), 500


# ───────────────────────────────────────────────────────────────
# POST /api/improve-resume
# ───────────────────────────────────────────────────────────────

@ai_enhancements_bp.route('/improve-resume', methods=['POST'])
def improve_resume_api():
    """
    Improve resume text with better phrasing and suggestions.

    Request JSON:
        {
            "resume_text": "I worked on many projects..."
        }

    Response JSON:
        {
            "success": true,
            "improved_text": "...",
            "suggestions": ["...", "..."],
            "sections_found": [...],
            "sections_missing": [...],
            "weak_phrases_replaced": 3
        }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            'success': False,
            'error': 'Invalid JSON payload. Send {"resume_text": "..."}.'
        }), 400

    resume_text = (data.get('resume_text') or '').strip()
    if not resume_text:
        return jsonify({
            'success': False,
            'error': 'resume_text cannot be empty.'
        }), 400

    try:
        from services.career.resume_improver import improve_resume
        result = improve_resume(resume_text)

        # Optional: log to MongoDB
        try:
            from services.mongo_service import safe_insert
            safe_insert('resume_improver_log', {
                'user_id': session.get('user_id'),
                'weak_phrases_replaced': result['weak_phrases_replaced'],
                'sections_missing': result['sections_missing'],
            })
        except Exception:
            pass

        return jsonify({
            'success': True,
            'data': result,
            **result,
        })

    except Exception as e:
        print(f"Error in /api/improve-resume: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while improving the resume.'
        }), 500
