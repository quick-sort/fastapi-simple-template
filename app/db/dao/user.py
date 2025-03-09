import logging
from sqlalchemy import Select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, UserRole, APIKey, ExternalUser
from app.utils.security import hash_password
from .base import DAO

logger = logging.getLogger(__name__)

class UserDAO(DAO[User]):

    def __init__(self, session:AsyncSession):
        super().__init__(User, session)

    async def create_user(self, username:str, email:str, password:str, roles: list[UserRole] = [UserRole.user]) -> User:
        return await self.create(username=username, email=email, password=hash_password(password), roles=roles)
    
    async def get_user_by_apikey(self, apikey:str) -> User:
        stmt = Select(User).where(User.api_keys.any(APIKey.api_key == apikey))
        objs = await self.session.scalars(stmt)
        objs = objs.all()
        if len(objs):
            return objs[0]
        
    async def get_user_by_external_token(self, token:str) -> User:
        stmt = Select(User).where(User.external_users.any(and_(ExternalUser.token_expired_at > func.now(), ExternalUser.access_token == token)))
        objs = await self.session.scalars(stmt)
        objs = objs.all()
        if len(objs):
            return objs[0]
