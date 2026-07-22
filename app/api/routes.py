"""API route definitions for Project Fifty."""
from __future__ import annotations

from fastapi import APIRouter

from app.api.analysis import router as analysis_router

router = APIRouter()

router.include_router(analysis_router, prefix="/api", tags=["analysis"])


@router.get("/agents")
async def list_agents():
    """Return all 50 registered agents."""
    from app.agents.registry import ALL_AGENTS
    return {
        "count": len(ALL_AGENTS),
        "agents": [
            {
                "id": a.id,
                "name": a.name,
                "role": a.role,
                "goal": a.goal,
                "category": a.category,
                "tools": a.tools,
            }
            for a in ALL_AGENTS
        ],
    }
