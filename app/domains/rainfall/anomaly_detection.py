"""Rainfall Domain — Anomaly Detection Agents (SRS 7, 8, 9).

Agents 7-9 detect long-term drying trends, dangerous cloudbursts,
and count consecutive dry days per sector.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

ANOMALY_DETECTION_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=3,
        name="Dry Spell Agent",
        role="Dry Spell Detector",
        goal="Detect consecutive dry days and flag anomalous drought patterns.",
        backstory="An agronomist who studies the impact of dry spells on crop phenology.",
        tools=["weather_analysis"],
        expected_output="Dry spell duration and anomaly flags.",
        category="rainfall",
    ),
]
