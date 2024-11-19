from fastapi import FastAPI
from app.config import settings
def add_middlewares(app: FastAPI):
    
    from .token import add_middleware
    add_middleware(app)
    from .basic import add_middleware
    add_middleware(app)
    from .cookie import add_middleware
    add_middleware(app)


__all__ = [
    'add_middlewares'
]