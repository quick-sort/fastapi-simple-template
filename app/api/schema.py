from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, ConfigDict, HttpUrl, Field
from app.db.models.user import UserRole

class JWTToken(BaseModel):
    user_id: int
    scopes: list[str]

class UpdateOAuthProviderParams(BaseModel):
    name: Optional[str] = Field(pattern=r'[A-Za-z_\-0-9]+')
    provider_type: Optional[str] = Field(pattern=r'[A-Za-z_\-0-9]+')
    client_id: Optional[str]
    client_secret: Optional[str]
    login_url: Optional[HttpUrl]
    verify_url: Optional[HttpUrl]
    access_token_url: Optional[HttpUrl]
    refresh_token_url: Optional[HttpUrl]
    callback_url: Optional[HttpUrl]
    scope: list[str]

class CreateOAuthProviderParams(BaseModel):
    name: str = Field(pattern=r'[A-Za-z_\-0-9]+')
    provider_type: str = Field(pattern=r'[A-Za-z_\-0-9]+')
    client_id: str
    client_secret: str
    login_url: HttpUrl
    verify_url: HttpUrl
    access_token_url: HttpUrl
    refresh_token_url: HttpUrl
    callback_url: HttpUrl
    scope: list[str]

class OAuthProvider(BaseModel):
    id: int
    name: str
    provider_type: str
    login_url: str

class Deleted(BaseModel):
    id: int

class APIKey(BaseModel):
    id: int
    user_id: int
    name: Optional[str] = 'api_key'
    api_key: str

class CreateAPIKeyParams(BaseModel):
    user_id: int
    name: Optional[str] = 'api_key'

class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal['Bearer']

class LoginParams(BaseModel):
    username: str
    password: str

class ChangePasswordParams(BaseModel):
    old_password: str
    new_password: str

class CreateUserParams(LoginParams):
    email: EmailStr

class User(BaseModel):
    id: int
    username: str
    roles: list[UserRole]
    email: EmailStr