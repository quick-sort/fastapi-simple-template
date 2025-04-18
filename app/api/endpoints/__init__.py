
from fastapi import APIRouter
from . import v1
router = APIRouter()
router.include_router(v1.router, prefix='/v1', tags=['v1'])

__all__ = ['router']