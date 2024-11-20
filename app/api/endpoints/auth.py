from typing import Optional, Annotated
import jwt
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dao.user import UserDAO
from app.db.models import User
from app.config import settings
from app.utils.security import generate_jwt_token
from .. import schema
from .. import depends

router = APIRouter()
@router.get('/logout')
async def logout(
    db_session: Annotated[AsyncSession, Depends(depends.get_db_session)],
    response: Response,
) -> None:
    response.delete_cookie(
        key=settings.SESSION_COOKIE_NAME, 
    )
    
@router.post('/login')
async def login(
    params: schema.LoginParams,
    db_session: Annotated[AsyncSession, Depends(depends.get_db_session)],
    response: Response,
) -> schema.TokenResponse:
    controller = UserDAO(db_session, autocommit=True)
    user = await controller.find(username=params.username)
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

@router.post('/change_password')
async def change_password(
    params: schema.ChangePasswordParams,
    user: Annotated[User, Depends(depends.get_current_user)],
    db_session: Annotated[AsyncSession, Depends(depends.get_db_session)],
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