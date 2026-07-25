"""Sunshine & Heat Domain — Crop Heat Stress Agents (SRS 22, 23, 24).

Agents 22-24 track crop-specific heat thresholds for maize,
beans, and coffee respectively.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

CROP_HEAT_STRESS_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=8,
        name="Crop Heat Stress Agent",
        role="Crop Modeler",
        goal="Model specific heat stress thresholds for Maize, Beans, and Coffee.",
        backstory="An agricultural scientist with deep knowledge of Rwandan crop thermal limits.",
        tools=["weather_analysis"],
        expected_output="Crop-specific yield loss projections due to heat.",
        category="sunshine_heat",
    ),
]
