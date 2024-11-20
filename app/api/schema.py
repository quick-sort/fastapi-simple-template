from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, ConfigDict
from app.db.models.user import UserRole

class JWTToken(BaseModel):
    user_id: int
    scopes: list[str]
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal['Bearer']

class LoginParams(BaseModel):
    username: str
    password: str

class ChangePasswordParams(BaseModel):
    old_password: str
    new_password: str

class CreateUserParams(BaseModel):
    username: str
    email: EmailStr
    password: str

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    roles: list[UserRole]
    email: EmailStr