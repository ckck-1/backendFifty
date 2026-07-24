"""Agent model and factory for creating agents from registry specs."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from app.orchestration.registry import AgentSpec, ALL_AGENTS, get_agent_by_name, get_agents_by_ids
from app.services.mistral import mistral_service
from app.tools.weather_tool import weather_analysis
from app.tools.satellite_tool import satellite_analysis
from app.tools.gis_tool import gis_analysis
from app.tools.database_tool import database_lookup
from app.tools.report_tool import report_generator

logger = logging.getLogger(__name__)

# Map tool name strings to their instances
_TOOL_MAP: dict[str, Any] = {
    "weather_analysis": weather_analysis,
    "satellite_analysis": satellite_analysis,
    "gis_analysis": gis_analysis,
    "database_lookup": database_lookup,
    "report_generator": report_generator,
}


@dataclass
class Agent:
    """A runnable agent backed by Mistral AI."""

    name: str
    role: str
    goal: str
    backstory: str
    tools: list[Any] = field(default_factory=list)
    expected_output: str = ""
    category: str = ""
    id: int = 0

    def run(
        self,
        task_description: str,
        context: str = "",
        location: str = "",
    ) -> str:
        """Execute the agent's task by calling Mistral AI with tool outputs."""
        tool_outputs = self._gather_tools(location)

        system_prompt = (
            f"You are {self.name}, role: {self.role}.\n"
            f"Goal: {self.goal}\n"
            f"Background: {self.backstory}\n\n"
            f"Instructions:\n"
            f"- Analyse the data provided and give expert-level findings.\n"
            f"- Be specific, quantitative, and cite data points.\n"
            f"- Conclude with a risk assessment and confidence level.\n"
        )

        user_prompt = f"Location: {location}\n\n"
        if tool_outputs:
            user_prompt += "Available data:\n"
            for tool_name, output in tool_outputs.items():
                user_prompt += f"\n--- {tool_name} ---\n{output}\n"
        if context:
            user_prompt += f"\nPrior analysis context:\n{context}\n"
        user_prompt += f"\nTask:\n{task_description}\n"
        if self.expected_output:
            user_prompt += f"\nExpected output format:\n{self.expected_output}\n"

        try:
            result = mistral_service.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=4096,
            )
            logger.info("Agent '%s' completed task", self.name)
            return result
        except Exception as exc:
            logger.error("Agent '%s' failed: %s", self.name, exc)
            return f"[{self.name}] Error: {exc}"

    def _gather_tools(self, location: str) -> dict[str, str]:
        """Run all available tools and collect their outputs."""
        outputs: dict[str, str] = {}
        for tool in self.tools:
            try:
                outputs[tool.name] = tool.invoke(location)
            except Exception as exc:
                outputs[tool.name] = f"Tool error: {exc}"
        return outputs


class AgentFactory:
    """Creates Agent instances from AgentSpec blueprints."""

    def _resolve_tools(self, tool_names: list[str]) -> list:
        tools = []
        for name in tool_names:
            tool = _TOOL_MAP.get(name)
            if tool is not None:
                tools.append(tool)
            else:
                logger.warning("Unknown tool '%s' — skipping", name)
        return tools

    def build_agent(self, spec: AgentSpec) -> Agent:
        return Agent(
            id=spec.id,
            name=spec.name,
            role=spec.role,
            goal=spec.goal,
            backstory=spec.backstory,
            tools=self._resolve_tools(spec.tools),
            expected_output=spec.expected_output,
            category=spec.category,
        )

    def build_agents(self, specs: list[AgentSpec]) -> list[Agent]:
        return [self.build_agent(s) for s in specs]

    def build_by_names(self, names: list[str]) -> list[Agent]:
        specs = [get_agent_by_name(n) for n in names]
        specs = [s for s in specs if s is not None]
        return self.build_agents(specs)

    def build_by_ids(self, ids: list[int]) -> list[Agent]:
        return self.build_agents(get_agents_by_ids(ids))

    def build_all(self) -> list[Agent]:
        return self.build_agents(ALL_AGENTS)


agent_factory = AgentFactory()
