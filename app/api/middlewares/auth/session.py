from fastapi import FastAPI
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError
)
from starlette.middleware.authentication import AuthenticationMiddleware
from app.api.middlewares.db import get_db_session
from app.db.models.user import User
from app.utils.security import decode_jwt_token
from .base import should_bypass, on_error
import logging
logger = logging.getLogger(__name__)
    
class SessionAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        bypass, data = should_bypass(conn)
        if bypass:
            return data
        token = conn.session.get('token')
        if not token:
            return
        payload = decode_jwt_token(token)
        if not payload or not payload.get('user_id'):
            raise AuthenticationError('Invalid cookie')
        user_id = payload.get('user_id')
        db_session = get_db_session(conn)
        user = await db_session.get(User, user_id)
        if not user:
            raise AuthenticationError('Invalid cookie')
        return AuthCredentials(user.roles), user

def add_middleware(app: FastAPI) -> None:
    app.add_middleware(
        AuthenticationMiddleware,
        backend=SessionAuthBackend(), 
        on_error=on_error
    )