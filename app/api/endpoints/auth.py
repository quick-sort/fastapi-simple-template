from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import models
from .. import schema

router = APIRouter()

@router.post('/login')
async def login(
) -> schema.LoginResponse:
    user = {}
    token = ''
    if not user:
        raise HTTPException(400)
    return schema.LoginResponse(user_id=user.id, user_token=token)