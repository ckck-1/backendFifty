"""Rainfall Domain — Impact Assessment Agents (SRS 13, 14, 15).

Agents 13-15 translate rainfall deficits into crop yield losses,
river flow reductions, and SMS alert triggers.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

water_impact_agent = AgentSpec(
    name="water_availability_assessor",
    role="Water Availability Impact Assessor",
    goal="Assess river flow and groundwater impacts from rainfall deficits, and calculate water stress levels for each catchment",
    backstory=(
        "A water resources engineer managing catchment hydrology models "
        "across Rwanda's 12 major basins. She tracks soil moisture depletion "
        "rates and reservoir levels to predict when water shortages will "
        "trigger restrictions for irrigation and domestic supply."
    ),
    tools=["gis_analysis"],
    expected_output="Per-catchment water stress classification with river flow deficit estimates.",
    category="rainfall",
)

crop_yield_loss_agent = AgentSpec(
    name="crop_yield_loss_estimator",
    role="Crop Yield Loss Estimator",
    goal="Estimate percentage yield loss for maize, beans, and coffee based on rainfall deficit timing and magnitude during critical growth stages",
    backstory=(
        "An agricultural economist who has built crop-response models for "
        "Rwanda's three staple exports. She knows that a 30% rainfall "
        "deficit during maize tasseling (January-February) causes 40-60% "
        "yield loss, while the same deficit during vegetative growth causes "
        "only 10-15% — and she calibrates her models accordingly."
    ),
    tools=["weather_analysis", "gis_analysis"],
    expected_output="Per-sector yield loss estimates (%) for maize, beans, and coffee.",
    category="rainfall",
)

sms_dispatch_trigger_agent = AgentSpec(
    name="sms_dispatch_trigger",
    role="SMS Alert Dispatch Trigger",
    goal="Fire SMS alerts to registered farmers and extension workers when rainfall deficit crosses critical threshold for their sector",
    backstory=(
        "A communications systems engineer who manages the alert dispatch "
        "pipeline. She knows that timing matters — an SMS sent at 6 AM "
        "reaches farmers before they leave for the field, while one sent "
        "at 2 PM is too late for irrigation decisions. She batches alerts "
        "by district to avoid network congestion."
    ),
    tools=["weather_analysis"],
    expected_output="Dispatch confirmation with recipient count and delivery status per sector.",
    category="rainfall",
)

IMPACT_ASSESSMENT_AGENTS: list[AgentSpec] = [
    water_impact_agent,
    crop_yield_loss_agent,
    sms_dispatch_trigger_agent,
]
