"""Cabinet brief approval endpoints — FR-15 / AC-07.

Operator-facing endpoints for reviewing and approving/rejecting
Cabinet-level emergency briefs before dispatch.
"""
from __future__ import annotations

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.schemas import ApprovalDecision, CabinetBriefResponse
from app.services.cabinet_service import cabinet_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/cabinet-briefs/pending", response_model=list[CabinetBriefResponse])
async def list_pending_briefs(db: AsyncSession = Depends(get_db)):
    """Return all Cabinet briefs awaiting human approval."""
    briefs = await cabinet_service.get_pending_briefs(db)
    return [
        CabinetBriefResponse(
            id=b.id,
            analysis_request_id=b.analysis_request_id,
            title=b.title,
            summary=b.summary,
            risk_level=b.risk_level,
            approval_status=b.approval_status.value,
            created_at=b.created_at,
            reviewed_by=b.reviewed_by,
            reviewed_at=b.reviewed_at,
        )
        for b in briefs
    ]


@router.get("/cabinet-briefs/{brief_id}", response_model=CabinetBriefResponse)
async def get_brief(brief_id: UUID, db: AsyncSession = Depends(get_db)):
    """Return a single Cabinet brief by ID."""
    brief = await cabinet_service.get_brief_by_id(db, brief_id)
    if brief is None:
        raise HTTPException(status_code=404, detail="Cabinet brief not found")
    return CabinetBriefResponse(
        id=brief.id,
        analysis_request_id=brief.analysis_request_id,
        title=brief.title,
        summary=brief.summary,
        risk_level=brief.risk_level,
        approval_status=brief.approval_status.value,
        created_at=brief.created_at,
        reviewed_by=brief.reviewed_by,
        reviewed_at=brief.reviewed_at,
    )


@router.post(
    "/cabinet-briefs/{brief_id}/approve",
    response_model=CabinetBriefResponse,
)
async def approve_brief(
    brief_id: UUID,
    decision: ApprovalDecision,
    db: AsyncSession = Depends(get_db),
):
    """Approve a Cabinet brief for dispatch.

    This is the ONLY path that allows a Cabinet brief to be sent.
    Requires explicit human operator approval per FR-15.
    """
    try:
        brief = await cabinet_service.approve_brief(
            db, brief_id, decision.reviewer_name
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # Trigger dispatch for approved brief
    await cabinet_service.dispatch_approved_brief(db, brief_id)

    return CabinetBriefResponse(
        id=brief.id,
        analysis_request_id=brief.analysis_request_id,
        title=brief.title,
        summary=brief.summary,
        risk_level=brief.risk_level,
        approval_status=brief.approval_status.value,
        created_at=brief.created_at,
        reviewed_by=brief.reviewed_by,
        reviewed_at=brief.reviewed_at,
    )


@router.post(
    "/cabinet-briefs/{brief_id}/reject",
    response_model=CabinetBriefResponse,
)
async def reject_brief(
    brief_id: UUID,
    decision: ApprovalDecision,
    db: AsyncSession = Depends(get_db),
):
    """Reject a Cabinet brief — it will NOT be dispatched."""
    try:
        brief = await cabinet_service.reject_brief(
            db, brief_id, decision.reviewer_name
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return CabinetBriefResponse(
        id=brief.id,
        analysis_request_id=brief.analysis_request_id,
        title=brief.title,
        summary=brief.summary,
        risk_level=brief.risk_level,
        approval_status=brief.approval_status.value,
        created_at=brief.created_at,
        reviewed_by=brief.reviewed_by,
        reviewed_at=brief.reviewed_at,
    )
