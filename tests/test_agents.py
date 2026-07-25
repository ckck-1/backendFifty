"""Tests for agent registry and factory."""
from __future__ import annotations

import pytest

from app.orchestration.registry import ALL_AGENTS, get_agent_by_name, get_agents_by_category
from app.orchestration.factory import agent_factory


def test_all_agents_count():
    assert len(ALL_AGENTS) >= 17


def test_agent_categories():
    rainfall = get_agents_by_category("rainfall")
    sunshine = get_agents_by_category("sunshine_heat")
    climate = get_agents_by_category("climate_intel")
    assert len(rainfall) >= 7
    assert len(sunshine) >= 5
    assert len(climate) >= 5


def test_get_agent_by_name():
    agent = get_agent_by_name("Radar Satellite Ingestion")
    assert agent is not None
    assert agent.id == 1


def test_factory_builds_agent():
    agent = get_agent_by_name("Radar Satellite Ingestion")
    built = agent_factory.build_agent(agent)
    assert built.name == "Radar Satellite Ingestion"
    assert built.role == "Radar Satellite Data Ingestion Specialist"
