from fastapi import FastAPI
from app.config import settings
def add_middlewares(app: FastAPI):
    from .cookie import add_middleware
    add_middleware(app)


__all__ = [
    'add_middlewares'
]