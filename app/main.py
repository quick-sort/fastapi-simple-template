import sys
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.api.endpoints import router
from app.api.middlewares import config_middlewares
app = FastAPI(
    debug=True if settings.ENV != 'prod' else False,
)
app.include_router(router, prefix='/api')
config_middlewares(app)

@app.get("/")
async def root():
    return FileResponse(os.path.join(settings.STATIC_FILES_DIR, 'index.html'))

if os.path.exists(settings.STATIC_FILES_DIR):
    app.mount("/", StaticFiles(directory=settings.STATIC_FILES_DIR), name="static")
