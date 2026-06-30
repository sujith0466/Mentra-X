from datetime import datetime, timezone
from flask import request, session
from backend.models import db, AuditLog


def log_audit(entity_type, action_type, entity_id=None, before=None, after=None, metadata=None, actor_id=None, actor_role=None):
    """Best-effort immutable audit logger."""
    try:
        resolved_actor_id = actor_id if actor_id is not None else session.get('user_id')
        resolved_actor_role = actor_role if actor_role is not None else session.get('admin_role')
        extra_metadata = dict(metadata or {})
        if request:
            extra_metadata.setdefault('path', request.path)
            extra_metadata.setdefault('method', request.method)
            extra_metadata.setdefault('ip', request.headers.get('X-Forwarded-For', request.remote_addr))
            extra_metadata.setdefault('user_agent', request.user_agent.string if request.user_agent else None)

        log = AuditLog(
            entity_type=entity_type,
            entity_id=entity_id,
            action_type=action_type,
            actor_id=resolved_actor_id,
            actor_role=resolved_actor_role,
            created_at=datetime.utcnow(),
        )
        log.set_before(before)
        log.set_after(after)
        log.set_metadata(extra_metadata)

        db.session.add(log)
        db.session.commit()
        return True
    except Exception as exc:
        db.session.rollback()
        print(f"Audit logging failed: {exc}")
        return False
