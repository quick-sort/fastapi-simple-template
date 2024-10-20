from sqlalchemy import Select
from app.db.models.user import User, UserRole
from app.api.schema import JWTToken
from app.utils.security import hash_password, verify_password, generate_jwt_token, decode_jwt_token
from .base import Controller

class UserController(Controller[User]):

    async def create_user(self, username:str, email:str, password:str, role: UserRole = UserRole.user) -> User:
        user = User(username=username, email=email, password=hash_password(password), role=role)
        self.session.add(user)
        if self.autocommit:
            await self.session.commit()
        return user
    
    async def verify_token(self, jwt_token: JWTToken, scopes:list[str]=None) -> User:
        pass
    async def verify_login(self, password:str, username:str=None, email:str=None) -> bool:
        user = None
        if username:
            user = await self.find_user(username)
        elif email:
            user = await self.find_user(email)
        pass