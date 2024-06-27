from fastapi import FastAPI

def config_middlewares(app: FastAPI):
    from starlette.middleware import Middleware
    from .auth import AuthMiddleware
    app.add_middleware(Middleware(AuthMiddleware, bypass=['/api/users/registry', '/api/auth/login']))

__all__ = [
    'config_middlewares'
]