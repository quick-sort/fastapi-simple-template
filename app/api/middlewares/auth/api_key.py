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


class APIKeyAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        bypass, data = has_auth(conn)
        if bypass:
            return data
        if "x-key" not in conn.headers:
            return

        apikey = conn.headers["x-key"]
        db_session = get_db_session(conn)
        user = await User.get_user_by_apikey(db_session, apikey)
        if not user:
            raise AuthenticationError("Invalid api key")
        return AuthCredentials(user.roles), user


def add_middleware(app: FastAPI) -> None:
    app.add_middleware(
        AuthenticationMiddleware, backend=APIKeyAuthBackend(), on_error=on_error
    )
