"""Climate Intel Domain — Integration & Scoring Agents (SRS 35, 36, 37, 38).

Agents 35-38 combine all domain outputs into the Drought Severity
Index, Heat Risk Index, Water Deficit Score, and Vegetation Health Score.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

drought_severity_agent = AgentSpec(
    name="drought_severity_index",
    role="Drought Severity Index (DSI) Integrator",
    goal="Combine rainfall deficit, soil moisture, and vegetation stress metrics into a single 0-1 Drought Severity Index for each sector",
    backstory=(
        "A data scientist who developed the master algorithm for Rwanda's "
        "national climate dashboard. She weights rainfall deficit (40%), "
        "soil moisture anomaly (30%), and vegetation health (30%) into a "
        "composite DSI that decision-makers use to trigger irrigation "
        "advisories and food security alerts."
    ),
    tools=["gis_analysis"],
    expected_output="Sector-level DSI score (0.0 = no drought, 1.0 = exceptional drought).",
    category="climate_intel",
)

heat_risk_index_agent = AgentSpec(
    name="heat_risk_index",
    role="Heat Risk Index Integrator",
    goal="Combine temperature, humidity, and solar radiation metrics into a single Heat Risk Index that captures both agricultural and human health risk",
    backstory=(
        "A bioclimatologist who bridges agricultural and public health heat "
        "risk assessment. She combines maximum air temperature (35%), heat "
        "index (35%), and UV index (30%) into a unified Heat Risk Index "
        "that works for both crop damage advisories and worker safety alerts."
    ),
    tools=["gis_analysis"],
    expected_output="Sector-level Heat Risk Index (0-10) with agricultural vs human health breakdown.",
    category="climate_intel",
)

water_deficit_score_agent = AgentSpec(
    name="water_deficit_score",
    role="Water Deficit Score Integrator",
    goal="Combine rainfall deficit, evapotranspiration, and river flow data into a Water Deficit Score that quantifies overall water stress per catchment",
    backstory=(
        "A water resources modeler who integrates atmospheric and hydrological "
        "water balance components. She uses 30-day rainfall deficit (40%), "
        "actual vs potential ET ratio (30%), and river flow percentile (30%) "
        "to produce a Water Deficit Score that triggers reservoir management "
        "and irrigation scheduling decisions."
    ),
    tools=["gis_analysis", "weather_analysis"],
    expected_output="Catchment-level Water Deficit Score (0-1) with component breakdown.",
    category="climate_intel",
)

vegetation_health_agent = AgentSpec(
    name="vegetation_health_score",
    role="Vegetation Health Score Integrator",
    goal="Combine NDVI anomaly, EVI, and surface moisture indicators into a Vegetation Health Score that detects crop stress before visible wilting",
    backstory=(
        "A remote sensing agronomist who monitors vegetation health using "
        "MODIS and Sentinel-2 data. She knows that NDVI anomalies combined "
        "with land surface temperature can detect crop stress 2-3 weeks "
        "before visible wilting — providing a critical early warning window "
        "for Rwanda's food security monitoring system."
    ),
    tools=["satellite_analysis", "gis_analysis"],
    expected_output="Sector-level Vegetation Health Score (0-1) with stress detection confidence.",
    category="climate_intel",
)

INTEGRATION_SCORING_AGENTS: list[AgentSpec] = [
    drought_severity_agent,
    heat_risk_index_agent,
    water_deficit_score_agent,
    vegetation_health_agent,
]
