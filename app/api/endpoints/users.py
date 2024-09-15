from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from .. import schema
from .. import depends

router = APIRouter()

@router.get('/me')
async def get_my_user(
    user: Annotated[User, Depends(depends.get_current_user)],
) -> dict:
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'email_verified': user.email_verified
    }

@router.post('/registry')
async def registry(
    params: schema.CreateUserParams
) -> dict:
    pass