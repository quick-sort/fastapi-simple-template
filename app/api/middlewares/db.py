from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import FastAPI
from app.db.session import ASYNC_DB_SESSION, set_db_session_id, reset_db_session_id
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

def get_db_session(request: Request) -> AsyncSession:
    return request.state.db_session

class DBMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        token = set_db_session_id()
        try:
            async with ASYNC_DB_SESSION() as db_session:
                request.state.db_session = db_session
                response = await call_next(request)
                await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            raise
        finally:
            reset_db_session_id(token)
            del request.state.db_session
        return response
    
def add_middleware(app: FastAPI) -> None:
    app.add_middleware(DBMiddleware)