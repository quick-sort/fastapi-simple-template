from fastapi import FastAPI
from .base import get_current_user, get_scoped_user
def add_middlewares(app: FastAPI):
    
    from .token import add_middleware
    add_middleware(app)
    from .basic import add_middleware
    add_middleware(app)
    from .session import add_middleware
    add_middleware(app)
    from .api_key import add_middleware
    add_middleware(app)


__all__ = [
    'add_middlewares',
    'get_current_user',
    'get_scoped_user',
]