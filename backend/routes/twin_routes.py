from flask import Blueprint, jsonify, session
from functools import wraps
from backend.models import db, StudentTwinRecord, TwinKnowledgeStateRecord
from backend.services.twin.twin_builder import build_initial_twin
from backend.services.twin.twin_health import compute_and_store_health
import json

twin_bp = Blueprint('twin', __name__, url_prefix='/api/v1/twin')

def login_required_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized', 'message': 'Please login first'}), 401
        return f(*args, **kwargs)
    return decorated_function

@twin_bp.route('/initialize', methods=['POST'])
@login_required_api
def initialize_twin():
    user_id = session['user_id']
    try:
        twin = build_initial_twin(user_id, "JEE")
        return jsonify({
            'status': 'success',
            'twin_id': twin.id,
            'twin_status': twin.twin_status,
            'twin_version': twin.twin_version
        }), 200
    except Exception as e:
        return jsonify({'error': 'Initialization Failed', 'message': str(e)}), 500

@twin_bp.route('/profile', methods=['GET'])
@login_required_api
def get_twin_profile():
    user_id = session['user_id']
    twin = db.session.query(StudentTwinRecord).filter_by(user_id=user_id).first()
    if not twin:
        return jsonify({'error': 'Not Found', 'message': 'Twin not initialized'}), 404
        
    return jsonify({
        'twin_id': twin.id,
        'twin_version': twin.twin_version,
        'twin_status': twin.twin_status,
        'twin_health': twin.twin_health,
        'exam_track': twin.exam_track,
        'academic_state': json.loads(twin.academic_state) if twin.academic_state else {},
        'skill_state': json.loads(twin.skill_state) if twin.skill_state else {},
        'learning_dna': json.loads(twin.learning_dna) if twin.learning_dna else {},
        'career_state': json.loads(twin.career_state) if twin.career_state else {},
        'project_state': json.loads(twin.project_state) if twin.project_state else {},
        'opportunity_state': json.loads(twin.opportunity_state) if twin.opportunity_state else {},
    }), 200

@twin_bp.route('/health', methods=['GET'])
@login_required_api
def get_twin_health():
    user_id = session['user_id']
    twin = db.session.query(StudentTwinRecord).filter_by(user_id=user_id).first()
    if not twin:
        return jsonify({'error': 'Not Found', 'message': 'Twin not initialized'}), 404
        
    health = compute_and_store_health(twin.id)
    return jsonify({
        'twin_id': twin.id,
        'twin_health': health
    }), 200

@twin_bp.route('/dashboard', methods=['GET'])
@login_required_api
def get_twin_dashboard():
    user_id = session['user_id']
    twin = db.session.query(StudentTwinRecord).filter_by(user_id=user_id).first()
    if not twin:
        return jsonify({'error': 'Not Found', 'message': 'Twin not initialized'}), 404
        
    dna = json.loads(twin.learning_dna) if twin.learning_dna else {}
    
    # Calculate weak concepts
    weak_concept_count = 0
    knowledge = db.session.query(TwinKnowledgeStateRecord).filter_by(twin_id=twin.id).all()
    for k in knowledge:
        if k.mastery_score < 0.5:
            weak_concept_count += 1
            
    return jsonify({
        'twin_status': twin.twin_status,
        'twin_health': twin.twin_health,
        'twin_version': twin.twin_version,
        'learning_dna_summary': dna.get('preferred_style', 'Assessing...'),
        'weak_concept_count': weak_concept_count,
        'last_updated': twin.updated_at.isoformat() if twin.updated_at else None
    }), 200
