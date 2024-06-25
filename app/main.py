import sys
from fastapi import FastAPI
from app.config import settings
from app.api.endpoints import router

app = FastAPI(
    debug=True if settings.ENV != 'production' else False,
)
app.include_router(router, prefix='/api')