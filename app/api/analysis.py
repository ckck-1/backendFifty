"""Analysis API endpoints."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from app.models.schemas import AnalysisRequest, AnalysisResponse
from app.agents.orchestrator import orchestrator

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
    """Submit a climate analysis request.

    The orchestrator dynamically selects relevant agents from the 50-agent
    fleet, runs them through the multi-agent pipeline, and returns a
    structured intelligence report.
    """
    try:
        result = await orchestrator.run(
            location=request.location,
            query=request.query,
            db=None,
        )
        return AnalysisResponse(**result)
    except Exception as exc:
        logger.error("Analysis failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(exc)}")
