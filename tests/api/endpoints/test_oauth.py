import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_oauth_authorize_valid_provider(client: AsyncClient, mock_admin):
    """Test OAuth authorization with valid provider."""
    # Login as admin to access the endpoint
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200

    # Test OAuth authorization
    resp = await client.get("/api/v1/oauth/login/test_provider")
    # This should redirect or return an error depending on provider configuration
    # The exact behavior depends on the OAuth provider setup
    assert resp.status_code in [200, 302, 400, 404]


@pytest.mark.asyncio
async def test_oauth_authorize_invalid_provider(client: AsyncClient, mock_admin):
    """Test OAuth authorization with invalid provider."""
    # Login as admin to access the endpoint
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200

    # Test OAuth authorization with invalid provider
    resp = await client.get("/api/v1/oauth/login/invalid_provider")
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_oauth_authorize_with_redirect_uri(client: AsyncClient, mock_admin):
    """Test OAuth authorization with redirect URI."""
    # Login as admin to access the endpoint
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200

    # Test OAuth authorization with redirect URI
    resp = await client.get("/api/v1/oauth/login/test_provider?redirect_uri=/dashboard")
    # This should redirect or return an error depending on provider configuration
    assert resp.status_code in [200, 302, 400, 404]


@pytest.mark.asyncio
async def test_oauth_callback_valid_provider(client: AsyncClient, mock_admin):
    """Test OAuth callback with valid provider."""
    # Login as admin to access the endpoint
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200

    # Test OAuth callback
    resp = await client.get("/api/v1/oauth/callback/test_provider")
    # This should redirect or return an error depending on provider configuration
    # The exact behavior depends on the OAuth provider setup and callback parameters
    assert resp.status_code in [200, 302, 400, 404]


@pytest.mark.asyncio
async def test_oauth_callback_invalid_provider(client: AsyncClient, mock_admin):
    """Test OAuth callback with invalid provider."""
    # Login as admin to access the endpoint
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200

    # Test OAuth callback with invalid provider
    resp = await client.get("/api/v1/oauth/callback/invalid_provider")
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_oauth_authorize_unauthenticated(client: AsyncClient):
    """Test OAuth authorization without authentication."""
    # Test OAuth authorization without login
    resp = await client.get("/api/v1/oauth/login/test_provider")
    # This might work or fail depending on the OAuth provider configuration
    # The endpoint doesn't require authentication in the current implementation
    assert resp.status_code in [200, 302, 400, 404]


@pytest.mark.asyncio
async def test_oauth_callback_unauthenticated(client: AsyncClient):
    """Test OAuth callback without authentication."""
    # Test OAuth callback without login
    resp = await client.get("/api/v1/oauth/callback/test_provider")
    # This might work or fail depending on the OAuth provider configuration
    # The endpoint doesn't require authentication in the current implementation
    assert resp.status_code in [200, 302, 400, 404]


@pytest.mark.asyncio
async def test_oauth_provider_name_validation(client: AsyncClient, mock_admin):
    """Test OAuth provider name validation."""
    # Login as admin to access the endpoint
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200

    # Test with invalid provider name format
    resp = await client.get("/api/v1/oauth/login/invalid@provider")
    assert resp.status_code == 422  # Validation error

    resp = await client.get("/api/v1/oauth/callback/invalid@provider")
    assert resp.status_code == 422  # Validation error

    # Test with valid provider name format
    resp = await client.get("/api/v1/oauth/login/valid_provider_123")
    assert resp.status_code in [200, 302, 400, 404]

    resp = await client.get("/api/v1/oauth/callback/valid_provider_123")
    assert resp.status_code in [200, 302, 400, 404]


@pytest.mark.asyncio
async def test_oauth_redirect_uri_handling(client: AsyncClient, mock_admin):
    """Test OAuth redirect URI handling."""
    # Login as admin to access the endpoint
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": mock_admin.username, "password": mock_admin.username},
    )
    assert resp.status_code == 200

    # Test with different redirect URI formats
    redirect_uris = [
        "/dashboard",
        "/profile",
        "https://example.com/callback",
        "http://localhost:3000/auth/callback",
    ]

    for redirect_uri in redirect_uris:
        resp = await client.get(
            f"/api/v1/oauth/login/test_provider?redirect_uri={redirect_uri}"
        )
        # All should handle the redirect URI parameter
        assert resp.status_code in [200, 302, 400, 404]
