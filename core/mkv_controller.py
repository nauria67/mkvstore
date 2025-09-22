from flask import Blueprint, jsonify, request
from flask_cors import CORS

from core.mkv_repository import MKVRepository
from core.mkv_service import MKVService
from db.redis_client import RedisDB

mkv_blueprint = Blueprint("mkv", __name__)

# Dependencies
redis_db = RedisDB()
mkv_repository = MKVRepository(redis_db)
mkv_service = MKVService(mkv_repository)

CORS(mkv_blueprint, resources={r"/*": {"origins": "*"}})


@mkv_blueprint.route("/get", methods=["POST"])
def get_mkv():
    data = request.get_json()
    tenant = data.get("tenant")
    key = data.get("key")
    if not tenant or not key:
        return jsonify({"message": "tenant and key are required"}), 400

    value = mkv_service.get_mkv(tenant, key)
    if value is not None:
        return jsonify({key: value})
    return jsonify({"message": "Key not found"}), 404


@mkv_blueprint.route("/put", methods=["POST"])
def put_mkv():
    data = request.get_json()
    tenant = data.get("tenant")
    key = data.get("key")
    value = data.get("value")
    if not tenant or not key or value is None:
        return jsonify({"message": "tenant, key, and value are required"}), 400

    mkv_service.put_mkv(tenant, key, value)
    return jsonify({"message": "Value set successfully"}), 201


@mkv_blueprint.route("/delete", methods=["POST"])
def delete_mkv():
    data = request.get_json()
    tenant = data.get("tenant")
    key = data.get("key")
    if not tenant or not key:
        return jsonify({"message": "tenant and key are required"}), 400

    mkv_service.delete_mkv(tenant, key)
    return jsonify({"message": "Key deleted successfully"}), 200
