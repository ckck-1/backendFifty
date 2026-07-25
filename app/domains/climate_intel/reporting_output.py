"""Climate Intel Domain — Reporting & Output Agents (SRS 47, 48, 49, 50).

Agents 47-50 generate weekly bulletins, ArcGIS layer updates,
SMS delivery routing, and Cabinet executive briefs.

FR-15 COMPLIANCE: Agent 50 (Cabinet brief) must NEVER dispatch
automatically. Briefs are created in PENDING status via
cabinet_service.create_pending_brief() and only dispatched after
explicit human operator approval via the /api/cabinet-briefs/ endpoints.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

REPORTING_OUTPUT_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=15,
        name="Reporting and Output Agent",
        role="Communication Specialist",
        goal="Format final data for Dashboards, SMS alerts, and PDF briefings.",
        backstory="A technical communicator who ensures alerts reach farmers and ministers in the right format.",
        tools=["report_generator"],
        expected_output="Structured JSON for dashboards, SMS text templates, and briefing summaries.",
        category="climate_intel",
    ),
]


async def create_cabinet_brief(
    analysis_request_id,
    title: str,
    summary: str,
    risk_level: str,
    full_report: str,
    recommendations: list[str],
) -> str:
    """Create a Cabinet brief in PENDING status (FR-15).

    This is the ONLY entry point for creating Cabinet briefs.
    The brief will NOT be dispatched until a human operator approves it
    via POST /api/cabinet-briefs/{id}/approve.

    Returns the brief ID as a string.
    """
    from app.services.cabinet_service import cabinet_service
    from app.core.database import async_session

    async with async_session() as db:
        brief = await cabinet_service.create_pending_brief(
            db=db,
            analysis_request_id=analysis_request_id,
            title=title,
            summary=summary,
            risk_level=risk_level,
            full_report=full_report,
            recommendations=recommendations,
        )
        await db.commit()
        return str(brief.id)
