from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, BaseUser
)
from starlette.middleware.authentication import AuthenticationMiddleware
from app.db.dao.user import UserDAO
from app.config import settings
from app.utils.security import decode_jwt_token
from .auth_user import SimpleUser
import logging
logger = logging.getLogger(__name__)
    
class TokenAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme.lower() != 'bearer':
                return
            payload = decode_jwt_token(token)
        except Exception:
            raise AuthenticationError('Invalid credentials')
        logger.info(payload)
        if not payload or not payload.get('user_id'):
            raise AuthenticationError('Invalid credentials')
        user_id = payload.get('user_id')
        dao = UserDAO(autocommit=True)
        user = await dao.get_by_id(user_id)
        if not user:
            raise AuthenticationError('Invalid credentials')
        return AuthCredentials([user.role]), SimpleUser(user.id)

def add_middleware(app: FastAPI) -> None:
    app.add_middleware(AuthenticationMiddleware, backend=TokenAuthBackend())