from fastapi import FastAPI

def config_middlewares(app: FastAPI):
    from .auth import add_middlewares
    add_middlewares(app)

__all__ = [
    'config_middlewares'
]