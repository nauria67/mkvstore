from flask import Blueprint, g, jsonify, request
from flask_cors import CORS

from core.auth.repository import AuthRepository
from core.auth.service import AuthService
from core.middleware.auth_middleware import require_access_token
from db.redis_client import RedisDB

blueprint = Blueprint("auth", __name__)

# Dependencies
redis_db = RedisDB()
auth_repository = AuthRepository(redis_db)
auth_service = AuthService(auth_repository)

CORS(blueprint, resources={r"/*": {"origins": "*"}})


@blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    tenant_name = data.get("tenant_name")
    password = data.get("password")

    user = auth_service.authenticate(tenant_name, password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = auth_service.generate_access_token(user)
    refresh_token = auth_service.generate_refresh_token(user)

    return jsonify(
        {
            "access_token": access_token["token"],
            "access_expires_at": access_token["expiresAt"],
            "refresh_token": refresh_token["token"],
            "refresh_expires_at": refresh_token["expiresAt"],
            "user": user,
        }
    )


@blueprint.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        return jsonify({"error": "Missing refresh token"}), 400
    decoded = auth_service.decode_token(refresh_token)
    if not decoded or decoded.get("type") != "refresh":
        return jsonify({"error": "Invalid or expired refresh token"}), 401
    # Create new access token
    user = {
        "tenant_id": decoded["tenant_id"],
        "tenant_name": decoded["tenant_name"],
    }
    new_access = auth_service.generate_access_token(user)

    return jsonify(
        {
            "access_token": new_access["token"],
            "access_expires_at": new_access["expiresAt"],
            "user": user,
        }
    )


@blueprint.route("/test_protected", methods=["GET"])
@require_access_token
def protected():
    # g.current_user is set by the middleware
    return jsonify({"message": "Protected route accessed", "user": g.current_user})
