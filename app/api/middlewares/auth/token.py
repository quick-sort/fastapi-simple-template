from fastapi import FastAPI
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError
)
from starlette.middleware.authentication import AuthenticationMiddleware
from app.api.middlewares.db import get_db_session
from app.db.dao.user import UserDAO
from app.utils.security import decode_jwt_token
from .base import should_bypass, on_error
import logging
logger = logging.getLogger(__name__)
    
class TokenAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        bypass, data = should_bypass(conn)
        if bypass:
            return data
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme.lower() != 'bearer':
                return
            payload = decode_jwt_token(token)
        except Exception:
            raise AuthenticationError('Invalid token')

        if not payload or not payload.get('user_id'):
            raise AuthenticationError('Invalid token')
        user_id = payload.get('user_id')
        session = get_db_session(conn)
        dao = UserDAO(session)
        user = await dao.get_by_id(user_id)
        if not user:
            raise AuthenticationError('Invalid token')
        return AuthCredentials(user.roles), user

def add_middleware(app: FastAPI) -> None:
    app.add_middleware(
        AuthenticationMiddleware, 
        backend=TokenAuthBackend(), 
        on_error=on_error
    )