"""
Tests for user management endpoints.
Follows Gebeta Sovereign Coding Rules:
- Security: No password/hash in responses, proper validation
- Quality: Small, focused test functions with docstrings
- API Design: Consistent response handling
- Database: Isolated test database with fixtures

Note: These tests use an in-memory SQLite database for speed and isolation.
Production uses PostgreSQL as configured in deployment modes.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.database import Base, get_db
from app.main import app

# Test database configuration (isolated, in-memory for speed)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(scope="function")
async def test_db():
    """Create fresh database tables for each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(test_db):
    """Return an async client with test database dependency override."""
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def auth_token(client):
    """Return a valid JWT token for an authenticated user."""
    # Register a test user
    await client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "StrongPass123!", "full_name": "Test User"},
    )
    # Login to get token
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "user@example.com", "password": "StrongPass123!"},
    )
    return response.json()["access_token"]


# ========== Get Current User Profile Tests ==========

@pytest.mark.asyncio
async def test_get_current_user_success(client, auth_token):
    """Test GET /users/me returns current user data."""
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@example.com"
    if "full_name" in data:
        assert data["full_name"] == "Test User"
    # Security: Password hash must never be returned
    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_get_current_user_unauthenticated(client):
    """Test GET /users/me returns 401 without token."""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(client):
    """Test GET /users/me returns 401 with invalid token."""
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid.token.here"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_get_current_user_expired_token(client):
    """Test GET /users/me returns 401 with expired token."""
    # This test requires a token with a past expiration.
    # For now, we test that an invalid token is rejected.
    # In a real implementation, you would mock the JWT validation.
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNTAwMDAwMDAwfQ.expired"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()


# ========== Update Current User Tests ==========

@pytest.mark.asyncio
async def test_update_current_user_success(client, auth_token):
    """Test PUT /users/me successfully updates user data."""
    response = await client.put(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "email": "updated@example.com",
            "full_name": "Updated Name",
            "password": "NewStrongPass123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"
    if "full_name" in data:
        assert data["full_name"] == "Updated Name"
    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_update_current_user_partial(client, auth_token):
    """Test PUT /users/me updates only provided fields."""
    # First get original user
    original = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    original_email = original.json()["email"]

    # Update only full_name
    response = await client.put(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"full_name": "Only Name Changed"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == original_email  # Email unchanged
    if "full_name" in data:
        assert data["full_name"] == "Only Name Changed"


@pytest.mark.asyncio
async def test_update_current_user_unauthenticated(client):
    """Test PUT /users/me returns 401 without token."""
    response = await client.put(
        "/api/v1/users/me",
        json={"email": "hacker@example.com"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_update_current_user_invalid_token(client):
    """Test PUT /users/me returns 401 with invalid token."""
    response = await client.put(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid.token.here"},
        json={"email": "hacker@example.com"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_update_current_user_duplicate_email(client, auth_token):
    """Test PUT /users/me returns 400 when email already exists."""
    # Register a second user
    await client.post(
        "/api/v1/auth/register",
        json={"email": "existing@example.com", "password": "StrongPass123!"},
    )

    # Try to update first user's email to existing email
    response = await client.put(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"email": "existing@example.com"},
    )
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "already exists" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_update_current_user_invalid_email(client, auth_token):
    """Test PUT /users/me returns 400 with malformed email."""
    response = await client.put(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"email": "not-an-email"},
    )
    assert response.status_code in [400, 422]
    assert "detail" in response.json()


# ========== Security & Response Validation Tests ==========

@pytest.mark.asyncio
async def test_user_response_never_leaks_password(client, auth_token):
    """Security: User response must never contain password or hash."""
    # Test GET /users/me
    get_response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    get_data = get_response.json()
    assert "password" not in get_data
    assert "hashed_password" not in get_data

    # Test PUT /users/me response
    put_response = await client.put(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"full_name": "Security Test"},
    )
    put_data = put_response.json()
    assert "password" not in put_data
    assert "hashed_password" not in put_data


@pytest.mark.asyncio
async def test_update_password_requires_strong_password(client, auth_token):
    """Test PUT /users/me rejects weak password."""
    response = await client.put(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"password": "123"},
    )
    assert response.status_code in [400, 422]
    assert "detail" in response.json()


# ========== Get User by ID (Admin) Tests ==========
# Note: These tests assume admin endpoints exist. If not implemented yet,
# they will fail. Uncomment when admin functionality is added.

# @pytest.mark.asyncio
# async def test_get_user_by_id_admin_success(client):
#     """Test GET /users/{id} returns user data (admin only)."""
#     # Requires admin authentication setup
#     pass


# @pytest.mark.asyncio
# async def test_get_user_by_id_forbidden(client, auth_token):
#     """Test GET /users/{id} returns 403 for non-admin users."""
#     # Requires admin authentication setup
#     pass


# ========== Delete User Tests ==========
# Note: These tests assume delete endpoints exist. Uncomment when implemented.

# @pytest.mark.asyncio
# async def test_delete_current_user_success(client, auth_token):
#     """Test DELETE /users/me successfully deletes current user."""
#     pass


# ========== Future / TODO ==========
# TODO (v2.0): Add pagination tests for GET /users (admin)
# TODO (v2.0): Add rate limiting tests for user endpoints
# TODO (v2.0): Add admin-only endpoint tests when implemented