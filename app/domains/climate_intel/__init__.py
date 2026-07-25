"""Climate Intelligence Domain — Agents 31-50 (SRS Domain 3)."""
from __future__ import annotations

from app.domains.climate_intel.trend_analysis import TREND_ANALYSIS_AGENTS
from app.domains.climate_intel.integration_scoring import INTEGRATION_SCORING_AGENTS
from app.domains.climate_intel.prediction_warning import PREDICTION_WARNING_AGENTS
from app.domains.climate_intel.sector_recommendations import SECTOR_RECOMMENDATION_AGENTS
from app.domains.climate_intel.reporting_output import REPORTING_OUTPUT_AGENTS

CLIMATE_INTEL_AGENTS: list = (
    TREND_ANALYSIS_AGENTS
    + INTEGRATION_SCORING_AGENTS
    + PREDICTION_WARNING_AGENTS
    + SECTOR_RECOMMENDATION_AGENTS
    + REPORTING_OUTPUT_AGENTS
)

__all__ = [
    "TREND_ANALYSIS_AGENTS",
    "INTEGRATION_SCORING_AGENTS",
    "PREDICTION_WARNING_AGENTS",
    "SECTOR_RECOMMENDATION_AGENTS",
    "REPORTING_OUTPUT_AGENTS",
    "CLIMATE_INTEL_AGENTS",
]
