import os
import mimetypes
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, FastAPI, HTTPException, StarletteHTTPException
from app.config import settings

router = APIRouter()
mimetypes.add_type("text/javascript", ".js")

class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except (HTTPException, StarletteHTTPException) as ex:
            if ex.status_code == 404:
                if path.endswith(".js"):
                    # Return 404 for javascript files
                    raise ex
                else:
                    return await super().get_response("index.html", scope)
            else:
                raise ex

def setup_static(app: FastAPI):
    if os.path.exists(settings.STATIC_FILES_DIR):
        app.mount("/", SPAStaticFiles(directory=settings.STATIC_FILES_DIR), name="static")