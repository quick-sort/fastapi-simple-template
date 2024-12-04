from fastapi import FastAPI
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError
)
from starlette.middleware.authentication import AuthenticationMiddleware
from app.db.dao.user import UserDAO
from app.db.session import ASYNC_DB_SESSION
from .auth_user import SimpleUser, should_bypass, on_error
import logging
logger = logging.getLogger(__name__)
    
class APIKeyAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        bypass, data = should_bypass(conn)
        if bypass:
            return data
        if "x-key" not in conn.headers:
            return

        apikey = conn.headers["x-key"]
        async with ASYNC_DB_SESSION() as session:
            dao = UserDAO(session)
            user = await dao.get_user_by_apikey(apikey)
            if not user:
                raise AuthenticationError('Invalid api key')
            return AuthCredentials(user.roles), SimpleUser(user.id)

def add_middleware(app: FastAPI) -> None:
    app.add_middleware(AuthenticationMiddleware, backend=APIKeyAuthBackend(), on_error=on_error)