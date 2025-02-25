from typing import Optional, Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.middlewares.db import get_db_session
from app.db.dao.user import UserDAO

router = APIRouter()

@router.get('/ping')
async def ping(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> dict:
    return {'ping': 'pong'}