from starlette.authentication import BaseUser
from starlette.requests import HTTPConnection
from starlette.responses import PlainTextResponse, Response
from fastapi import status

class SimpleUser(BaseUser):
    def __init__(self, user_id):
        self.user_id = user_id

    @property
    def is_authenticated(self) -> bool:
        return True  # pragma: no cover

    @property
    def identity(self) -> int:
        return self.user_id
    
def should_bypass(conn: HTTPConnection) -> bool:
    if 'user' in conn.scope and conn.scope["user"].is_authenticated:
        return True, (conn.scope["auth"], conn.scope["user"])
    return False, None

def on_error(conn:HTTPConnection, exc:Exception) -> Response:
    return PlainTextResponse(str(exc), status_code=status.HTTP_401_UNAUTHORIZED)