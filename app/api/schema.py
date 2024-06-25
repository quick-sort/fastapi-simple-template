from pydantic import BaseModel

class LoginParams(BaseModel):
    username: str
    password: str
    
class CreateUserParams(BaseModel):
    username: str
    password: str