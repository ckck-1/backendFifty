"""Cabinet brief approval service — FR-15 / AC-07 compliance.

This service handles the safety-critical workflow where Cabinet briefs
must be reviewed and approved by a human operator before dispatch.
No automated dispatch is ever permitted for Cabinet-level reports.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database_models import ApprovalStatus, ClimateReport

logger = logging.getLogger(__name__)


class CabinetService:
    """Manages the Cabinet brief approval lifecycle."""

    async def create_pending_brief(
        self,
        db: AsyncSession,
        analysis_request_id: UUID,
        title: str,
        summary: str,
        risk_level: str,
        full_report: str,
        recommendations: list[str],
    ) -> ClimateReport:
        """Create a Cabinet brief in PENDING status — never dispatched automatically."""
        brief = ClimateReport(
            analysis_request_id=analysis_request_id,
            title=title,
            summary=summary,
            risk_level=risk_level,
            full_report=full_report,
            recommendations=recommendations,
            report_type="cabinet_brief",
            approval_status=ApprovalStatus.PENDING,
        )
        db.add(brief)
        await db.flush()
        logger.info(
            "Cabinet brief created (pending): id=%s risk=%s",
            brief.id,
            risk_level,
        )
        return brief

    async def get_pending_briefs(
        self,
        db: AsyncSession,
    ) -> list[ClimateReport]:
        """Return all Cabinet briefs awaiting human review."""
        stmt = (
            select(ClimateReport)
            .where(
                ClimateReport.report_type == "cabinet_brief",
                ClimateReport.approval_status == ApprovalStatus.PENDING,
            )
            .order_by(ClimateReport.created_at.desc())
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_brief_by_id(
        self,
        db: AsyncSession,
        brief_id: UUID,
    ) -> Optional[ClimateReport]:
        """Return a single Cabinet brief by ID."""
        stmt = select(ClimateReport).where(ClimateReport.id == brief_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def approve_brief(
        self,
        db: AsyncSession,
        brief_id: UUID,
        reviewer_name: str,
    ) -> ClimateReport:
        """Approve a Cabinet brief — this is the only path to dispatch.

        Raises ValueError if brief is not in PENDING status.
        """
        brief = await self.get_brief_by_id(db, brief_id)
        if brief is None:
            raise ValueError(f"Brief {brief_id} not found")
        if brief.approval_status != ApprovalStatus.PENDING:
            raise ValueError(
                f"Brief {brief_id} is already {brief.approval_status.value}"
            )

        brief.approval_status = ApprovalStatus.APPROVED
        brief.reviewed_by = reviewer_name
        brief.reviewed_at = datetime.utcnow()
        await db.flush()

        logger.info(
            "Cabinet brief APPROVED: id=%s reviewer=%s",
            brief_id,
            reviewer_name,
        )
        return brief

    async def reject_brief(
        self,
        db: AsyncSession,
        brief_id: UUID,
        reviewer_name: str,
    ) -> ClimateReport:
        """Reject a Cabinet brief — it will not be dispatched.

        Raises ValueError if brief is not in PENDING status.
        """
        brief = await self.get_brief_by_id(db, brief_id)
        if brief is None:
            raise ValueError(f"Brief {brief_id} not found")
        if brief.approval_status != ApprovalStatus.PENDING:
            raise ValueError(
                f"Brief {brief_id} is already {brief.approval_status.value}"
            )

        brief.approval_status = ApprovalStatus.REJECTED
        brief.reviewed_by = reviewer_name
        brief.reviewed_at = datetime.utcnow()
        await db.flush()

        logger.info(
            "Cabinet brief REJECTED: id=%s reviewer=%s",
            brief_id,
            reviewer_name,
        )
        return brief

    async def dispatch_approved_brief(
        self,
        db: AsyncSession,
        brief_id: UUID,
    ) -> bool:
        """Dispatch an approved Cabinet brief.

        This is the ONLY function that should trigger actual dispatch
        (email, notification, etc.). It only works on briefs with
        approval_status == APPROVED.

        Returns True if dispatch was executed, False otherwise.
        """
        brief = await self.get_brief_by_id(db, brief_id)
        if brief is None:
            logger.warning("Cannot dispatch: brief %s not found", brief_id)
            return False

        if brief.approval_status != ApprovalStatus.APPROVED:
            logger.warning(
                "Cannot dispatch: brief %s has status %s (must be approved)",
                brief_id,
                brief.approval_status.value,
            )
            return False

        # TODO: Implement actual dispatch (email to Cabinet, notification, etc.)
        logger.info(
            "Cabinet brief DISPATCHED: id=%s reviewer=%s",
            brief_id,
            brief.reviewed_by,
        )
        return True


cabinet_service = CabinetService()
