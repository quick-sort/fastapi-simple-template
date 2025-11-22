from fastapi import FastAPI


def add_middleware(app: FastAPI):
    from app.config import settings

    if settings.COOKIE_ENABLED:
        from starlette.middleware.sessions import SessionMiddleware

        app.add_middleware(
            SessionMiddleware,
            secret_key=settings.SESSION_SECRET_KEY,
        )
