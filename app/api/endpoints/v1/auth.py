import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import schema
from app.api.middlewares.auth import get_current_user
from app.api.middlewares.db import get_db_session
from app.config import settings
from app.db.models import User, UserRole
from app.utils.security import generate_jwt_token

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/logout")
async def logout(
    request: Request,
) -> None:
    request.session.clear()


@router.post("/registry")
async def registry_user(
    params: schema.CreateUserParams,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.User:
    users: list[User] = await User.find(
        async_session=db_session, username=params.username
    )
    if len(users) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username exists",
        )
    user: User = await User.create(
        async_session=db_session,
        username=params.username,
        password=params.password,
        roles=[UserRole.user],
    )
    return user


@router.post("/login")
async def login(
    params: schema.LoginParams,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    request: Request,
) -> schema.TokenResponse:
    user: User | None = await User.find_one(
        async_session=db_session, username=params.username
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    verified = user.verify_password(params.password)
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    jwt_token = generate_jwt_token(
        {"user_id": user.id, "username": user.username}, expires_delta=expires
    )
    if settings.COOKIE_ENABLED:
        request.session["token"] = jwt_token
    return schema.TokenResponse(
        access_token=jwt_token,
        token_type="Bearer",
        expires_in=expires.total_seconds(),
        expires_at=int((datetime.now(timezone.utc) + expires).timestamp()),
    )


@router.get("/me")
async def get_my_user(
    user: Annotated[User, Depends(get_current_user)],
) -> schema.User:
    return user


@router.post("/change_password")
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
    return user
