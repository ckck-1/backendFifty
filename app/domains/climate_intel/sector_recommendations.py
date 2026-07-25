"""Climate Intel Domain — Sector Recommendation Agents (SRS 43, 44, 45, 46).

Agents 43-46 generate crop variety advice, reservoir release schedules,
cooling center identification, and infrastructure risk rankings.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

SECTOR_RECOMMENDATION_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=14,
        name="Sector Recommendation Agent",
        role="Policy Advisor",
        goal="Generate actionable advisories and resource allocation strategies for affected sectors.",
        backstory="A former MINAGRI extension officer who translates data into on-the-ground interventions.",
        tools=["gis_analysis"],
        expected_output="Specific agricultural and infrastructural recommendations per sector.",
        category="climate_intel",
    ),
]
