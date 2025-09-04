import pytest
from httpx import AsyncClient
from main import app 

@pytest.mark.asyncio
async def test_signup_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Signup
        res = await ac.post("/auth/signup", json={
            "email": "test@example.com",
            "password": "password123"
        })
        assert res.status_code == 201

        # Login
        res = await ac.post("/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        assert res.status_code == 200
        assert "access_token" in res.json()

@pytest.mark.asyncio
async def test_protected_media_requires_auth():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post("/media", json={
            "title": "Sample video",
            "type": "video",
            "file_url": "http://example.com/video.mp4"
        })
        assert res.status_code == 401  # should fail without token
