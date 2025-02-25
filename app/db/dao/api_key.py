import logging
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import APIKey
from app.utils.security import generate_api_key
from app.config import settings
from .base import DAO

logger = logging.getLogger(__name__)

class APIKeyDAO(DAO[APIKey]):

    def __init__(self, session:AsyncSession):
        super().__init__(APIKey, session)

    async def create_api_key(self, user_id:int, name:str) -> APIKey:
        api_key = generate_api_key(settings.API_KEY_LEN)
        obj = await self.create(user_id=user_id, name=name, api_key=api_key)
        return obj
