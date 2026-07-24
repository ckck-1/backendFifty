"""Rainfall Domain Agents (MVP) — Agents 1-5."""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

RAINFALL_AGENTS: list[AgentSpec] = [
    AgentSpec(
        id=1,
        name="Satellite Data Agent",
        role="Satellite Data Specialist",
        goal="Ingest and preprocess raw satellite data for rainfall and moisture.",
        backstory="A data engineer specialized in Earth Observation data pipelines.",
        tools=["satellite_analysis"],
        expected_output="Preprocessed satellite data grids ready for analysis.",
        category="rainfall",
    ),
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
    AgentSpec(
        id=5,
        name="Water Impact Agent",
        role="Hydrology Specialist",
        goal="Assess river flow and groundwater impacts from rainfall deficits.",
        backstory="A water resources engineer managing catchment hydrology models.",
        tools=["gis_analysis"],
        expected_output="Water availability status and flow deficit analysis.",
        category="rainfall",
    ),
]
