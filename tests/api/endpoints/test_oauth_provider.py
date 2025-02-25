import pytest
import httpx
import logging
from fastapi.testclient import TestClient

logger = logging.getLogger(__name__)
def test_crud_oauth_provider(client: TestClient):
    resp = client.get('/api/v1/oauth_providers/')
    providers = resp.json()
    resp = client.post('/api/v1/auth/login', json={'username': 'admin', 'password': 'admin'})
    assert resp.status_code == 200
    for i in providers:
        resp = client.delete(f'/api/v1/oauth_providers/{i["id"]}')
        assert resp.status_code == 200
    resp = client.post('/api/v1/oauth_providers/', json={
        'name': 'test_provider',
        'provider_type': 'oauth2',
        'client_id': 'test_client_id',
        'client_secret': 'test_client_secret',
        'login_url': 'http://test_login.url.com',
        'verify_url': 'http://test_verify.url.com',
        'access_token_url': 'http://test_access_token.url.com',
        'refresh_token_url': 'http://test_refresh_token.url.com',
        'callback_url': 'http://test_callback.url.com',
        'scope':['login'],
    })
    assert resp.status_code == 200
    provider_id = resp.json()['id']
    resp = client.put(f'/api/v1/oauth_providers/{provider_id}', json={
        'name': 'test_provider_updated',
    })
    assert resp.status_code == 200
    resp = client.get(f'/api/v1/oauth_providers/{provider_id}')
    assert resp.status_code == 200
    assert resp.json()['name'] == 'test_provider_updated'
    resp = client.delete(f'/api/v1/oauth_providers/{provider_id}')
    assert resp.status_code == 200