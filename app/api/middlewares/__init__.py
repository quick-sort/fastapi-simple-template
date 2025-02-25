from fastapi import FastAPI

def config_middlewares(app: FastAPI):
    from .auth import add_middlewares
    add_middlewares(app)
    from .db import add_middleware
    add_middleware(app)

__all__ = [
    'config_middlewares'
]