from core.mkv_repository import MKVRepository


class MKVService:
    def __init__(self, mkv_repository: MKVRepository):
        self.mkv_repository = mkv_repository

    def get_mkv(self, tenant: str, key: str):
        return self.mkv_repository.get_mkv(tenant, key)

    def put_mkv(self, tenant: str, key: str, value: str):
        self.mkv_repository.add_mkv(tenant, key, value)

    def delete_mkv(self, tenant: str, key: str):
        self.mkv_repository.delete_mkv(tenant, key)
