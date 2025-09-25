# middleware/auth_middleware.py
import os
from functools import wraps

import jwt
from flask import g, jsonify, request

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def _extract_bearer_token():
    auth_header = request.headers.get("Authorization", "")
    parts = auth_header.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


def require_access_token(fn):
    """Protects a route by requiring a valid ACCESS JWT. Puts decoded user on g.current_user."""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = _extract_bearer_token()
        if not token:
            return jsonify({"error": "Missing Authorization Bearer token"}), 401

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Access token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid access token"}), 401

        if decoded.get("type") != "access":
            return jsonify({"error": "Invalid token type"}), 401

        # Attach user info to request context
        g.current_user = {
            "tenant_id": decoded.get("tenant_id"),
            "tenant_name": decoded.get("tenant_name"),
        }
        return fn(*args, **kwargs)

    return wrapper
