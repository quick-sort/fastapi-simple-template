import logging
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, UserRole, APIKey
from app.utils.security import hash_password, verify_password, generate_jwt_token, decode_jwt_token
from .base import DAO

logger = logging.getLogger(__name__)

class UserDAO(DAO[User]):

    def __init__(self, session:AsyncSession, autocommit=True):
        super().__init__(User, session, autocommit)

    async def create_user(self, username:str, email:str, password:str, roles: list[UserRole] = [UserRole.user]) -> User:
        return await self.create(username=username, email=email, password=hash_password(password), roles=roles)
    
    async def get_user_by_apikey(self, apikey:str) -> User:
        stmt = Select(User).where(User.api_keys.any(APIKey.api_key == apikey))
        objs = await self.session.scalars(stmt)
        objs = objs.all()
        if len(objs):
            return objs[0]