import logging
from functools import wraps
from flask import Blueprint, request, jsonify, session

from backend.services.memory.memory_facade import MemoryFacade
from backend.services.memory.memory_dtos import MemoryRetrieveRequest, MemoryStoreRequest, MemoryRetrieveResponse, MemoryStoreResponse
from backend.services.memory.qdrant_client import MemoryClient
from backend.services.memory.embedding_provider import get_embedding_provider
from backend.services.memory.collection_schema import CollectionRegistry

logger = logging.getLogger(__name__)

memory_bp = Blueprint('memory_bp', __name__)
facade = MemoryFacade()

def login_required_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@memory_bp.route('/api/v1/memory/health', methods=['GET'])
@login_required_api
def get_memory_health():
    """Verify Qdrant connectivity and embedding readiness."""
    qdrant_healthy = MemoryClient.check_health()
    try:
        # Check embedding provider instantiation (Local triggers download on first run)
        _ = get_embedding_provider()
        embeddings_ready = True
    except Exception as e:
        logger.error(f"Embedding provider health check failed: {e}")
        embeddings_ready = False
        
    if not qdrant_healthy or not embeddings_ready:
        return jsonify({
            "status": "error",
            "message": "MEMORY_QDRANT_UNAVAILABLE" if not qdrant_healthy else "MEMORY_EMBEDDING_FAILED",
            "qdrant": qdrant_healthy,
            "embeddings": embeddings_ready
        }), 503

    return jsonify({"status": "success", "message": "Memory layer healthy", "qdrant": True, "embeddings": True}), 200

@memory_bp.route('/api/v1/memory/status', methods=['GET'])
@login_required_api
def get_memory_status():
    """Returns the current collections and schema configuration."""
    return jsonify({
        "status": "success",
        "collections": CollectionRegistry.get_all_collections()
    }), 200

@memory_bp.route('/api/v1/memory/retrieve', methods=['POST'])
@login_required_api
def retrieve_memory():
    """Retrieves top-k relevant memories strictly isolated by user_id."""
    user_id = session.get('user_id')
    
    try:
        data = request.get_json() or {}
        req_dto = MemoryRetrieveRequest.from_dict(data)
    except ValueError as e:
        error_msg = str(e)
        return jsonify({"status": "error", "message": error_msg}), 400

    try:
        results = facade.retrieve_context(
            collection_name=req_dto.collection_name,
            query_text=req_dto.query_text,
            user_id=user_id,
            limit=req_dto.limit
        )
        response = MemoryRetrieveResponse(results=results)
        return jsonify({"status": "success", "data": response.to_dict()}), 200
        
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Retrieve memory error: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@memory_bp.route('/api/v1/memory/store', methods=['POST'])
@login_required_api
def store_memory():
    """Stores a semantic point in the relevant collection."""
    user_id = session.get('user_id')
    
    try:
        data = request.get_json() or {}
        req_dto = MemoryStoreRequest.from_dict(data)
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    try:
        # Route to appropriate mutator method
        if req_dto.memory_type == "learning_dna":
            facade.store_learning_dna(user_id, req_dto.twin_version, req_dto.text, req_dto.extra_data)
        elif req_dto.memory_type == "past_doubt":
            facade.store_doubt(user_id, req_dto.twin_version, req_dto.text, req_dto.extra_data)
        elif req_dto.memory_type == "explanation_history":
            success_flag = req_dto.extra_data.pop("success_flag", False)
            facade.store_explanation(user_id, req_dto.twin_version, req_dto.text, success_flag, req_dto.extra_data)
        elif req_dto.memory_type == "session_log":
            facade.store_session(user_id, req_dto.twin_version, req_dto.text, req_dto.extra_data)
        elif req_dto.memory_type == "weak_concept":
            severity = float(req_dto.extra_data.pop("severity_score", 0.5))
            facade.store_weak_concept(user_id, req_dto.twin_version, req_dto.text, severity, req_dto.extra_data)

        resp = MemoryStoreResponse(status="success", message=f"{req_dto.memory_type} stored successfully.")
        return jsonify(resp.to_dict()), 201

    except Exception as e:
        logger.error(f"Store memory error: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
