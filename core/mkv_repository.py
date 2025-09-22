from db.redis_client import RedisDB


class MKVRepository:
    def __init__(self, key_store: RedisDB):
        self.key_store = key_store
        self.key_store.connect()

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
    mkv_controller = MKVRepository(redis_db)

    mkv_controller.add_mkv("user1@example.com", "sample_key", "sample_value")
    print(
        f"Value for 'sample_key': {mkv_controller.get_mkv('user1@example.com', 'sample_key')}"
    )

    mkv_controller.delete_mkv("user2@example.com", "sample_key")
    print(
        f"Value for 'sample_key': {mkv_controller.get_mkv('user2@example.com', 'sample_key')}"
    )
