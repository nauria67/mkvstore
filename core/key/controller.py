from flask import Blueprint, g, jsonify, request
from flask_cors import CORS

from core.auth.service import AuthService
from core.key.repository import KeyRepository
from core.key.service import KeyService
from core.middleware.auth_middleware import require_access_token
from db.redis_client import RedisDB

blueprint = Blueprint("key", __name__)

# Dependencies
redis_db = RedisDB()
key_repository = KeyRepository(redis_db)
key_service = KeyService(key_repository)

CORS(blueprint, resources={r"/*": {"origins": "*"}})


@blueprint.route("/", methods=["POST"])
@require_access_token
def get_mkv():
    data = request.get_json()
    key = data.get("key")
    value = key_service.get_mkv(g.current_user, key)
    if value is None:
        return jsonify({"error": "key not found"}), 404
    return jsonify(value)


@blueprint.route("/", methods=["PUT"])
@require_access_token
def add_mkv():
    data = request.get_json()
    key = data.get("key")
    value = data.get("value")

    key_service.add_mkv(g.current_user, key, value)
    return jsonify(value), 201
