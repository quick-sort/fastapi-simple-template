from typing import Optional, Literal
from pydantic import BaseModel, EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal['Bearer']

class CreateUserParams(BaseModel):
    username: str
    email: EmailStr
    password: str