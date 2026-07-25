"""Rainfall Domain — Impact Assessment Agents (SRS 13, 14, 15).

Agents 13-15 translate rainfall deficits into crop yield losses,
river flow reductions, and SMS alert triggers.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

IMPACT_ASSESSMENT_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=5,
        name="Water Impact Agent",
        role="Hydrology Specialist",
        goal="Assess river flow and groundwater impacts from rainfall deficits.",
        backstory="A water resources engineer managing catchment hydrology models.",
        tools=["gis_analysis"],
        expected_output="Water availability status and flow deficit analysis.",
        category="rainfall",
    ),
]
