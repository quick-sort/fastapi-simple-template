import base64
import binascii
import logging

from fastapi import FastAPI
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)
from starlette.middleware.authentication import AuthenticationMiddleware

from app.api.middlewares.db import get_db_session
from app.db.models.user import User

from .base import has_auth, on_error

logger = logging.getLogger(__name__)


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        bypass, data = has_auth(conn)
        if bypass:
            return data

        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != "basic":
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError("Invalid credentials")
        username, _, password = decoded.partition(":")
        session = get_db_session(conn)
        user: User | None = await User.find_one(session, username=username)
        if not user:
            raise AuthenticationError("Invalid credentials")
        verified = user.verify_password(password=password)
        if not verified:
            raise AuthenticationError("Invalid credentials")
        return AuthCredentials(user.roles), user


def add_middleware(app: FastAPI) -> None:
    app.add_middleware(
        AuthenticationMiddleware, backend=BasicAuthBackend(), on_error=on_error
    )
