from datetime import datetime
from backend.models import db, StudentTwinRecord, TwinMutationLogRecord, TwinKnowledgeStateRecord, utcnow

def mutate_knowledge(user_id: int, concept: str, new_score: float, mutation_type: str, agent_name: str = "System"):
    """
    Mutates a specific concept in the Twin Knowledge State, increments the version, 
    and logs the delta in TwinMutationLogRecord with optimistic locking logic via version increment.
    """
    twin = db.session.query(StudentTwinRecord).filter_by(user_id=user_id).with_for_update().first()
    if not twin:
        return False
        
    ks = db.session.query(TwinKnowledgeStateRecord).filter_by(twin_id=twin.id, concept_id=concept).first()
    old_val = 0.0
    if not ks:
        ks = TwinKnowledgeStateRecord(
            twin_id=twin.id,
            concept_id=concept,
            mastery_score=new_score,
            last_reviewed=utcnow()
        )
        db.session.add(ks)
    else:
        old_val = ks.mastery_score
        ks.mastery_score = new_score
        ks.last_reviewed = utcnow()
        
    twin.twin_version += 1
    twin.updated_at = utcnow()
    
    log = TwinMutationLogRecord(
        user_id=user_id,
        twin_version=twin.twin_version,
        mutation_type=mutation_type,
        concept=concept,
        field_changed="mastery_score",
        old_value=str(old_val),
        new_value=str(new_score),
        agent_name=agent_name
    )
    db.session.add(log)
    db.session.commit()
    
    # Optionally update health
    from backend.services.twin.twin_health import compute_and_store_health
    compute_and_store_health(twin.id)
    return True

def mutate_learning_dna(user_id: int, new_dna: dict, mutation_type: str, agent_name: str = "System"):
    """
    Mutates the learning DNA of the twin.
    """
    twin = db.session.query(StudentTwinRecord).filter_by(user_id=user_id).with_for_update().first()
    if not twin:
        return False
        
    import json
    old_val = twin.learning_dna
    twin.learning_dna = json.dumps(new_dna) if isinstance(new_dna, dict) else new_dna
    twin.twin_version += 1
    twin.updated_at = utcnow()
    
    log = TwinMutationLogRecord(
        user_id=user_id,
        twin_version=twin.twin_version,
        mutation_type=mutation_type,
        concept="learning_dna",
        field_changed="learning_dna",
        old_value=old_val,
        new_value=json.dumps(new_dna),
        agent_name=agent_name
    )
    db.session.add(log)
    db.session.commit()
    return True
