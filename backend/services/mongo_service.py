from flask import current_app
from datetime import datetime, timezone
import os


_logged_unavailable_once = False


def _is_mongo_enabled():
    return os.getenv("MENTRA_USE_MONGO", "false").strip().lower() == "true"


def get_mongo_db():
    if hasattr(current_app, "mongo_db"):
        return current_app.mongo_db
    return None


def get_collections():
    db = get_mongo_db()
    if db is None:
        return None

    return {
        "chat_logs": db["chat_logs"],
        "learning_insights": db["learning_insights"],
        "project_ideas": db["project_ideas"],
        "debug_logs": db["debug_logs"],
        "coding_logs": db["coding_logs"],
        "learning_path_log": db["learning_path_log"],
        "weekly_report_log": db["weekly_report_log"],
        "coding_hints_log": db["coding_hints_log"],
        "resume_improver_log": db["resume_improver_log"],
        "orchestrator_logs": db["orchestrator_logs"],
        "interview_sessions": db["interview_sessions"],
        "misconception_reports": db["misconception_reports"],
        "vulnerability_scans": db["vulnerability_scans"],
        "ai_reasoning_logs": db["ai_reasoning_logs"],
        "remediation_plans": db["remediation_plans"],
        "remediation_quizzes": db["remediation_quizzes"],
    }


def safe_insert(collection_name, data):
    """
    Safely inserts data into a MongoDB collection.
    Automatically appends 'created_at' if not present.
    """
    global _logged_unavailable_once

    try:
        # If Mongo support is turned off, skip silently.
        if not _is_mongo_enabled():
            return False

        collections = get_collections()
        if not collections:
            # Mongo is enabled, but not connected: log only once to avoid noise.
            if not _logged_unavailable_once:
                current_app.logger.warning("MongoDB unavailable; optional logging inserts are being skipped.")
                _logged_unavailable_once = True
            return False

        if collection_name not in collections:
            current_app.logger.warning("Mongo insert skipped: disallowed collection '%s'", collection_name)
            return False

        collection = collections[collection_name]

        if "created_at" not in data:
            data["created_at"] = datetime.utcnow()

        collection.insert_one(data)
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return True
    except Exception as e:
        current_app.logger.warning("Mongo insert failed for %s: %s", collection_name, e)
        return False


def safe_find(collection_name, query=None, limit=50, sort_by="created_at", sort_order=-1):
    """
    Safely retrieves documents from a MongoDB collection.
    Returns empty list if Mongo is disabled or unavailable.
    """
    try:
        if not _is_mongo_enabled():
            return []
        collections = get_collections()
        if not collections or collection_name not in collections:
            return []
        collection = collections[collection_name]
        cursor = collection.find(query or {}).sort(sort_by, sort_order).limit(limit)
        results = []
        for doc in cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            if "created_at" in doc and hasattr(doc["created_at"], "isoformat"):
                doc["created_at"] = doc["created_at"].isoformat()
            results.append(doc)
        return results
    except Exception as e:
        current_app.logger.warning("Mongo find failed for %s: %s", collection_name, e)
        return []


def safe_find_one(collection_name, query=None):
    """
    Safely retrieves a single document from a MongoDB collection.
    """
    res = safe_find(collection_name, query=query, limit=1)
    return res[0] if res else None
