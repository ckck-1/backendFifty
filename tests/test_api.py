"""Tests for API endpoints."""
from __future__ import annotations

import pytest


@pytest.mark.anyio
async def test_root(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["project"] == "Project Fifty"
    assert data["status"] == "running"


@pytest.mark.anyio
async def test_list_agents(client):
    resp = await client.get("/agents")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] == 15
    assert len(data["agents"]) == 15
