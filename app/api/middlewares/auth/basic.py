import base64
import binascii
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, BaseUser
)
from starlette.middleware.authentication import AuthenticationMiddleware
from app.db.dao.user import UserDAO
from app.db.session import ASYNC_DB_SESSION
from .auth_user import SimpleUser, should_bypass, on_error
import logging
logger = logging.getLogger(__name__)

class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        bypass, data = should_bypass(conn)
        if bypass:
            return data

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
        async with ASYNC_DB_SESSION() as session:
            dao = UserDAO(session=session)
            user = await dao.find_one(username=username)
            if not user:
                raise AuthenticationError('Invalid credentials')
            verified = user.verify_password(password=password)
            if not verified:
                raise AuthenticationError('Invalid credentials')
            return AuthCredentials(user.roles), SimpleUser(user.id)

def add_middleware(app: FastAPI) -> None:
    app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend(), on_error=on_error)