import pytest
import httpx
import logging
from fastapi.testclient import TestClient

logger = logging.getLogger(__name__)
def test_ping(client: TestClient):
    resp = client.get('/api/health/ping')
    assert resp.json()['ping'] == 'pong'

def test_registry(client: TestClient):
    resp = client.get('/api/auth/logout')
    assert resp.status_code == 200, 'logout is not working'

    resp = client.post('/api/auth/registry', json={'username': 'new_user', 'password': 'test', 'email': 'email@email.com'})
    assert resp.status_code == 200, 'registry failed'

    resp = client.post('/api/auth/login', json={'username': 'new_user', 'password': 'test'})
    assert resp.status_code == 200, 'new user login failed'
    result = resp.json()
    access_token = result['access_token']
    assert access_token != None


def test_login(client: TestClient):
    resp = client.get('/api/auth/logout')
    assert resp.status_code == 200, 'logout is not working'

    resp = client.get('/api/auth/me')
    assert resp.status_code == 401, 'auth middleware is not working'

    resp = client.post('/api/auth/login', json={'username': 'notexist', 'password': 'incorrect'})
    assert resp.status_code == 401, 'login check failed'

    resp = client.post('/api/auth/login', json={'username': 'admin', 'password': 'incorrect'})
    assert resp.status_code == 401, 'login check failed'
    resp = client.post('/api/auth/login', json={'username': 'admin', 'password': 'admin'})
    assert resp.status_code == 200, 'login failed'
    resp = client.get('/api/auth/logout')
    assert resp.status_code == 200, 'logout is not working'

def test_auth(client: TestClient):
    resp = client.post('/api/auth/login', json={'username': 'admin', 'password': 'admin'})
    assert resp.status_code == 200, 'login failed'
    result = resp.json()
    access_token = result['access_token']
    assert access_token != None

    resp = client.get('/api/auth/me')
    assert resp.status_code == 200, 'cookie auth middleware is not working'

    resp = client.get('/api/auth/logout')
    assert resp.status_code == 200, 'logout is not working'

    resp = client.get('/api/auth/me')
    assert resp.status_code == 401, 'logout is not working or auth middleware is not working'

    resp = client.get('/api/auth/me', auth=httpx.BasicAuth('admin', 'admin'))
    assert resp.status_code == 200, 'basic auth middleware is not working'

    resp = client.get('/api/auth/me', auth=httpx.BasicAuth('admin', 'incorrect'))
    assert resp.status_code == 401, 'basic auth middleware is not working'
    
    resp = client.get('/api/auth/me', headers={'Authorization': f'Bearer {access_token}'})
    assert resp.status_code == 200, 'token auth middleware is not working'

    resp = client.get('/api/auth/me', headers={'Authorization': f'Bearer {access_token[0:10]}'})
    assert resp.status_code == 401, 'token auth middleware is not working'

def test_api_key(client: TestClient):
    resp = client.get('/api/auth/logout')
    assert resp.status_code == 200, 'logout is not working'

    api_key = 'incorrect'
    resp = client.get('/api/auth/me', headers={'x-key': api_key})
    assert resp.status_code == 401, 'api key middleware is not working'

    resp = client.post('/api/auth/login', json={'username': 'user', 'password': 'user'})
    assert resp.status_code == 200, 'login failed'

    resp = client.post('/api/api_keys/my', params={'name': 'api_key'})
    assert resp.status_code == 200, 'create my api key failed'
    data = resp.json()
    api_key = data['api_key']
    key_id = data['id']

    resp = client.get('/api/auth/me', headers={'x-key': api_key})
    assert resp.status_code == 200, 'api key middleware is not working'

    resp = client.get('/api/api_keys/my', headers={'x-key': api_key})
    assert resp.status_code == 200, 'api key middleware is not working'
    assert len(resp.json()) > 0

    resp = client.delete(f'/api/api_keys/my/{key_id}', headers={'x-key': api_key})
    assert resp.status_code == 200, 'api key middleware is not working'

def test_root_role(client: TestClient):
    resp = client.post('/api/auth/login', json={'username': 'user', 'password': 'user'})
    assert resp.status_code == 200, 'login failed'

    resp = client.get('/api/auth/me')
    assert resp.status_code == 200, 'cookie auth middleware is not working'

    resp = client.get('/api/users')
    assert resp.status_code == 401, 'role checking is not working'

    resp = client.post('/api/auth/login', json={'username': 'admin', 'password': 'admin'})
    assert resp.status_code == 200, 'login failed'

    resp = client.get('/api/users')
    assert resp.status_code == 200, 'role checking is not working'
    
    result = resp.json()
    assert len(result) >= 2, 'get user list failed'
    for i in result:
        if i['username'] not in ['admin', 'user']:
            user_id = i['id']
            resp = client.delete(f'/api/users/{user_id}')
            assert resp.status_code == 200, 'user deletion failed'

def test_change_password(client: TestClient):
    resp = client.post('/api/auth/login', json={'username': 'user', 'password': 'user'})
    assert resp.status_code == 200, 'login failed'

    resp = client.post('/api/auth/change_password', json={'old_password': 'incorrect', 'new_password': 'user'})
    assert resp.status_code == 401, 'failed to verify old password'

    resp = client.post('/api/auth/change_password', json={'old_password': 'user', 'new_password': 'new_password'})
    assert resp.status_code == 200, 'failed to change password'

    resp = client.post('/api/auth/login', json={'username': 'user', 'password': 'new_password'})
    assert resp.status_code == 200, 'failed to change password'

    resp = client.post('/api/auth/change_password', json={'old_password': 'new_password', 'new_password': 'user'})
    assert resp.status_code == 200, 'failed to change password'