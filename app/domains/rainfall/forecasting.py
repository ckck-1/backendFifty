"""Rainfall Domain — Forecasting Agents (SRS 10, 11, 12).

Agents 10-12 generate short-term (7-day), seasonal (3-month),
and ENSO-cycle rainfall forecasts.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

FORECASTING_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=4,
        name="Rainfall Forecast Agent",
        role="Precipitation Forecaster",
        goal="Generate short-term and seasonal rainfall forecasts.",
        backstory="A predictive modeler utilizing global weather models for local forecasts.",
        tools=["weather_analysis"],
        expected_output="7-day and seasonal rainfall probabilistic forecasts.",
        category="rainfall",
    ),
]
