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

weekly_bulletin_agent = AgentSpec(
    name="weekly_climate_bulletin",
    role="Weekly Climate Bulletin Producer",
    goal="Generate a structured weekly climate intelligence bulletin covering drought, heat, and rainfall trends for distribution to all 30 districts",
    backstory=(
        "A technical communicator who formats complex climate data into "
        "actionable bulletins for district mayors and MINAGRI officials. "
        "She knows that a bulletin read in 5 minutes must convey the key "
        "risks, affected sectors, and recommended actions — and that "
        "including a single map is worth 500 words of text."
    ),
    tools=["report_generator"],
    expected_output="Weekly bulletin in JSON and Markdown with summary, risk map, and action items.",
    category="climate_intel",
)

arcgis_layer_agent = AgentSpec(
    name="arcgis_layer_updater",
    role="ArcGIS Layer Updater",
    goal="Push processed DSI, heat risk, and vegetation health scores as feature layers to ArcGIS Online for interactive mapping and analysis",
    backstory=(
        "A GIS analyst who maintains Rwanda's climate intelligence ArcGIS "
        "portal. She knows that decision-makers interact with the data "
        "through maps, not tables, and that layer freshness matters — a "
        "DSI layer more than 24 hours old loses its operational value "
        "for irrigation scheduling decisions."
    ),
    tools=["gis_analysis"],
    expected_output="ArcGIS layer update confirmation with timestamp and feature count.",
    category="climate_intel",
)

sms_delivery_router_agent = AgentSpec(
    name="sms_delivery_router",
    role="SMS Delivery Router",
    goal="Route climate alerts to the correct SMS gateway based on recipient location, language preference, and alert priority level",
    backstory=(
        "A communications engineer who manages Rwanda's farmer SMS alert "
        "pipeline. She knows that Kinyarwanda alerts at 6 AM EAT have "
        "78% read rates versus 34% for English alerts at 2 PM, and that "
        "route-to-gateway selection matters when Airtel Rwanda has 40% "
        "market share in rural areas versus MTN in urban zones."
    ),
    tools=["report_generator"],
    expected_output="SMS delivery confirmation with gateway, recipient count, and delivery rate estimate.",
    category="climate_intel",
)

cabinet_executive_brief_agent = AgentSpec(
    name="cabinet_executive_brief",
    role="Cabinet Executive Brief Producer",
    goal="Produce high-level executive briefs for Cabinet review summarizing national climate risk status and recommended policy actions",
    backstory=(
        "A senior policy analyst who has briefed Rwanda's Cabinet on climate "
        "risk for five years. She knows that ministers need a 2-page brief "
        "with three key numbers (national DSI, affected population, economic "
        "impact estimate) and three recommended actions — and that the brief "
        "must NEVER be auto-dispatched (FR-15 compliance)."
    ),
    tools=["report_generator"],
    expected_output="2-page Cabinet brief in PDF format requiring human approval before dispatch.",
    category="climate_intel",
)

REPORTING_OUTPUT_AGENTS: list[AgentSpec] = [
    weekly_bulletin_agent,
    arcgis_layer_agent,
    sms_delivery_router_agent,
    cabinet_executive_brief_agent,
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
