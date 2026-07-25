"""Rainfall Domain — Data Collection Agents (SRS 1, 2, 3).

Agents 1-3 handle raw satellite rainfall data ingestion from three
independent sources: radar, infrared, and microwave sensors.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

DATA_COLLECTION_AGENTS: list[AgentSpec] = [
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
]
