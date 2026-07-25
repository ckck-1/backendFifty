"""Tests for the Cabinet brief approval workflow (FR-15 / AC-07)."""
from __future__ import annotations

import pytest
from datetime import datetime
from uuid import uuid4

from app.models.database_models import ApprovalStatus, ClimateReport


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


def test_climate_report_default_approval_status():
    """New ClimateReport defaults to PENDING approval status."""
    report = ClimateReport(
        analysis_request_id=uuid4(),
        title="Test Brief",
        summary="Test summary",
        full_report="Test full report",
    )
    assert report.approval_status == ApprovalStatus.PENDING
    assert report.reviewed_by is None
    assert report.reviewed_at is None
    assert report.report_type == "json"


def test_climate_report_cabinet_brief_type():
    """Cabinet briefs are tagged with report_type='cabinet_brief'."""
    report = ClimateReport(
        analysis_request_id=uuid4(),
        title="Cabinet Brief",
        summary="Emergency summary",
        full_report="Full emergency report",
        report_type="cabinet_brief",
    )
    assert report.report_type == "cabinet_brief"


@pytest.mark.anyio
async def test_create_pending_brief():
    """Creating a brief sets status to PENDING."""
    from app.services.cabinet_service import cabinet_service
    from app.core.database import async_session

    async with async_session() as db:
        brief = await cabinet_service.create_pending_brief(
            db=db,
            analysis_request_id=uuid4(),
            title="Test Brief",
            summary="Test summary",
            risk_level="SEVERE",
            full_report="Full report text",
            recommendations=["Rec 1", "Rec 2"],
        )
        assert brief.approval_status == ApprovalStatus.PENDING
        assert brief.report_type == "cabinet_brief"
        assert brief.risk_level == "SEVERE"
        await db.rollback()


@pytest.mark.anyio
async def test_approve_brief():
    """Approving a brief sets status to APPROVED with reviewer info."""
    from app.services.cabinet_service import cabinet_service
    from app.core.database import async_session

    async with async_session() as db:
        brief = await cabinet_service.create_pending_brief(
            db=db,
            analysis_request_id=uuid4(),
            title="Test Brief",
            summary="Test summary",
            risk_level="RED",
            full_report="Full report",
            recommendations=[],
        )
        approved = await cabinet_service.approve_brief(
            db, brief.id, "Operator Jean"
        )
        assert approved.approval_status == ApprovalStatus.APPROVED
        assert approved.reviewed_by == "Operator Jean"
        assert approved.reviewed_at is not None
        await db.rollback()


@pytest.mark.anyio
async def test_reject_brief():
    """Rejecting a brief sets status to REJECTED with reviewer info."""
    from app.services.cabinet_service import cabinet_service
    from app.core.database import async_session

    async with async_session() as db:
        brief = await cabinet_service.create_pending_brief(
            db=db,
            analysis_request_id=uuid4(),
            title="Test Brief",
            summary="Test summary",
            risk_level="ORANGE",
            full_report="Full report",
            recommendations=[],
        )
        rejected = await cabinet_service.reject_brief(
            db, brief.id, "Operator Paul"
        )
        assert rejected.approval_status == ApprovalStatus.REJECTED
        assert rejected.reviewed_by == "Operator Paul"
        assert rejected.reviewed_at is not None
        await db.rollback()


@pytest.mark.anyio
async def test_cannot_approve_already_approved():
    """Cannot approve a brief that is already approved."""
    from app.services.cabinet_service import cabinet_service
    from app.core.database import async_session

    async with async_session() as db:
        brief = await cabinet_service.create_pending_brief(
            db=db,
            analysis_request_id=uuid4(),
            title="Test Brief",
            summary="Test",
            risk_level="RED",
            full_report="Report",
            recommendations=[],
        )
        await cabinet_service.approve_brief(db, brief.id, "Op 1")
        with pytest.raises(ValueError, match="already"):
            await cabinet_service.approve_brief(db, brief.id, "Op 2")
        await db.rollback()


@pytest.mark.anyio
async def test_cannot_reject_already_rejected():
    """Cannot reject a brief that is already rejected."""
    from app.services.cabinet_service import cabinet_service
    from app.core.database import async_session

    async with async_session() as db:
        brief = await cabinet_service.create_pending_brief(
            db=db,
            analysis_request_id=uuid4(),
            title="Test Brief",
            summary="Test",
            risk_level="RED",
            full_report="Report",
            recommendations=[],
        )
        await cabinet_service.reject_brief(db, brief.id, "Op 1")
        with pytest.raises(ValueError, match="already"):
            await cabinet_service.reject_brief(db, brief.id, "Op 2")
        await db.rollback()


@pytest.mark.anyio
async def test_dispatch_only_works_on_approved():
    """dispatch_approved_brief returns False for non-approved briefs."""
    from app.services.cabinet_service import cabinet_service
    from app.core.database import async_session

    async with async_session() as db:
        brief = await cabinet_service.create_pending_brief(
            db=db,
            analysis_request_id=uuid4(),
            title="Test Brief",
            summary="Test",
            risk_level="RED",
            full_report="Report",
            recommendations=[],
        )
        # Pending — should not dispatch
        result = await cabinet_service.dispatch_approved_brief(db, brief.id)
        assert result is False

        # Reject — should not dispatch
        await cabinet_service.reject_brief(db, brief.id, "Op 1")
        result = await cabinet_service.dispatch_approved_brief(db, brief.id)
        assert result is False
        await db.rollback()
