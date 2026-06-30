from backend.models import db, StudentTwinRecord, TwinKnowledgeStateRecord

def compute_and_store_health(twin_id: int) -> float:
    """
    Computes a composite TwinHealthScore from modular states
    and stores it in the twin record.
    """
    twin = StudentTwinRecord.query.get(twin_id)
    if not twin:
        return 0.0
        
    knowledge_states = db.session.query(TwinKnowledgeStateRecord).filter_by(twin_id=twin_id).all()
    if not knowledge_states:
        health = 0.5 # Default starting health if no data
    else:
        coverage = len([k for k in knowledge_states if k.mastery_score > 0.6]) / len(knowledge_states)
        avg_mastery = sum([k.mastery_score for k in knowledge_states]) / len(knowledge_states)
        
        # Simple Phase-1 composite formula
        health = (coverage * 0.4) + (avg_mastery * 0.6)
        
    twin.twin_health = round(health, 2)
    db.session.commit()
    return twin.twin_health
