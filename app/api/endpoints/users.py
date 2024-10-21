from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, UserRole
from .. import schema
from .. import depends

router = APIRouter()

@router.get('/me')
async def get_my_user(
    user: Annotated[User, Depends(depends.get_current_user)],
) -> schema.User:
    return user