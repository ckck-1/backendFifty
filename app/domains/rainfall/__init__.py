"""Rainfall Domain — Agents 1-15 (SRS Domain 1)."""
from __future__ import annotations

from app.domains.rainfall.data_collection import DATA_COLLECTION_AGENTS
from app.domains.rainfall.deficit_calculation import DEFICIT_CALCULATION_AGENTS
from app.domains.rainfall.anomaly_detection import ANOMALY_DETECTION_AGENTS
from app.domains.rainfall.forecasting import FORECASTING_AGENTS
from app.domains.rainfall.impact_assessment import IMPACT_ASSESSMENT_AGENTS

RAINFALL_AGENTS: list = (
    DATA_COLLECTION_AGENTS
    + DEFICIT_CALCULATION_AGENTS
    + ANOMALY_DETECTION_AGENTS
    + FORECASTING_AGENTS
    + IMPACT_ASSESSMENT_AGENTS
)

__all__ = [
    "DATA_COLLECTION_AGENTS",
    "DEFICIT_CALCULATION_AGENTS",
    "ANOMALY_DETECTION_AGENTS",
    "FORECASTING_AGENTS",
    "IMPACT_ASSESSMENT_AGENTS",
    "RAINFALL_AGENTS",
]
