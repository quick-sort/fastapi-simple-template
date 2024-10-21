from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User, UserRole
from app.utils.security import hash_password, verify_password, generate_jwt_token, decode_jwt_token
from .base import Controller

class UserController(Controller[User]):

    def __init__(self, session:AsyncSession=None, autocommit=False):
        super().__init__(User, session, autocommit)

    async def create_user(self, username:str, email:str, password:str, role: UserRole = UserRole.user) -> User:
        return await self.create(username=username, email=email, password=hash_password(password), role=role)
        