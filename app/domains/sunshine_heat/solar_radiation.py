"""Sunshine & Heat Domain — Solar Radiation Agents (SRS 16, 17, 18).

Agents 16-18 measure raw solar energy, UV index, and daily
bright sunshine hours.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

SOLAR_RADIATION_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=6,
        name="Solar Radiation Agent",
        role="Radiation Analyst",
        goal="Measure surface energy, UV index, and sunshine hours.",
        backstory="A solar physicist specializing in agricultural radiation budgets.",
        tools=["weather_analysis", "satellite_analysis"],
        expected_output="Solar radiation metrics and UV warnings.",
        category="sunshine_heat",
    ),
]
