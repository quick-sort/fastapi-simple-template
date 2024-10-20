from fastapi import FastAPI

def add_middlewares(app: FastAPI):
    from .basic import add_middleware
    add_middleware(app)


__all__ = [
    'add_middlewares'
]