"""
Tests for authentication and user endpoints.
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


# ========== Registration Tests ==========

@pytest.mark.asyncio
async def test_register_user_success(client):
    """Test successful user registration - happy path."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "StrongPass123!",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    # full_name is optional in the schema; test passes whether present or not
    if "full_name" in data:
        assert data["full_name"] == "Test User"
    # Security: Password hash must never be returned
    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    """Test registration fails with 400 when email already exists."""
    # First registration
    await client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "StrongPass123!"},
    )

    # Second attempt with same email
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "StrongPass123!"},
    )
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "already exists" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_weak_password(client):
    """Test registration fails with weak password (if validation enabled)."""
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "weak@example.com", "password": "123"},
    )
    # Expect 400 or 422 if password validation is implemented
    assert response.status_code in [400, 422]
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_register_invalid_email(client):
    """Test registration fails with malformed email."""
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "not-an-email", "password": "StrongPass123!"},
    )
    assert response.status_code in [400, 422]
    assert "detail" in response.json()


# ========== Login Tests ==========

@pytest.mark.asyncio
async def test_login_success(client):
    """Test successful login returns JWT token."""
    # Register first
    await client.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "password": "StrongPass123!"},
    )

    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "login@example.com", "password": "StrongPass123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 20  # JWT should be substantial


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    """Test login fails with wrong password."""
    await client.post(
        "/api/v1/auth/register",
        json={"email": "wrongpass@example.com", "password": "CorrectPass123!"},
    )

    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "wrongpass@example.com", "password": "WrongPass123!"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_login_nonexistent_user(client):
    """Test login fails for non-existent user."""
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "nonexistent@example.com", "password": "AnyPass123!"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_login_response_has_no_password(client):
    """Security: Login response must not contain password or hash."""
    await client.post(
        "/api/v1/auth/register",
        json={"email": "nopass@example.com", "password": "StrongPass123!"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "nopass@example.com", "password": "StrongPass123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "password" not in data
    assert "hashed_password" not in data


# ========== Profile (Protected Endpoint) Tests ==========
# Note: Profile endpoint is in /api/v1/users/me (users router), not /auth/*
# This matches the FastAPI template structure where auth handles login/register
# and users handles authenticated user operations.

@pytest.mark.asyncio
async def test_profile_authenticated(client):
    """Test authenticated profile endpoint returns user data."""
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={"email": "profile@example.com", "password": "StrongPass123!", "full_name": "Profile User"},
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "profile@example.com", "password": "StrongPass123!"},
    )
    token = login_resp.json()["access_token"]

    # Access profile with token
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "profile@example.com"
    if "full_name" in data:
        assert data["full_name"] == "Profile User"
    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_profile_unauthenticated(client):
    """Test profile endpoint returns 401 without token."""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_profile_invalid_token(client):
    """Test profile endpoint returns 401 with invalid token."""
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid.token.here"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_token_works_for_protected_endpoint(client):
    """Verify that the returned JWT token actually authorizes access."""
    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={"email": "token@example.com", "password": "StrongPass123!"},
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "token@example.com", "password": "StrongPass123!"},
    )
    token = login_resp.json()["access_token"]

    # Use token to access protected endpoint
    profile_resp = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert profile_resp.status_code == 200
    assert profile_resp.json()["email"] == "token@example.com"


@pytest.mark.asyncio
async def test_token_not_expired(client):
    """Verify that the returned JWT token has a future expiration."""
    from datetime import datetime
    import jwt
    from app.config import settings

    # Register and login
    await client.post(
        "/api/v1/auth/register",
        json={"email": "expiry@example.com", "password": "StrongPass123!"},
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "expiry@example.com", "password": "StrongPass123!"},
    )
    token = login_resp.json()["access_token"]

    # Decode without verification to check expiration claim
    decoded = jwt.decode(token, options={"verify_signature": False})
    exp_timestamp = decoded.get("exp")
    assert exp_timestamp is not None
    exp_datetime = datetime.fromtimestamp(exp_timestamp)
    assert exp_datetime > datetime.utcnow()


# ========== Future / TODO ==========
# TODO (v2.0): Add rate limiting test when implemented
# Rate limiting rule: "Implement rate limiting for public endpoints"