from typing import Optional, Literal
from pydantic import BaseModel

class LoginParams(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal['bearer']

class CreateUserParams(BaseModel):
    username: str
    password: str