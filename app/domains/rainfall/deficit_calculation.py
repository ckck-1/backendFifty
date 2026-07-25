"""Rainfall Domain — Deficit Calculation Agents (SRS 4, 5, 6).

Agents 4-6 compare current rainfall against historical baselines
over 30-day, 90-day, and year-to-date windows.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

DEFICIT_CALCULATION_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=2,
        name="Rainfall Deficit Agent",
        role="Deficit Analyst",
        goal="Calculate 30 and 90-day rainfall deficits against historical baselines.",
        backstory="A hydrometeorologist focused on agricultural drought indices.",
        tools=["weather_analysis"],
        expected_output="Rainfall deficit percentages per sector.",
        category="rainfall",
    ),
]
