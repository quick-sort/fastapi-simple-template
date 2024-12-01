import httpx
from urllib.parse import urlencode

class OAuthProvider:
    def __init__(self, client_id:str, client_secret:str, login_url:str, verify_url:str, access_token_url:str, refresh_token_url:str, scope:str, callback_url:str, *args, **kwargs):
        self.client_id = client_id
        self.client_secret = client_secret
        self.login_url = login_url
        self.verify_url = verify_url
        self.access_token_url = access_token_url
        self.refresh_token_url = refresh_token_url
        self.callback_url = callback_url
        self.scope = scope

    def build_redirect_url(self) -> str:
        params = {
            'client_id': self.client_id,
            'scope': self.scope,
            'redirect_uri': self.callback_url,
            'response_type': 'code',
        }
        params_encoded = urlencode(params)
        return f"{self.login_url}?{params_encoded}"

    async def fetch_access_token(self, code:str) -> dict|None:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url=self.access_token_url,
                params={
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': self.callback_url,
                }
            )
            if resp.status_code != 200:
                return
            return resp.json()
            
    async def validate_access_token(self, access_token:str) -> tuple[bool, dict]:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url=self.refresh_token_url,
                params={
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                }
            )
            if resp.status_code != 200:
                return
            return resp.json()
    async def refresh_access_token(self, refresh_token:str) -> dict|None:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url=self.refresh_token_url,
                params={
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                }
            )
            if resp.status_code != 200:
                return
            return resp.json()

class ProviderFactory:
    providers = {
        'oauth2': OAuthProvider
    }

    @classmethod
    def create_provider(cls, provider:str, *args, **kwargs):
        provider_cls = ProviderFactory.providers.get(provider)
        assert provider_cls is not None, f'oauth provider {provider} not found'
        return cls(*args, **kwargs)