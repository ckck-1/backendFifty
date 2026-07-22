"""High-level orchestration service for climate analysis requests."""
from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database_models import AgentResult, AnalysisRequest, ClimateReport
from app.services.memory import memory_service

logger = logging.getLogger(__name__)


class AnalysisService:
    """Coordinates the end-to-end analysis pipeline."""

    async def create_request(
        self,
        db: AsyncSession,
        location: str,
        query: str,
    ) -> AnalysisRequest:
        """Persist a new analysis request."""
        request = AnalysisRequest(
            id=uuid4(),
            location_name=location,
            query=query,
            status="pending",
        )
        db.add(request)
        await db.flush()
        return request

    async def mark_running(self, db: AsyncSession, request_id) -> None:
        stmt = select(AnalysisRequest).where(AnalysisRequest.id == request_id)
        result = await db.execute(stmt)
        req = result.scalar_one_or_none()
        if req:
            req.status = "running"
            await db.flush()

    async def complete_request(
        self,
        db: AsyncSession,
        request_id,
        summary: str,
        risk_level: str,
        confidence: float,
    ) -> None:
        stmt = select(AnalysisRequest).where(AnalysisRequest.id == request_id)
        result = await db.execute(stmt)
        req = result.scalar_one_or_none()
        if req:
            req.status = "completed"
            req.result_summary = summary
            req.risk_level = risk_level
            req.confidence = confidence
            req.completed_at = datetime.utcnow()
            await db.flush()

    async def fail_request(self, db: AsyncSession, request_id, error: str) -> None:
        stmt = select(AnalysisRequest).where(AnalysisRequest.id == request_id)
        result = await db.execute(stmt)
        req = result.scalar_one_or_none()
        if req:
            req.status = "failed"
            req.result_summary = f"Error: {error}"
            await db.flush()

    async def save_agent_result(
        self,
        db: AsyncSession,
        analysis_request_id,
        agent_name: str,
        agent_role: str,
        output: str,
        execution_time_ms: int = 0,
        confidence_score: float = 0.0,
    ) -> AgentResult:
        ar = AgentResult(
            id=uuid4(),
            analysis_request_id=analysis_request_id,
            agent_name=agent_name,
            agent_role=agent_role,
            output=output,
            status="completed",
            execution_time_ms=execution_time_ms,
            confidence_score=confidence_score,
        )
        db.add(ar)
        await db.flush()
        return ar

    async def save_report(
        self,
        db: AsyncSession,
        analysis_request_id,
        title: str,
        summary: str,
        risk_level: str,
        confidence: float,
        recommendations: list[str],
        full_report: str,
    ) -> ClimateReport:
        report = ClimateReport(
            id=uuid4(),
            analysis_request_id=analysis_request_id,
            title=title,
            summary=summary,
            risk_level=risk_level,
            confidence=confidence,
            recommendations=recommendations,
            full_report=full_report,
        )
        db.add(report)
        await db.flush()
        return report

    async def get_request_with_results(
        self, db: AsyncSession, request_id
    ) -> Optional[AnalysisRequest]:
        stmt = (
            select(AnalysisRequest)
            .where(AnalysisRequest.id == request_id)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()


analysis_service = AnalysisService()
