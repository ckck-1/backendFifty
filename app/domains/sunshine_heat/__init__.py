"""Sunshine & Heat Domain — Agents 16-30 (SRS Domain 2)."""
from __future__ import annotations

from app.domains.sunshine_heat.solar_radiation import SOLAR_RADIATION_AGENTS
from app.domains.sunshine_heat.temperature_stress import TEMPERATURE_STRESS_AGENTS
from app.domains.sunshine_heat.crop_heat_stress import CROP_HEAT_STRESS_AGENTS
from app.domains.sunshine_heat.evaporation import EVAPORATION_AGENTS
from app.domains.sunshine_heat.human_infra_risk import HUMAN_INFRA_RISK_AGENTS

SUNSHINE_HEAT_AGENTS: list = (
    SOLAR_RADIATION_AGENTS
    + TEMPERATURE_STRESS_AGENTS
    + CROP_HEAT_STRESS_AGENTS
    + EVAPORATION_AGENTS
    + HUMAN_INFRA_RISK_AGENTS
)

__all__ = [
    "SOLAR_RADIATION_AGENTS",
    "TEMPERATURE_STRESS_AGENTS",
    "CROP_HEAT_STRESS_AGENTS",
    "EVAPORATION_AGENTS",
    "HUMAN_INFRA_RISK_AGENTS",
    "SUNSHINE_HEAT_AGENTS",
]
