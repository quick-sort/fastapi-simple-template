import os
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, FastAPI
from app.config import settings

router = APIRouter()
def setup_static(app: FastAPI):
    if os.path.exists(settings.STATIC_FILES_DIR):
        app.mount("/", StaticFiles(directory=settings.STATIC_FILES_DIR), name="static")

@router.get("/")
async def root():
    return FileResponse(os.path.join(settings.STATIC_FILES_DIR, 'index.html'))