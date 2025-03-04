from fastapi import FastAPI
from app.config import settings
from app.api.endpoints import router as api_router
from app.api.middlewares import config_middlewares

app = FastAPI(
    debug=True if settings.ENV != 'prod' else False,
    docs_url="/api/docs",
)
app.include_router(api_router, prefix='/api')
config_middlewares(app)