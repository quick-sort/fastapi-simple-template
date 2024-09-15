from typing import Optional, Annotated
import jwt
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.db.models import User
from app.config import settings
from app.utils.security import generate_jwt_token
from .. import schema
from .. import depends

router = APIRouter()

@router.post('/token')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> schema.TokenResponse:
    username = form_data.username
    
    ## TODO: authenticate form_data
    ## TODO: get user_id
    user = {}
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    jwt_token = generate_jwt_token({'user_id': user.id})
    return schema.TokenResponse(access_token=jwt_token, token_type='Bearer')

@router.get('/token/verify')
async def verify_token(
    token: Annotated[str, Depends(depends.get_oauth_token)]
) -> schema.TokenResponse:
    user = await depends.get_current_user(token)
    return schema.TokenResponse(access_token=token, token_type='bearer')