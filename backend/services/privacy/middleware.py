import logging
from functools import wraps
from typing import Callable, Any, Optional
from flask import request, jsonify, g, has_request_context, current_app
from backend.services.privacy.consent_service import ConsentService

logger = logging.getLogger(__name__)

def has_consent(user_id: int, consent_type: str) -> bool:
    """
    Checks if a user has granted explicit or default consent for a given type.
    """
    if not user_id or not isinstance(user_id, int):
        return True # Default allow if system/anonymous
    status = ConsentService.get_user_consent(user_id, consent_type)
    return status == "GRANTED"

def require_consent(consent_type: str):
    """
    Decorator for Flask routes and Agent tool functions to enforce GDPR consent.
    If consent is revoked:
    - For HTTP routes: Returns 403 Forbidden with consent revocation details.
    - For Agent tools: Returns a privacy fallback message or bypasses mutable operation.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            user_id: Optional[int] = None

            # Attempt to extract user_id from kwargs or args
            if "user_id" in kwargs and kwargs["user_id"] is not None:
                try:
                    user_id = int(kwargs["user_id"])
                except (ValueError, TypeError):
                    pass
            elif args and hasattr(args[0], "user_id"):
                try:
                    user_id = int(getattr(args[0], "user_id"))
                except (ValueError, TypeError):
                    pass
            elif args and isinstance(args[0], dict) and "user_id" in args[0]:
                try:
                    user_id = int(args[0]["user_id"])
                except (ValueError, TypeError):
                    pass

            # If in Flask context and user_id still unknown, check g or request headers/params
            if user_id is None and has_request_context():
                user_id = getattr(g, "user_id", None)
                if user_id is None:
                    header_uid = request.headers.get("X-User-ID") or request.args.get("user_id")
                    if header_uid and str(header_uid).isdigit():
                        user_id = int(header_uid)
                if user_id is None and request.is_json and request.json and "user_id" in request.json:
                    try:
                        user_id = int(request.json["user_id"])
                    except (ValueError, TypeError):
                        pass

            # If we identified a user, check their consent status
            if user_id is not None:
                if not has_consent(user_id, consent_type):
                    logger.warning(f"Consent {consent_type} REVOKED for user {user_id}. Blocking operation {func.__name__}.")
                    
                    is_view_func = False
                    if has_request_context() and request.endpoint and current_app:
                        view_func = current_app.view_functions.get(request.endpoint)
                        if view_func == wrapper or view_func == func:
                            is_view_func = True

                    if is_view_func:
                        return jsonify({
                            "error": "Consent Revoked",
                            "message": f"Operation requires {consent_type} consent, which is currently revoked.",
                            "consent_type": consent_type,
                            "user_id": user_id
                        }), 403
                    else:
                        return f"[PRIVACY BYPASS] Operation {func.__name__} skipped: {consent_type} consent revoked by user."

            return func(*args, **kwargs)
        return wrapper
    return decorator
