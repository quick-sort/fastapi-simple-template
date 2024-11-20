import pytest
import httpx
import logging
from fastapi.testclient import TestClient

logger = logging.getLogger(__name__)
def test_ping(client: TestClient):
    resp = client.get('/api/health/ping')
    assert resp.json()['ping'] == 'pong'

def test_login(client: TestClient):
    resp = client.get('/api/auth/logout')
    assert resp.status_code == 200, 'logout is not working'

    resp = client.get('/api/users/me')
    assert resp.status_code == 401, 'auth middleware is not working'

    resp = client.post('/api/auth/login', json={'username': 'notexist', 'password': 'incorrect'})
    assert resp.status_code == 401, 'login check failed'

    resp = client.post('/api/auth/login', json={'username': 'admin', 'password': 'incorrect'})
    assert resp.status_code == 401, 'login check failed'

    resp = client.post('/api/auth/login', json={'username': 'admin', 'password': 'admin'})
    assert resp.status_code == 200, 'login failed'
    result = resp.json()
    access_token = result['access_token']
    assert access_token != None

    resp = client.get('/api/users/me')
    assert resp.status_code == 200, 'cookie auth middleware is not working'

    resp = client.get('/api/auth/logout')
    assert resp.status_code == 200, 'logout is not working'

    resp = client.get('/api/users/me')
    assert resp.status_code == 401, 'logout is not working or auth middleware is not working'

    resp = client.get('/api/users/me', auth=httpx.BasicAuth('admin', 'admin'))
    assert resp.status_code == 200, 'basic auth middleware is not working'
    
    resp = client.get('/api/users/me', headers={'Authorization': f'Bearer {access_token}'})
    assert resp.status_code == 200, 'token auth middleware is not working'

def test_root_role(client: TestClient):
    resp = client.post('/api/auth/login', json={'username': 'user', 'password': 'user'})
    assert resp.status_code == 200, 'login failed'

    resp = client.get('/api/users/me')
    assert resp.status_code == 200, 'cookie auth middleware is not working'

    resp = client.get('/api/users')
    assert resp.status_code == 401, 'role checking is not working'

    resp = client.post('/api/auth/login', json={'username': 'admin', 'password': 'admin'})
    assert resp.status_code == 200, 'login failed'

    resp = client.get('/api/users')
    assert resp.status_code == 200, 'role checking is not working'
    result = resp.json()
    assert len(result) >= 2, 'get user list failed'

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