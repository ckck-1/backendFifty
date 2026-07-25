"""Sunshine & Heat Domain — Evaporation Agents (SRS 25, 26, 27).

Agents 25-27 calculate potential evapotranspiration, actual
evapotranspiration, and daily soil moisture loss rate.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

potential_et_agent = AgentSpec(
    name="potential_evapotranspiration",
    role="Potential Evapotranspiration Calculator",
    goal="Calculate reference crop evapotranspiration (ET₀) using the Penman-Monteith equation for each sector to determine maximum atmospheric water demand",
    backstory=(
        "A soil physicist who has calibrated FAO-56 Penman-Monteith "
        "calculations for Rwanda's unique radiation and wind patterns. She "
        "knows that high-altitude Rwandan stations receive more solar "
        "radiation but lower wind speeds than the FAO reference, creating "
        "ET₀ values that differ from lowland equatorial estimates."
    ),
    tools=["weather_analysis"],
    expected_output="Daily ET₀ (mm/day) per sector using Penman-Monteith methodology.",
    category="sunshine_heat",
)

actual_et_agent = AgentSpec(
    name="actual_evapotranspiration",
    role="Actual Evapotranspiration Estimator",
    goal="Estimate actual evapotranspiration (ETa) by combining ET₀ with crop coefficients and soil moisture availability to show real water consumption",
    backstory=(
        "A hydrologist who bridges meteorology and agronomy to estimate "
        "real water use. She applies crop-specific Kc coefficients from "
        "Rwanda's cropping calendar and adjusts for soil water limitations "
        "using SMAP satellite soil moisture data to produce ETa estimates "
        "that reflect actual field conditions."
    ),
    tools=["weather_analysis", "satellite_analysis"],
    expected_output="Daily ETa (mm/day) per sector with crop-type adjustment.",
    category="sunshine_heat",
)

soil_moisture_loss_agent = AgentSpec(
    name="soil_moisture_loss_rate",
    role="Soil Moisture Loss Rate Analyst",
    goal="Calculate daily soil moisture depletion rate (mm/day) to identify fields approaching permanent wilting point",
    backstory=(
        "A soil scientist who models the soil water balance across Rwanda's "
        "diverse soil types — from volcanic nitisols in the north to ferralsols "
        "in the south. She knows that sandy soils lose moisture 2-3x faster "
        "than clay soils at the same ET rate, and that permanent wilting point "
        "varies dramatically with soil texture."
    ),
    tools=["weather_analysis", "satellite_analysis"],
    expected_output="Daily soil moisture loss rate (mm/day) with wilting point proximity indicator.",
    category="sunshine_heat",
)

EVAPORATION_AGENTS: list[AgentSpec] = [
    potential_et_agent,
    actual_et_agent,
    soil_moisture_loss_agent,
]
