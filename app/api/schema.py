from typing import Optional, Literal, Any
from pydantic import BaseModel, EmailStr, ConfigDict, HttpUrl, Field, field_serializer, FieldSerializationInfo
from app.db.models.user import UserRole
from app.db.models.oauth_provider import ProviderType

class JWTToken(BaseModel):
    user_id: int
    scopes: list[str]

class UpdateOAuthProviderParams(BaseModel):
    name: Optional[str] = Field(pattern=r'[A-Za-z_\-0-9]+', default=None)
    provider_type: Optional[str] = Field(pattern=r'[A-Za-z_\-0-9]+', default=None)
    client_id: Optional[str] = Field(pattern=r'[A-Za-z_\-0-9]+', default=None)
    client_secret: Optional[str] = Field(default=None)
    login_url: Optional[HttpUrl] = Field(default=None)
    verify_url: Optional[HttpUrl] = Field(default=None)
    access_token_url: Optional[HttpUrl] = Field(default=None)
    refresh_token_url: Optional[HttpUrl] = Field(default=None)
    callback_url: Optional[HttpUrl] = Field(default=None)
    scope: Optional[list[str]] = Field(default=[])

    @field_serializer('login_url', 'verify_url', 'access_token_url', 'refresh_token_url', 'callback_url')
    def url_to_str(self, value: Any, info: FieldSerializationInfo) -> str:
        return str(value)

class BaseOAuthProvider(BaseModel):
    name: str = Field(pattern=r'[A-Za-z_\-0-9]+')
    provider_type: ProviderType
    client_id: str
    server_metadata_url: Optional[HttpUrl] = Field(default=None)
    api_base_url: Optional[HttpUrl] = Field(default=None)
    request_token_url: Optional[HttpUrl] = Field(default=None)
    request_token_params: Optional[dict] = Field(default={})
    authorize_url: Optional[HttpUrl] = Field(default=None)
    authorize_params: Optional[dict] = Field(default={})
    access_token_url: Optional[HttpUrl] = Field(default=None)
    access_token_params: Optional[dict] = Field(default={})
    refresh_token_url: Optional[HttpUrl] = Field(default=None)
    refresh_token_params: Optional[dict] = Field(default={})
    userinfo_url: Optional[HttpUrl] = Field(default=None)
    redirect_uri: HttpUrl
    client_kwargs: Optional[dict] = Field(default={})

    @field_serializer('server_metadata_url', 'api_base_url', 'request_token_url', 'authorize_url', 'access_token_url', 'refresh_token_url', 'userinfo_url', 'redirect_uri')
    def url_to_str(self, value: Any, info: FieldSerializationInfo) -> str|None:
        if value is None:
            return
        return str(value)

class CreateOAuthProviderParams(BaseOAuthProvider):
    client_secret: str

class OAuthProvider(BaseOAuthProvider):
    id: int

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
    token_type: Literal['Bearer'] = 'Bearer'
    refresh_token: Optional[str] = None
    expires_in: int
    expires_at: int

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