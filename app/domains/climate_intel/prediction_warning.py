"""Climate Intel Domain — Prediction & Early Warning Agents (SRS 39, 40, 41, 42).

Agents 39-42 forecast future DSI, heatwaves, crop failure probability,
and livestock thermal comfort.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

PREDICTION_WARNING_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=13,
        name="Prediction and Warning Agent",
        role="Early Warning Specialist",
        goal="Forecast future DSI and crop failure probabilities using ML models.",
        backstory="A machine learning engineer building predictive early warning systems for food security.",
        tools=["database_lookup", "weather_analysis"],
        expected_output="30-day DSI predictions and 14-day crop failure probabilities.",
        category="climate_intel",
    ),
]
