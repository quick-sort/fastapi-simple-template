from fastapi import APIRouter

from . import api_key, auth, health, oauth, oauth_providers, users

router = APIRouter()


router.include_router(auth.router, prefix="/auth")


router.include_router(users.router, prefix="/users")


router.include_router(health.router, prefix="/health")


router.include_router(api_key.router, prefix="/api_keys")


router.include_router(oauth_providers.router, prefix="/oauth_providers")


router.include_router(oauth.router, prefix="/oauth")

__all__ = ["router"]
