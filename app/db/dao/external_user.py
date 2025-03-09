import logging
from datetime import datetime
from sqlalchemy import Select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, OauthProvider, ExternalUser, UserRole
from .base import DAO

logger = logging.getLogger(__name__)

class ExternalUserDAO(DAO[OauthProvider]):

    def __init__(self, session:AsyncSession):
        super().__init__(ExternalUser, session)

    async def create_external_user(self, provider:OauthProvider, access_token:str, refresh_token:str, expires_at:int, userinfo:dict, id_token:str=None) -> ExternalUser:
        external_id = userinfo.get('sub')
        if not external_id:
            return
        if isinstance(expires_at, int):
            expires_at = datetime.fromtimestamp(expires_at)
        stmt = Select(ExternalUser).where(ExternalUser.oauth_provider_id == provider.id, ExternalUser.external_id == external_id)
        external_user = await self.session.scalar(stmt)
        if external_user:
            external_user.id_token = id_token
            external_user.access_token = access_token
            external_user.refresh_token = refresh_token
            external_user.expires_at = expires_at
            external_user.userinfo = userinfo
            return external_user

        async with self.session.begin_nested() as nested_transaction:
            user = User(
                username=userinfo.get('email'),
                email=userinfo.get('email'),
                password='', ## Not NULL in DB
                roles=[UserRole.user],
            )
            external_user = ExternalUser(
                user=user,
                oauth_provider_id=provider.id,
                external_id=external_id,
                id_token=id_token,
                access_token=access_token,
                refresh_token=refresh_token,
                userinfo=userinfo,
                expires_at=expires_at,
            )
            self.session.add_all([user, external_user])
            await nested_transaction.commit()
            return external_user