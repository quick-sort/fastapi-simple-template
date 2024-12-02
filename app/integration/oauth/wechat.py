from .provider import ProviderFactory, BaseProvider


class WechatProvider(BaseProvider):
    def build_redirect_url(self):
        ...
    async def fetch_access_token(self, code:str) -> str:
        ...
    async def validate_access_token(self, access_token:str) -> tuple[bool, dict]:
        ...
    async def refresh_access_token(self, refresh_token:str) -> str:
        ...

ProviderFactory.providers['wechat'] = WechatProvider