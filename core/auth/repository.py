import json

from db.redis_client import RedisDB


class AuthRepository:
    def __init__(self, key_store: RedisDB):
        self.key_store = key_store
        self.key_store.connect()

    def validate_user(self, tenant_name, password):
        tenant_data = self.key_store.get(f"user_{tenant_name}")
        if not tenant_data:
            return None
        tenant_data = json.loads(tenant_data)
        if tenant_data and tenant_data.get("password") == password:
            return {
                "tenant_id": tenant_data.get("tenant_id"),
                "tenant_name": tenant_name,
            }
        return None

    def _generate_key(self, tenant: str, key: str) -> str:
        return f"{tenant}!{key}"

    def add_mkv(self, tenant: str, key: str, value: str):
        __key = self._generate_key(tenant, key)
        self.key_store.set(__key, value)

    def get_mkv(self, tenant: str, key: str):
        __key = self._generate_key(tenant, key)
        return self.key_store.get(__key)

    def delete_mkv(self, tenant: str, key: str):
        __key = self._generate_key(tenant, key)
        self.key_store.delete(__key)


if __name__ == "__main__":
    redis_db = RedisDB()
    auth_repository = AuthRepository(redis_db)
    result = auth_repository.validate_user("tenant1", "pass101")
    print(f"tenant_validation': {result}")
