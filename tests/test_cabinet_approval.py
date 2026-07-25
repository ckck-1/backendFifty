"""Tests for the Cabinet brief approval workflow (FR-15 / AC-07)."""
from __future__ import annotations

import pytest
import pytest_asyncio
from uuid import uuid4

from app.models.database_models import ApprovalStatus, ClimateReport, AnalysisRequest


# ── Sync unit tests (no DB) ─────────────────────────────────────

def test_approval_status_enum_values():
    """ApprovalStatus has exactly three states."""
    assert ApprovalStatus.PENDING.value == "pending"
    assert ApprovalStatus.APPROVED.value == "approved"
    assert ApprovalStatus.REJECTED.value == "rejected"


def test_approval_status_is_string_enum():
    """ApprovalStatus can be used as a string in comparisons."""
    assert ApprovalStatus.PENDING == "pending"
    assert ApprovalStatus.APPROVED != "pending"


def test_climate_report_has_approval_fields():
    """ClimateReport model has the required approval columns."""
    columns = {c.name for c in ClimateReport.__table__.columns}
    assert "approval_status" in columns
    assert "reviewed_by" in columns
    assert "reviewed_at" in columns
    assert "report_type" in columns


# ── Async DB tests (NullPool — no connection reuse) ─────────────

@pytest_asyncio.fixture
async def test_analysis_request():
    """Create a real AnalysisRequest row so FK constraints are satisfied.

    Uses NullPool session factory — each test gets its own connection,
    eliminating asyncpg concurrency errors.
    """
    from app.core.database import get_test_session_factory

    factory = get_test_session_factory()
    session = factory()
    try:
        req = AnalysisRequest(
            location_name="Test Sector",
            query="test query",
            status="completed",
        )
        session.add(req)
        await session.flush()
        req_id = req.id
        await session.commit()
        return req_id
    finally:
        await session.close()


@pytest.mark.asyncio
async def test_create_pending_brief(test_analysis_request):
    """Creating a brief sets status to PENDING."""
    from app.services.cabinet_service import cabinet_service
    from app.core.database import get_test_session_factory

    factory = get_test_session_factory()
    session = factory()
    try:
        brief = await cabinet_service.create_pending_brief(
            db=session,
            analysis_request_id=test_analysis_request,
            title="Test Brief",
            summary="Test summary",
            risk_level="SEVERE",
            full_report="Full report text",
            recommendations=["Rec 1", "Rec 2"],
        )
        await session.flush()
        await session.refresh(brief)
        assert brief.approval_status == ApprovalStatus.PENDING
        assert brief.report_type == "cabinet_brief"
        assert brief.risk_level == "SEVERE"
        await session.rollback()
    finally:
        await session.close()


@pytest.mark.asyncio
async def test_approve_brief(test_analysis_request):
    """Approving a brief sets status to APPROVED with reviewer info."""
    from app.services.cabinet_service import cabinet_service
    from app.core.database import get_test_session_factory

    factory = get_test_session_factory()
    session = factory()
    try:
        brief = await cabinet_service.create_pending_brief(
            db=session,
            analysis_request_id=test_analysis_request,
            title="Test Brief",
            summary="Test summary",
            risk_level="RED",
            full_report="Full report",
            recommendations=[],
        )
        approved = await cabinet_service.approve_brief(
            session, brief.id, "Operator Jean"
        )
        assert approved.approval_status == ApprovalStatus.APPROVED
        assert approved.reviewed_by == "Operator Jean"
        assert approved.reviewed_at is not None
        await session.rollback()
    finally:
        await session.close()


@pytest.mark.asyncio
async def test_reject_brief(test_analysis_request):
    """Rejecting a brief sets status to REJECTED with reviewer info."""
    from app.services.cabinet_service import cabinet_service
    from app.core.database import get_test_session_factory

    factory = get_test_session_factory()
    session = factory()
    try:
        brief = await cabinet_service.create_pending_brief(
            db=session,
            analysis_request_id=test_analysis_request,
            title="Test Brief",
            summary="Test summary",
            risk_level="ORANGE",
            full_report="Full report",
            recommendations=[],
        )
        rejected = await cabinet_service.reject_brief(
            session, brief.id, "Operator Paul"
        )
        assert rejected.approval_status == ApprovalStatus.REJECTED
        assert rejected.reviewed_by == "Operator Paul"
        assert rejected.reviewed_at is not None
        await session.rollback()
    finally:
        await session.close()


@pytest.mark.asyncio
async def test_cannot_approve_already_approved(test_analysis_request):
    """Cannot approve a brief that is already approved."""
    from app.services.cabinet_service import cabinet_service
    from app.core.database import get_test_session_factory

    factory = get_test_session_factory()
    session = factory()
    try:
        brief = await cabinet_service.create_pending_brief(
            db=session,
            analysis_request_id=test_analysis_request,
            title="Test Brief",
            summary="Test",
            risk_level="RED",
            full_report="Report",
            recommendations=[],
        )
        await cabinet_service.approve_brief(session, brief.id, "Op 1")
        with pytest.raises(ValueError, match="already"):
            await cabinet_service.approve_brief(session, brief.id, "Op 2")
        await session.rollback()
    finally:
        await session.close()


@pytest.mark.asyncio
async def test_cannot_reject_already_rejected(test_analysis_request):
    """Cannot reject a brief that is already rejected."""
    from app.services.cabinet_service import cabinet_service
    from app.core.database import get_test_session_factory

    factory = get_test_session_factory()
    session = factory()
    try:
        brief = await cabinet_service.create_pending_brief(
            db=session,
            analysis_request_id=test_analysis_request,
            title="Test Brief",
            summary="Test",
            risk_level="RED",
            full_report="Report",
            recommendations=[],
        )
        await cabinet_service.reject_brief(session, brief.id, "Op 1")
        with pytest.raises(ValueError, match="already"):
            await cabinet_service.reject_brief(session, brief.id, "Op 2")
        await session.rollback()
    finally:
        await session.close()


@pytest.mark.asyncio
async def test_dispatch_only_works_on_approved(test_analysis_request):
    """dispatch_approved_brief returns False for non-approved briefs."""
    from app.services.cabinet_service import cabinet_service
    from app.core.database import get_test_session_factory

    factory = get_test_session_factory()
    session = factory()
    try:
        brief = await cabinet_service.create_pending_brief(
            db=session,
            analysis_request_id=test_analysis_request,
            title="Test Brief",
            summary="Test",
            risk_level="RED",
            full_report="Report",
            recommendations=[],
        )
        # Pending — should not dispatch
        result = await cabinet_service.dispatch_approved_brief(session, brief.id)
        assert result is False

        # Reject — should not dispatch
        await cabinet_service.reject_brief(session, brief.id, "Op 1")
        result = await cabinet_service.dispatch_approved_brief(session, brief.id)
        assert result is False
        await session.rollback()
    finally:
        await session.close()
