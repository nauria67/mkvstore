import json

from db.redis_client import RedisDB


class KeyRepository:
    def __init__(self, key_store: RedisDB):
        self.key_store = key_store
        self.key_store.connect()

    def _generate_key(self, tenant_id: str, key: str) -> str:
        return f"id_{tenant_id}_key_{key}"

    def add_mkv(self, tenant_id, key, value):
        redis_key = self._generate_key(tenant_id, key)
        self.key_store.set(redis_key, json.dumps(value))

    def get_mkv(self, tenant_id: str, key: str):
        redis_key = self._generate_key(tenant_id, key)
        data = self.key_store.get(redis_key)
        return json.loads(data) if data else None

    def delete_mkv(self, tenant_id: str, key: str):
        __key = self._generate_key(tenant_id, key)
        self.key_store.delete(__key)
