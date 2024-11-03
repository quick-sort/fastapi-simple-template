import sys
import os
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.api.endpoints import router
from app.api.middlewares import config_middlewares
app = FastAPI(
    debug=True if settings.ENV != 'production' else False,
)
app.include_router(router, prefix='/api')
config_middlewares(app)

@app.get("/")
async def root():
    return RedirectResponse(
        '/index.html', status_code=status.HTTP_301_MOVED_PERMANENTLY, headers=None, background=None
    )

if os.path.exists(settings.STATIC_FILES_DIR):
    app.mount("/", StaticFiles(directory=settings.STATIC_FILES_DIR), name="static")