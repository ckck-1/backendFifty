"""Sunshine & Heat Domain — Evaporation Agents (SRS 25, 26, 27).

Agents 25-27 calculate potential evapotranspiration, actual
evapotranspiration, and daily soil moisture loss rate.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

EVAPORATION_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=9,
        name="Evaporation Agent",
        role="Evapotranspiration Specialist",
        goal="Calculate daily potential and actual soil moisture loss.",
        backstory="A soil physicist modeling soil-plant-atmosphere continuums.",
        tools=["weather_analysis", "satellite_analysis"],
        expected_output="Daily evapotranspiration rates and soil drying metrics.",
        category="sunshine_heat",
    ),
]
