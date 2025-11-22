import logging

import httpx
import pytest
from httpx import AsyncClient

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_registry(client: AsyncClient):
    resp = await client.get("/api/v1/auth/logout")
    assert resp.status_code == 200, "logout is not working"

    resp = await client.post(
        "/api/v1/auth/registry",
        json={"username": "new_user", "password": "test"},
    )
    assert resp.status_code == 200, "registry failed"

    resp = await client.post(
        "/api/v1/auth/login", json={"username": "new_user", "password": "test"}
    )
    assert resp.status_code == 200, "new user login failed"
    result = resp.json()
    access_token = result["access_token"]
    assert access_token is not None


@pytest.mark.asyncio
async def test_login(client: AsyncClient, mock_admin):
    resp = await client.get("/api/v1/auth/logout")
    assert resp.status_code == 200, "logout is not working"

    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 401, "auth middleware is not working"

    resp = await client.post(
        "/api/v1/auth/login", json={"username": "notexist", "password": "incorrect"}
    )
    assert resp.status_code == 401, "login check failed"

    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": "incorrect"},
    )
    assert resp.status_code == 401, "login check failed"
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200, "login failed"
    resp = await client.get("/api/v1/auth/logout")
    assert resp.status_code == 200, "logout is not working"


@pytest.mark.asyncio
async def test_auth(client: AsyncClient, mock_admin):
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200, "login failed"
    result = resp.json()
    access_token = result["access_token"]
    assert access_token is not None

    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 200, "cookie auth middleware is not working"

    resp = await client.get("/api/v1/auth/logout")
    assert resp.status_code == 200, "logout is not working"

    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 401, (
        "logout is not working or auth middleware is not working"
    )

    resp = await client.get(
        "/api/v1/auth/me",
        auth=httpx.BasicAuth(mock_admin.username, mock_admin.username),
    )
    assert resp.status_code == 200, "basic auth middleware is not working"

    resp = await client.get(
        "/api/v1/auth/me", auth=httpx.BasicAuth("admin", "incorrect")
    )
    assert resp.status_code == 401, "basic auth middleware is not working"

    resp = await client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200, "token auth middleware is not working"

    resp = await client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token[0:10]}"}
    )
    assert resp.status_code == 401, "token auth middleware is not working"


@pytest.mark.asyncio
async def test_api_key(client: AsyncClient, mock_user):
    resp = await client.get("/api/v1/auth/logout")
    assert resp.status_code == 200, "logout is not working"

    api_key = "incorrect"
    resp = await client.get("/api/v1/auth/me", headers={"x-key": api_key})
    assert resp.status_code == 401, "api key middleware is not working"

    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_user.username, "password": mock_user.username},
    )
    assert resp.status_code == 200, "login failed"

    resp = await client.post("/api/v1/api_keys/my", params={"name": "api_key"})
    assert resp.status_code == 200, "create my api key failed"
    data = resp.json()
    api_key = data["api_key"]
    key_id = data["id"]

    resp = await client.get("/api/v1/auth/me", headers={"x-key": api_key})
    assert resp.status_code == 200, "api key middleware is not working"

    resp = await client.get("/api/v1/api_keys/my", headers={"x-key": api_key})
    assert resp.status_code == 200, "api key middleware is not working"
    assert len(resp.json()) > 0

    resp = await client.delete(
        f"/api/v1/api_keys/my/{key_id}", headers={"x-key": api_key}
    )
    assert resp.status_code == 200, "api key middleware is not working"


@pytest.mark.asyncio
async def test_root_role(client: AsyncClient, mock_user, mock_admin):
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_user.username, "password": mock_user.username},
    )
    assert resp.status_code == 200, "login failed"

    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 200, "cookie auth middleware is not working"

    resp = await client.get("/api/v1/users")
    assert resp.status_code == 401, "role checking is not working"

    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200, "login failed"

    resp = await client.get("/api/v1/users")
    assert resp.status_code == 200, "role checking is not working"

    result = resp.json()["items"]
    assert len(result) >= 2, "get user list failed"
    for i in result:
        if i["username"] not in [mock_admin.username, mock_user.username]:
            user_id = i["id"]
            resp = await client.delete(f"/api/v1/users/{user_id}")
            assert resp.status_code == 200, "user deletion failed"


@pytest.mark.asyncio
async def test_change_password(client: AsyncClient, mock_user):
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_user.username, "password": mock_user.username},
    )
    assert resp.status_code == 200, "login failed"

    resp = await client.post(
        "/api/v1/auth/change_password",
        json={"old_password": "incorrect", "new_password": "user"},
    )
    assert resp.status_code == 401, "failed to verify old password"

    resp = await client.post(
        "/api/v1/auth/change_password",
        json={"old_password": "user", "new_password": "new_password"},
    )
    assert resp.status_code == 200, "failed to change password"

    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_user.username, "password": "new_password"},
    )
    assert resp.status_code == 200, "failed to change password"

    resp = await client.post(
        "/api/v1/auth/change_password",
        json={"old_password": "new_password", "new_password": mock_user.username},
    )
    assert resp.status_code == 200, "failed to change password"
