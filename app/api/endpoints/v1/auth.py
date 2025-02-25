from typing import Optional, Annotated
import logging
from fastapi import APIRouter, Depends, HTTPException, Response, status, Path
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.middlewares.auth import get_current_user, get_scoped_user
from app.api.middlewares.db import get_db_session
from app.db.dao.user import UserDAO
from app.db.models import User, UserRole
from app.config import settings
from app.utils.security import generate_jwt_token
from app.api import schema

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get('/logout')
async def logout(
    response: Response,
) -> None:
    response.delete_cookie(
        key=settings.SESSION_COOKIE_NAME, 
    )

@router.post('/registry')
async def registry_user(
    params: schema.CreateUserParams,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.User:
    dao = UserDAO(db_session)
    user = await dao.find(username=params.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username exists",
        )
    user = await dao.find(email=params.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email exists",
        )
    user = await dao.create_user(username=params.username, email=params.email, password=params.password, roles=[UserRole.user])
    return user

@router.post('/login')
async def login(
    params: schema.LoginParams,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    response: Response,
) -> schema.TokenResponse:
    dao = UserDAO(db_session)
    user = await dao.find(username=params.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = user[0]
    verified = user.verify_password(params.password)
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    jwt_token = generate_jwt_token({'user_id': user.id})
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME, 
        value=jwt_token, 
        httponly=True, 
        # secure=True, # for https
        samesite="strict"
    )
    return schema.TokenResponse(access_token=jwt_token, token_type='Bearer')

@router.get('/me')
async def get_my_user(
    user: Annotated[User, Depends(get_current_user)],
) -> schema.User:
    return user

@router.post('/change_password')
async def change_password(
    params: schema.ChangePasswordParams,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.User:
    verified = user.verify_password(params.old_password)
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    if params.new_password != params.old_password:
        user.update_password(params.new_password)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
    return user

@router.get('/oauth/login/{provider_name}')
async def oauth_login(
    provider_name: Annotated[str, Path(pattern=r'^[A-Za-z0-9_\-]+$')],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> RedirectResponse:
    # login_url?response_type=code&client_id=CLIENT_ID&redirect_uri=CALLBACK_URL&scope=read
    ...

@router.get('/oauth/callback/{provider_name}')
async def oauth_callback_with_id(
    provider_name: Annotated[str, Path(pattern=r'^[A-Za-z0-9_\-]+$')],
    code: str,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> RedirectResponse:
    ...
