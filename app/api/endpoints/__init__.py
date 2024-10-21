
from fastapi import APIRouter


router = APIRouter()
from . import auth
router.include_router(auth.router, prefix='/auth', tags=['authentication'])

from . import users
router.include_router(users.router, prefix='/users', tags=['users'])

from . import health
router.include_router(health.router, prefix='/health', tags=['health'])

__all__ = ['router']