"""Shared test fixtures."""
from __future__ import annotations

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest_asyncio.fixture
def anyio_backend():
    """Restrict anyio tests to asyncio only — asyncpg is not trio-compatible."""
    return "asyncio"


@pytest_asyncio.fixture
async def client():
    """Async HTTP client for testing API endpoints."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
