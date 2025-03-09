from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
from app.config import settings

def add_middleware(app: FastAPI):
    app.add_middleware(
        SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY,
    )