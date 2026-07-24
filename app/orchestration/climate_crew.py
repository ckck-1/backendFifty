"""ClimateCrew — sequential multi-agent orchestration via Mistral AI."""
from __future__ import annotations

import logging
import time
from typing import Any, Optional

logger = logging.getLogger(__name__)


class CrewOutput:
    """Simple container for crew execution results."""

    def __init__(self, raw: str, results: list[dict[str, str]]) -> None:
        self.raw = raw
        self.results = results

    def __str__(self) -> str:
        return self.raw


class ClimateCrew:
    """Runs a sequential pipeline of agents, each building on prior context."""

    def __init__(
        self,
        agents: list,
        location: str,
        query: str,
        prior_context: Optional[dict] = None,
    ) -> None:
        self.agents = agents
        self.location = location
        self.query = query
        self.prior_context = prior_context or {}

    def kickoff(self) -> CrewOutput:
        """Execute agents sequentially and return the aggregated output."""
        accumulated_context = ""
        results: list[dict[str, str]] = []

        for i, agent in enumerate(self.agents):
            t0 = time.time()
            task_desc = self._task_for_phase(i, agent)

            logger.info(
                "[%d/%d] Running agent: %s",
                i + 1,
                len(self.agents),
                agent.name,
            )

            output = agent.run(
                task_description=task_desc,
                context=accumulated_context,
                location=self.location,
            )

            elapsed_ms = int((time.time() - t0) * 1000)
            logger.info("  → %s completed in %d ms", agent.name, elapsed_ms)

            results.append({
                "agent": agent.name,
                "role": agent.role,
                "output": output,
                "elapsed_ms": str(elapsed_ms),
            })

            # Feed output as context for the next agent
            accumulated_context += f"\n\n[{agent.name}]:\n{output}"

        # Combine all outputs into a single report
        final_parts = []
        for r in results:
            final_parts.append(f"## {r['agent']} ({r['role']})\n\n{r['output']}")
        combined = "\n\n---\n\n".join(final_parts)

        return CrewOutput(raw=combined, results=results)

    def _task_for_phase(self, index: int, agent) -> str:
        """Generate the task description for each pipeline phase."""
        n = len(self.agents)

        if index == 0 and n >= 2:
            return (
                f"Analyse this climate intelligence request and create an "
                f"execution plan.\n\n"
                f"Location: {self.location}\nQuery: {self.query}\n"
                f"Prior context: {self.prior_context}\n\n"
                f"Identify which specialist analyses are needed and in what order."
            )
        elif index == n - 1:
            return (
                f"Generate a comprehensive climate intelligence report for "
                f"{self.location}.\n\n"
                f"Compile all preceding findings into a well-structured report.\n"
                f"Original query: {self.query}\n\n"
                f"Include: executive summary, methodology, detailed findings, "
                f"risk assessment, recommendations, and data sources."
            )
        elif index == n - 2 and n >= 3:
            return (
                f"Synthesise all preceding agent outputs into a single "
                f"coherent decision for {self.location}.\n\n"
                f"Query: {self.query}\n\n"
                f"Produce:\n"
                f"1) Risk level: CRITICAL / SEVERE / HIGH / MODERATE / LOW / NONE\n"
                f"2) Confidence score: 0.0 – 1.0\n"
                f"3) Key findings summary\n"
                f"4) Top 5 actionable recommendations\n"
                f"5) Uncertainties and caveats"
            )
        else:
            return (
                f"You are contributing to a climate intelligence analysis for "
                f"{self.location}.\n\n"
                f"Original query: {self.query}\n\n"
                f"Use your expertise to analyse relevant data and provide "
                f"findings for your area of specialty. Be specific and "
                f"quantitative where possible."
            )
