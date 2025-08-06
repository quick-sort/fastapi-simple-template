import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_users_admin(client: AsyncClient, mock_admin, mock_user):
    """Test admin listing users with pagination."""
    # Login as admin
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200

    # List users with default pagination
    resp = await client.get("/api/v1/users/")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data
    assert "offset" in data
    assert "limit" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) >= 2  # At least admin and user

    # Test pagination parameters
    resp = await client.get("/api/v1/users/?offset=0&limit=1")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) == 1
    assert data["offset"] == 0
    assert data["limit"] == 1

    # Test with larger limit
    resp = await client.get("/api/v1/users/?limit=100")
    assert resp.status_code == 200
    data = resp.json()
    assert data["limit"] == 100


@pytest.mark.asyncio
async def test_list_users_unauthorized(client: AsyncClient, mock_user):
    """Test that regular users cannot list users."""
    # Login as regular user
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_user.username, "password": mock_user.username},
    )
    assert resp.status_code == 200

    # Try to list users
    resp = await client.get("/api/v1/users/")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_list_users_unauthenticated(client: AsyncClient):
    """Test that unauthenticated requests cannot list users."""
    resp = await client.get("/api/v1/users/")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_delete_user_unauthenticated(client: AsyncClient):
    """Test that unauthenticated requests cannot delete users."""
    resp = await client.delete("/api/v1/users/1")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_users_endpoints_with_api_key(client: AsyncClient, mock_admin):
    """Test users endpoints with API key authentication."""
    # Login as admin and create API key
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200

    resp = await client.post("/api/v1/api_keys/my", params={"name": "admin_key"})
    assert resp.status_code == 200
    api_key_data = resp.json()
    api_key = api_key_data["api_key"]

    # Logout
    resp = await client.get("/api/v1/auth/logout")
    assert resp.status_code == 200

    # Use API key to access users endpoints
    resp = await client.get("/api/v1/users/", headers={"x-key": api_key})
    assert resp.status_code == 200

    # Create a temporary user to delete
    # First login again to create a user
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200

    # Get users list to find a user to delete
    resp = await client.get("/api/v1/users/")
    assert resp.status_code == 200
    users_data = resp.json()

    assert len(users_data["items"]) == 2
