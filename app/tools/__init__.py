"""Base tool class for Project Fifty tools."""
from __future__ import annotations


class BaseTool:
    """Minimal base class replacing CrewAI's BaseTool."""

    name: str = ""
    description: str = ""

    def run(self, input_data: str) -> str:
        return self._run(input_data)

    def _run(self, input_data: str) -> str:
        raise NotImplementedError
