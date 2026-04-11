"""Tests for user endpoints."""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_get_current_user():
    """Test getting current user profile."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Register a user
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": "profile@example.com",
                "password": "testpassword123",
                "full_name": "Profile User",
            },
        )
        
        # Login to get token
        login_response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": "profile@example.com",
                "password": "testpassword123",
            },
        )
        token = login_response.json()["access_token"]
        
        # Get profile
        response = await client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["email"] == "profile@example.com"
