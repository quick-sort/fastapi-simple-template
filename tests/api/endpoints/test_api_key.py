import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_my_api_keys(client: AsyncClient, mock_user):
    """Test listing user's own API keys."""
    # Login as user
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_user.username, "password": mock_user.username},
    )
    assert resp.status_code == 200

    # List my API keys
    resp = await client.get("/api/v1/api_keys/my")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_create_my_api_key(client: AsyncClient, mock_user):
    """Test creating a user's own API key."""
    # Login as user
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_user.username, "password": mock_user.username},
    )
    assert resp.status_code == 200

    # Create API key with name
    resp = await client.post("/api/v1/api_keys/my", params={"name": "test_key"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "test_key"
    assert "api_key" in data
    assert "id" in data

    # Create API key without name (should use default)
    resp = await client.post("/api/v1/api_keys/my")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "api_key"
    assert "api_key" in data


@pytest.mark.asyncio
async def test_delete_my_api_key(client: AsyncClient, mock_user):
    """Test deleting a user's own API key."""
    # Login as user
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_user.username, "password": mock_user.username},
    )
    assert resp.status_code == 200

    # Create an API key first
    resp = await client.post("/api/v1/api_keys/my", params={"name": "to_delete"})
    assert resp.status_code == 200
    key_data = resp.json()
    key_id = key_data["id"]

    # Delete the API key
    resp = await client.delete(f"/api/v1/api_keys/my/{key_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == key_id

    # Try to delete non-existent key
    resp = await client.delete("/api/v1/api_keys/my/99999")
    assert resp.status_code == 200  # Should still return success


@pytest.mark.asyncio
async def test_admin_create_api_key(client: AsyncClient, mock_admin, mock_user):
    """Test admin creating API key for another user."""
    # Login as admin
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200

    # Create API key for user
    resp = await client.post(
        "/api/v1/api_keys/",
        json={"user_id": mock_user.id, "name": "admin_created_key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["user_id"] == mock_user.id
    assert data["name"] == "admin_created_key"
    assert "api_key" in data


@pytest.mark.asyncio
async def test_admin_list_api_keys(client: AsyncClient, mock_admin, mock_user):
    """Test admin listing all API keys."""
    # Login as admin
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200

    # List all API keys
    resp = await client.get("/api/v1/api_keys/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

    # List API keys for specific user
    resp = await client.get(f"/api/v1/api_keys/?user_id={mock_user.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_admin_delete_api_key(client: AsyncClient, mock_admin, mock_user):
    """Test admin deleting any API key."""
    # Login as admin
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200

    # Create API key for user first
    resp = await client.post(
        "/api/v1/api_keys/",
        json={"user_id": mock_user.id, "name": "to_delete_by_admin"},
    )
    assert resp.status_code == 200
    key_data = resp.json()
    key_id = key_data["id"]

    # Delete the API key as admin
    resp = await client.delete(f"/api/v1/api_keys/{key_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == key_id


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """Test unauthorized access to API key endpoints."""
    # Try to access without authentication
    resp = await client.get("/api/v1/api_keys/my")
    assert resp.status_code == 401

    resp = await client.post("/api/v1/api_keys/my")
    assert resp.status_code == 401

    resp = await client.delete("/api/v1/api_keys/my/1")
    assert resp.status_code == 401

    resp = await client.get("/api/v1/api_keys/")
    assert resp.status_code == 401

    resp = await client.post("/api/v1/api_keys/")
    assert resp.status_code == 401

    resp = await client.delete("/api/v1/api_keys/1")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_user_cannot_access_admin_endpoints(client: AsyncClient, mock_user):
    """Test that regular users cannot access admin-only endpoints."""
    # Login as user
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_user.username, "password": mock_user.username},
    )
    assert resp.status_code == 200

    # Try to access admin endpoints
    resp = await client.get("/api/v1/api_keys/")
    assert resp.status_code == 401

    resp = await client.post("/api/v1/api_keys/", json={"user_id": 1, "name": "test"})
    assert resp.status_code == 401

    resp = await client.delete("/api/v1/api_keys/1")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_api_key_authentication(client: AsyncClient, mock_user):
    """Test API key authentication."""
    # Login and create API key
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_user.username, "password": mock_user.username},
    )
    assert resp.status_code == 200

    resp = await client.post("/api/v1/api_keys/my", params={"name": "auth_test"})
    assert resp.status_code == 200
    api_key_data = resp.json()
    api_key = api_key_data["api_key"]

    # Logout
    resp = await client.get("/api/v1/auth/logout")
    assert resp.status_code == 200

    # Use API key for authentication
    resp = await client.get("/api/v1/api_keys/my", headers={"x-key": api_key})
    assert resp.status_code == 200

    # Test with invalid API key
    resp = await client.get("/api/v1/api_keys/my", headers={"x-key": "invalid_key"})
    assert resp.status_code == 401
