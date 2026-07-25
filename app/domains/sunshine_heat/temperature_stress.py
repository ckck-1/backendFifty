"""Sunshine & Heat Domain — Temperature Stress Agents (SRS 19, 20, 21).

Agents 19-21 monitor ground surface temperature, air temperature,
and combined heat index.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

TEMPERATURE_STRESS_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=7,
        name="Temperature Agent",
        role="Thermal Analyst",
        goal="Analyze ground and air temperature stress and heatwaves.",
        backstory="A bioclimatologist studying thermal extremes in the Great Lakes region.",
        tools=["weather_analysis"],
        expected_output="Temperature anomaly and heat stress indices.",
        category="sunshine_heat",
    ),
]
