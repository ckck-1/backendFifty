"""Climate Intel Domain — Reporting & Output Agents (SRS 47, 48, 49, 50).

Agents 47-50 generate weekly bulletins, ArcGIS layer updates,
SMS delivery routing, and Cabinet executive briefs.
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
