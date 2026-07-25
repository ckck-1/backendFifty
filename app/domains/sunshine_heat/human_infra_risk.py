"""Sunshine & Heat Domain — Human & Infrastructure Risk Agents (SRS 28, 29, 30).

Agents 28-30 map school heat risks, worker safety (WBGT),
and urban heat islands.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

HUMAN_INFRA_RISK_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=10,
        name="Human Risk Agent",
        role="Public Health Modeler",
        goal="Identify heat hazards for human populations and infrastructure.",
        backstory="An epidemiologist focused on environmental health and heat island effects.",
        tools=["gis_analysis"],
        expected_output="Wet-Bulb Globe Temperature warnings and vulnerable population mapping.",
        category="sunshine_heat",
    ),
]
