"""Sunshine & Heat Domain — Crop Heat Stress Agents (SRS 22, 23, 24).

Agents 22-24 track crop-specific heat thresholds for maize,
beans, and coffee respectively.
"""
from __future__ import annotations

from app.orchestration.registry import AgentSpec

maize_heat_stress_agent = AgentSpec(
    name="maize_heat_stress",
    role="Maize Heat Stress Analyst",
    goal="Detect when air temperature exceeds 30°C during maize critical growth stages (tasseling, silking, grain fill) and estimate yield impact",
    backstory=(
        "An agronomist specializing in heat stress physiology of C4 cereals. "
        "She knows that maize pollen viability drops sharply above 30°C, and "
        "that a 3-day exposure during tasseling can cause 30-50% kernel "
        "abortion — a loss invisible until harvest. She tracks Growing Degree "
        "Days alongside temperature extremes."
    ),
    tools=["weather_analysis"],
    expected_output="Maize heat stress alerts with growth-stage-specific yield loss estimate.",
    category="sunshine_heat",
)

beans_heat_stress_agent = AgentSpec(
    name="beans_heat_stress",
    role="Beans Heat Stress Analyst",
    goal="Detect when air temperature exceeds 32°C during bean flowering and pod-filling stages and calculate expected pod abortion rates",
    backstory=(
        "A pulse crop physiologist who understands that common beans are "
        "more heat-tolerant than maize but suffer catastrophic flower "
        "above 32°C. She monitors the critical 10-day flowering window "
        "and models pod-set reduction using established thermal response "
        "curves calibrated to Rwandan bean varieties."
    ),
    tools=["weather_analysis"],
    expected_output="Bean heat stress alerts with flowering-stage-specific pod loss estimate.",
    category="sunshine_heat",
)

coffee_heat_stress_agent = AgentSpec(
    name="coffee_heat_stress",
    role="Coffee Heat Stress Analyst",
    goal="Monitor temperature conditions at coffee-growing elevations (>1200m) and flag when temperatures exceed 28°C during cherry development",
    backstory=(
        "A coffee agronomist who knows that Arabica coffee in Rwanda grows "
        "between 1200-2000m, where temperatures above 28°C during cherry "
        "development cause premature ripening, reduced cup quality, and "
        "increased berry borer activity. She cross-references temperature "
        "with elevation to produce zone-specific advisories."
    ),
    tools=["weather_analysis", "gis_analysis"],
    expected_output="Coffee zone heat stress alerts with elevation-adjusted severity classification.",
    category="sunshine_heat",
)

CROP_HEAT_STRESS_AGENTS: list[AgentSpec] = [
    maize_heat_stress_agent,
    beans_heat_stress_agent,
    coffee_heat_stress_agent,
]
