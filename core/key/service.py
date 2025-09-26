import datetime
import os

import jwt

from core.key.repository import KeyRepository

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXP_MINUTES = 30
REFRESH_TOKEN_EXP_DAYS = 7


class KeyService:
    def __init__(self, repository: KeyRepository):
        self.repository = repository

    def add_mkv(self, tenant_id: str, key: str, value: str):
        self.repository.add_mkv(tenant_id, key, value)

    def get_mkv(self, tenant_id: str, key: str):
        return self.repository.get_mkv(tenant_id, key)

    def delete_mkv(self, tenant_id: str, key: str):
        self.repository.delete_mkv(tenant_id, key)
