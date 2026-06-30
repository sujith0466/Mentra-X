from qdrant_client.http.models import Distance

class CollectionRegistry:
    # Defaulting to 384 dimensions for BAAI/bge-small-en-v1.5
    VECTOR_DIMENSION = 384
    DISTANCE_METRIC = Distance.COSINE
    
    COLLECTIONS = {
        "learning_dna": {
            "version": "1.0",
            "dimension": VECTOR_DIMENSION,
            "distance": DISTANCE_METRIC,
            "description": "Behavioral fingerprint per student (1 document/student)"
        },
        "past_doubts": {
            "version": "1.0",
            "dimension": VECTOR_DIMENSION,
            "distance": DISTANCE_METRIC,
            "description": "Semantic store of every question a student has ever asked"
        },
        "explanation_history": {
            "version": "1.0",
            "dimension": VECTOR_DIMENSION,
            "distance": DISTANCE_METRIC,
            "description": "Tracks successful and failed teaching approaches"
        },
        "session_logs": {
            "version": "1.0",
            "dimension": VECTOR_DIMENSION,
            "distance": DISTANCE_METRIC,
            "description": "Raw transcripts of tutoring/assessment sessions"
        },
        "weak_concepts": {
            "version": "1.0",
            "dimension": VECTOR_DIMENSION,
            "distance": DISTANCE_METRIC,
            "description": "Synthesized macro-weaknesses"
        }
    }
    
    @classmethod
    def get_all_collections(cls):
        return cls.COLLECTIONS
