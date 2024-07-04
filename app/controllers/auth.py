
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.db.models import User

class JWTToken(BaseModel):
    user_id: int
    scopes: list[str]

class AuthController:

    def __init__(self, ):
        pass

    async def verify_token(self, jwt_token: JWTToken, scopes:list[str]=None) -> User:
        pass
    async def verify_login(self) -> bool:
        pass