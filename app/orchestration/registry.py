"""Master registry combining all 15 MVP agents from the three domains."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class AgentSpec:
    """Blueprint for a single agent."""
    id: int
    name: str
    role: str
    goal: str
    backstory: str
    tools: list[str] = field(default_factory=list)
    expected_output: str = ""
    category: str = ""

from app.domains.rainfall import RAINFALL_AGENTS
from app.domains.sunshine_heat import SUNSHINE_HEAT_AGENTS
from app.domains.climate_intel import CLIMATE_INTEL_AGENTS

ALL_AGENTS: list[AgentSpec] = (
    RAINFALL_AGENTS
    + SUNSHINE_HEAT_AGENTS
    + CLIMATE_INTEL_AGENTS
)

AGENT_CATEGORIES: dict[str, list[AgentSpec]] = {
    "rainfall": RAINFALL_AGENTS,
    "sunshine_heat": SUNSHINE_HEAT_AGENTS,
    "climate_intel": CLIMATE_INTEL_AGENTS,
}

def get_agent_by_name(name: str) -> Optional[AgentSpec]:
    """Return an AgentSpec by its exact name."""
    for agent in ALL_AGENTS:
        if agent.name.lower() == name.lower():
            return agent
    return None

def get_agents_by_category(category: str) -> list[AgentSpec]:
    """Return all agents in a given category."""
    return AGENT_CATEGORIES.get(category, [])

def get_agents_by_ids(ids: list[int]) -> list[AgentSpec]:
    """Return agents whose id is in the provided list."""
    id_set = set(ids)
    return [a for a in ALL_AGENTS if a.id in id_set]
