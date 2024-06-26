from typing import Optional
from pydantic import BaseModel

class LoginParams(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    user_id: int
    user_token: str

class CreateUserParams(BaseModel):
    username: str
    password: str