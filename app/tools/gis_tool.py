"""Geographic Information System analysis tool."""
from __future__ import annotations

from app.tools import BaseTool


class GISTool(BaseTool):
    """Performs spatial and geographic analysis for a sector."""

    name: str = "gis_analysis"
    description: str = (
        "Perform geographic and spatial analysis for a location in Rwanda. "
        "Input should be a location name string."
    )

    def _run(self, location: str) -> str:
        mock = {
            "Bugesera": {
                "lat": -2.2167,
                "lon": 30.2167,
                "elevation_m": 1420,
                "area_km2": 1326,
                "neighboring_sectors": ["Nyamata", "Rilima", "Juru", "Kabagali"],
                "water_bodies": ["Lake Cyahinda", "Rwambunga stream"],
                "drought_vulnerability": "high",
                "flood_risk": "moderate",
            },
            "default": {
                "lat": -1.9403,
                "lon": 29.8739,
                "elevation_m": 1567,
                "area_km2": 800,
                "neighboring_sectors": [],
                "water_bodies": [],
                "drought_vulnerability": "moderate",
                "flood_risk": "low",
            },
        }
        data = mock.get(location, mock["default"])
        neighbors = ", ".join(data["neighboring_sectors"]) or "N/A"
        waters = ", ".join(data["water_bodies"]) or "None"

        return (
            f"GIS Analysis for {location}:\n"
            f"  Coordinates: ({data['lat']}, {data['lon']})\n"
            f"  Elevation: {data['elevation_m']} m\n"
            f"  Area: {data['area_km2']} km²\n"
            f"  Neighbors: {neighbors}\n"
            f"  Water Bodies: {waters}\n"
            f"  Drought Vulnerability: {data['drought_vulnerability']}\n"
            f"  Flood Risk: {data['flood_risk']}\n"
        )
