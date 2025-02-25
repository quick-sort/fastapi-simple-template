from typing import Annotated
from starlette.requests import HTTPConnection
from starlette.responses import PlainTextResponse, Response
from fastapi import Depends, status, HTTPException, Request
from fastapi.security import SecurityScopes
from app.db.models import User


def should_bypass(conn: HTTPConnection) -> bool:
    if 'user' in conn.scope and conn.scope["user"].is_authenticated:
        return True, (conn.scope["auth"], conn.scope["user"])
    return False, None

def on_error(conn:HTTPConnection, exc:Exception) -> Response:
    return PlainTextResponse(str(exc), status_code=status.HTTP_401_UNAUTHORIZED)


async def get_current_user(request: Request) -> User:
    if request.user.is_authenticated:
        return request.user
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Unauthorized'
    )
    
async def get_scoped_user(
    security_scopes: SecurityScopes,
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    for scope in security_scopes.scopes:
        if scope not in user.roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
    return user