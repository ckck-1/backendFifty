"""Climate Intel Domain — Long-Term Trend Analysis Agents (SRS 31, 32, 33, 34).

Agents 31-34 analyze decadal warming rates, rainy season shifts,
extreme event frequency, and season strength/duration changes.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

TREND_ANALYSIS_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=12,
        name="Trend Analysis Agent",
        role="Climate Historian",
        goal="Contextualize current events with decadal climate data and warming trends.",
        backstory="A long-term climate researcher maintaining 50 years of meteorological records.",
        tools=["database_lookup"],
        expected_output="Historical trend comparison and anomaly severity context.",
        category="climate_intel",
    ),
]
