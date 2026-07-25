"""Climate Intel Domain — Integration & Scoring Agents (SRS 35, 36, 37, 38).

Agents 35-38 combine all domain outputs into the Drought Severity
Index, Heat Risk Index, Water Deficit Score, and Vegetation Health Score.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

INTEGRATION_SCORING_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=11,
        name="DSI Integration Agent",
        role="Index Synthesizer",
        goal="Combine rainfall, heat, and vegetation metrics into a single Drought Severity Index (DSI).",
        backstory="A data scientist who developed the master algorithm for the national climate dashboard.",
        tools=["gis_analysis"],
        expected_output="Final DSI score (0 to 1) for each sector.",
        category="climate_intel",
    ),
]
