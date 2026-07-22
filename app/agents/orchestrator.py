"""Orchestrator — dynamically selects agents and runs the CrewAI pipeline."""
from __future__ import annotations

import logging
import time
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.factory import agent_factory
from app.agents.registry import ALL_AGENTS, get_agent_by_name
from app.crews.climate_crew import ClimateCrew
from app.services.analysis_service import analysis_service
from app.services.memory import memory_service

logger = logging.getLogger(__name__)

# Keyword → agent name mapping for dynamic selection
_KEYWORD_MAP: dict[str, list[str]] = {
    # weather / climate
    "drought": ["Drought Prediction Agent", "Weather Agent", "Soil Agent", "Water Availability Agent"],
    "flood": ["Flood Prediction Agent", "Rainfall Forecast Agent", "River Agent"],
    "rainfall": ["Rainfall Forecast Agent", "Weather Agent", "Climate Change Agent"],
    "temperature": ["Temperature Agent", "Extreme Weather Agent"],
    "fire": ["Fire Risk Agent", "Weather Agent", "Satellite Agent"],
    "weather": ["Weather Agent", "Satellite Agent"],
    "climate": ["Climate Change Agent", "Historical Climate Agent", "Environmental Risk Agent"],
    "extreme": ["Extreme Weather Agent", "Disaster Response Agent", "Emergency Planning Agent"],
    "water": ["Water Availability Agent", "River Agent"],
    "carbon": ["Carbon Agent", "Environmental Risk Agent"],
    # agriculture / food
    "crop": ["Agriculture Agent", "Farmer Advisor Agent", "NDVI Agent"],
    "farm": ["Agriculture Agent", "Farmer Advisor Agent", "Soil Agent"],
    "food": ["Food Security Agent", "Agriculture Agent"],
    "agriculture": ["Agriculture Agent", "Soil Agent", "NDVI Agent"],
    # population / society
    "population": ["Population Agent", "Economic Agent"],
    "health": ["Health Impact Agent"],
    "disaster": ["Disaster Response Agent", "Emergency Planning Agent"],
    "emergency": ["Emergency Planning Agent", "Disaster Response Agent"],
    "policy": ["Government Policy Agent", "Sustainability Agent"],
    "community": ["Community Alert Agent", "Education Agent"],
    # data quality
    "clean": ["Data Cleaning Agent", "Data Validation Agent"],
    "validate": ["Data Validation Agent", "Fact Checker Agent"],
    "pattern": ["Pattern Recognition Agent", "Anomaly Detection Agent"],
    "anomaly": ["Anomaly Detection Agent", "Pattern Recognition Agent"],
    "forecast": ["Forecasting Agent", "Simulation Agent"],
    "simulate": ["Simulation Agent", "Forecasting Agent"],
    "map": ["GIS Mapping Agent", "Satellite Agent"],
    "gis": ["GIS Mapping Agent"],
    "research": ["Research Agent", "Fact Checker Agent"],
    # report
    "report": ["Report Generator Agent", "Dashboard Agent"],
    "dashboard": ["Dashboard Agent"],
    "translate": ["Translation Agent"],
    "voice": ["Voice Assistant Agent"],
    "api": ["API Agent"],
    "satellite": ["Satellite Agent", "NDVI Agent"],
    "ndvi": ["NDVI Agent", "Satellite Agent"],
    "soil": ["Soil Agent", "Agriculture Agent"],
    "river": ["River Agent", "Water Availability Agent"],
    "sensor": ["Sensor Agent", "Weather Agent"],
    "history": ["Historical Climate Agent", "Climate Change Agent"],
    "economic": ["Economic Agent", "Resource Allocation Agent"],
    "sustainability": ["Sustainability Agent", "Government Policy Agent"],
    "education": ["Education Agent"],
    "resource": ["Resource Allocation Agent"],
    "alert": ["Community Alert Agent"],
    "confidence": ["Confidence Scoring Agent", "Quality Control Agent"],
    "quality": ["Quality Control Agent", "Data Validation Agent"],
}

# Agents always included in every analysis run
_BASE_AGENTS: list[str] = [
    "Orchestrator Agent",
    "Planning Agent",
    "Quality Control Agent",
    "Decision Agent",
    "Report Generator Agent",
]


class Orchestrator:
    """Analyses a user query, selects relevant agents, and runs the crew."""

    def __init__(self) -> None:
        pass

    # ── agent selection ────────────────────────────────────────────

    def select_agents(self, query: str) -> list[str]:
        """Return a list of agent names relevant to the user query."""
        query_lower = query.lower()
        selected: set[str] = set(_BASE_AGENTS)

        for keyword, agent_names in _KEYWORD_MAP.items():
            if keyword in query_lower:
                for name in agent_names:
                    selected.add(name)

        # Always include Memory Agent for context
        selected.add("Memory Agent")

        logger.info("Selected %d agents for query: %s", len(selected), query[:80])
        return list(selected)

    # ── pipeline execution ─────────────────────────────────────────

    async def run(
        self,
        location: str,
        query: str,
        db: Optional[AsyncSession] = None,
    ) -> dict:
        """Execute the full analysis pipeline and return the result dict."""
        t0 = time.time()

        # 1. Create analysis request if db available
        request_id = None
        if db:
            req = await analysis_service.create_request(db, location, query)
            request_id = req.id
            await analysis_service.mark_running(db, request_id)

        # 2. Select agents
        agent_names = self.select_agents(query)
        agent_specs = [get_agent_by_name(n) for n in agent_names]
        agent_specs = [s for s in agent_specs if s is not None]

        # 3. Build agents
        crew_agents = agent_factory.build_agents(agent_specs)

        # 4. Check memory for prior context
        prior_context = memory_service.get(f"context:{location}")

        # 5. Build and run crew
        try:
            crew = ClimateCrew(
                agents=crew_agents,
                location=location,
                query=query,
                prior_context=prior_context,
            )
            crew_output = crew.kickoff()

            # 6. Parse output
            result_text = str(crew_output)
            risk_level = self._extract_risk(result_text)
            confidence = self._extract_confidence(result_text)
            recommendations = self._extract_recommendations(result_text)

            # 7. Persist results
            if db and request_id:
                await analysis_service.complete_request(
                    db, request_id, result_text, risk_level, confidence
                )
                for spec in agent_specs:
                    await analysis_service.save_agent_result(
                        db, request_id, spec.name, spec.role, result_text
                    )
                await analysis_service.save_report(
                    db,
                    request_id,
                    title=f"Climate Intelligence Report — {location}",
                    summary=result_text[:500],
                    risk_level=risk_level,
                    confidence=confidence,
                    recommendations=recommendations,
                    full_report=result_text,
                )

            # 8. Cache for future memory lookups
            memory_service.set(f"context:{location}", {
                "location": location,
                "risk_level": risk_level,
                "confidence": confidence,
                "timestamp": time.time(),
            })

            elapsed = time.time() - t0
            logger.info("Analysis completed in %.1fs", elapsed)

            return {
                "location": location,
                "risk_level": risk_level,
                "confidence": str(confidence),
                "analysis": result_text,
                "recommendations": recommendations,
            }

        except Exception as exc:
            logger.error("Pipeline failed: %s", exc, exc_info=True)
            if db and request_id:
                await analysis_service.fail_request(db, request_id, str(exc))
            raise

    # ── output parsing helpers ─────────────────────────────────────

    @staticmethod
    def _extract_risk(text: str) -> str:
        text_lower = text.lower()
        if "risk level:" in text_lower:
            idx = text_lower.index("risk level:")
            snippet = text[idx: idx + 60]
            for level in ["critical", "severe", "high", "moderate", "mild", "low", "none"]:
                if level in snippet.lower():
                    return level.upper()
        if any(w in text_lower for w in ["severe drought", "critical", "extreme risk"]):
            return "SEVERE"
        if any(w in text_lower for w in ["high risk", "significant"]):
            return "HIGH"
        if any(w in text_lower for w in ["moderate", "medium"]):
            return "MODERATE"
        if any(w in text_lower for w in ["low risk", "mild", "minimal"]):
            return "LOW"
        return "MODERATE"

    @staticmethod
    def _extract_confidence(text: str) -> float:
        import re
        match = re.search(r"confidence[:\s]+(\d+(?:\.\d+)?)\s*%?", text, re.IGNORECASE)
        if match:
            val = float(match.group(1))
            return val if val <= 1.0 else val / 100.0
        return 0.75

    @staticmethod
    def _extract_recommendations(text: str) -> list[str]:
        import re
        lines = text.split("\n")
        recs: list[str] = []
        capture = False
        for line in lines:
            stripped = line.strip()
            if any(kw in stripped.lower() for kw in ["recommendation", "advise", "suggested action"]):
                capture = True
                continue
            if capture:
                if stripped.startswith(("- ", "* ", "• ")) or re.match(r"^\d+[\.\)]\s", stripped):
                    recs.append(re.sub(r"^[-*•]\s*|^\d+[\.\)]\s*", "", stripped).strip())
                elif stripped and not stripped.startswith(("=", "-")):
                    if recs:
                        break
        if not recs:
            recs = ["Monitor conditions closely", "Engage local agricultural extension services"]
        return recs[:10]


orchestrator = Orchestrator()
