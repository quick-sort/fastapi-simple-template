import sys
from fastapi import FastAPI
from app.config import settings
from app.api.endpoints import router
from app.api.middlewares import config_middlewares
app = FastAPI(
    debug=True if settings.ENV != 'production' else False,
)
app.include_router(router, prefix='/api')
config_middlewares(app)