import base64
import binascii
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, BaseUser
)
from starlette.middleware.authentication import AuthenticationMiddleware
from app.db.dao.user import UserDAO
from .auth_user import SimpleUser
import logging
logger = logging.getLogger(__name__)

class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if 'user' in conn.scope and conn.scope["user"].is_authenticated:
            return conn.scope["auth"], conn.scope["user"]

        if "Authorization" not in conn.headers:
            return 
        
        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid credentials')
        username, _, password = decoded.partition(":")
        dao = UserDAO(autocommit=True)
        user = await dao.find(username=username)
        if not user:
            raise AuthenticationError('Invalid credentials')
        user = user[0]
        verified = user.verify_password(password=password)
        if not verified:
            raise AuthenticationError('Invalid credentials')
        return AuthCredentials(user.roles), SimpleUser(user.id)

def add_middleware(app: FastAPI) -> None:
    app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())