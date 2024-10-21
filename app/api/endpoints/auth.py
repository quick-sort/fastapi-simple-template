from typing import Optional, Annotated
import jwt
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers.user import UserController
from app.db.models import User
from app.config import settings
from app.utils.security import generate_jwt_token
from .. import schema
from .. import depends

router = APIRouter()

@router.post('/login')
async def login(
    params: schema.LoginParams,
    db_session: Annotated[AsyncSession, Depends(depends.get_db_session)],
    response: Response,
) -> schema.TokenResponse:
    controller = UserController(db_session, autocommit=True)
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
        secure=True, 
        samesite="strict"
    )
    return schema.TokenResponse(access_token=jwt_token, token_type='Bearer')