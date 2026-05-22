from flask import current_app
from datetime import datetime
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
        return True
    except Exception as e:
        current_app.logger.warning("Mongo insert failed for %s: %s", collection_name, e)
        return False
