from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, BaseUser
)
from starlette.middleware.authentication import AuthenticationMiddleware
from app.db.dao.user import UserDAO
from app.db.session import ASYNC_DB_SESSION
from app.config import settings
from app.utils.security import decode_jwt_token
from .auth_user import SimpleUser, should_bypass, on_error
import logging
logger = logging.getLogger(__name__)
    
class CookieAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        bypass, data = should_bypass(conn)
        if bypass:
            return data
        token = conn.cookies.get(settings.SESSION_COOKIE_NAME)
        if not token:
            return
        payload = decode_jwt_token(token)
        if not payload or not payload.get('user_id'):
            raise AuthenticationError('Invalid cookie')
        user_id = payload.get('user_id')
        async with ASYNC_DB_SESSION() as session:
            dao = UserDAO(session)
            user = await dao.get_by_id(user_id)
            if not user:
                raise AuthenticationError('Invalid cookie')
            return AuthCredentials(user.roles), SimpleUser(user.id)

def add_middleware(app: FastAPI) -> None:
    app.add_middleware(AuthenticationMiddleware, backend=CookieAuthBackend(), on_error=on_error)