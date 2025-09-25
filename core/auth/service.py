import datetime
import os

import jwt

from core.auth.repository import AuthRepository

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXP_MINUTES = 30
REFRESH_TOKEN_EXP_DAYS = 7


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def generate_access_token(self, user):
        exp = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=ACCESS_TOKEN_EXP_MINUTES
        )
        exp_ms = int(exp.timestamp() * 1000)  # epoch milliseconds
        payload = {
            "tenant_id": user["tenant_id"],
            "tenant_name": user["tenant_name"],
            "type": "access",
            "exp": exp,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return {"token": token, "expiresAt": exp_ms}

    def generate_refresh_token(self, user):
        exp = datetime.datetime.utcnow() + datetime.timedelta(
            days=REFRESH_TOKEN_EXP_DAYS
        )
        exp_ms = int(exp.timestamp() * 1000)
        payload = {
            "tenant_id": user["tenant_id"],
            "tenant_name": user["tenant_name"],
            "type": "refresh",
            "exp": exp,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return {"token": token, "expiresAt": exp_ms}

    def decode_token(self, token):
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return decoded
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def authenticate(self, tenant_name, password):
        return self.repository.validate_user(tenant_name, password)
