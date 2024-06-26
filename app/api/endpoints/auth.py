from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.db import models
from .. import schema

router = APIRouter()

@router.post('/token')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> schema.TokenResponse:
    access_token = ''
    if not access_token:
        raise HTTPException(400)
    return schema.TokenResponse(access_token=access_token, token_type='bearer')

@router.get('/login/{provider}')
async def login_with_provider(
    provider: str,
):
    pass