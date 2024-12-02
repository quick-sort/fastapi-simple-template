import httpx
from urllib.parse import urlencode
from .provider import BaseProvider, ProviderFactory

class KeycloakProvider(BaseProvider):

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
                    'refresh_token': access_token,
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

ProviderFactory.providers['keycloak'] = KeycloakProvider