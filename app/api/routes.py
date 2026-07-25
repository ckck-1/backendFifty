"""API route definitions for Project Fifty."""
from __future__ import annotations

from fastapi import APIRouter

from app.api.analysis import router as analysis_router
from app.api.cabinet import router as cabinet_router

router = APIRouter()

router.include_router(analysis_router, prefix="/api", tags=["analysis"])
router.include_router(cabinet_router, prefix="/api", tags=["cabinet"])


@router.get("/agents")
async def list_agents():
    """Return all 50 registered climate intelligence agents across 3 domains.

    Domains: Rainfall (15), Sunshine & Heat (15), Climate Intelligence (20).
    """
    from app.orchestration.registry import ALL_AGENTS
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
