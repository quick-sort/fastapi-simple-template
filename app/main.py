from fastapi import FastAPI

from app.api.endpoints import router as api_router
from app.api.middlewares import config_middlewares
from app.config import settings
from app.static import setup_static

app = FastAPI(
    debug=True if settings.ENV != "prod" else False,
    docs_url="/api/docs",
)
app.include_router(api_router, prefix="/api")
config_middlewares(app)
setup_static(app)

if __name__ == "__main__":
    from app.cli.main import main

    main()
