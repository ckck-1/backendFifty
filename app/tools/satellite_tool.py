"""Satellite imagery processing tool."""
from __future__ import annotations

from app.tools import BaseTool


class SatelliteTool(BaseTool):
    """Processes satellite imagery for vegetation and land-cover analysis."""

    name: str = "satellite_analysis"
    description: str = (
        "Analyse satellite imagery (NDVI, land cover, moisture) for a location. "
        "Input should be a location name string."
    )

    def _run(self, location: str) -> str:
        mock = {
            "Bugesera": {
                "ndvi": 0.28,
                "land_cover": "sparse vegetation / agricultural",
                "surface_water_pct": 3.2,
                "vegetation_health": "stressed",
                "soil_exposure_pct": 62,
            },
            "default": {
                "ndvi": 0.45,
                "land_cover": "mixed agriculture and forest",
                "surface_water_pct": 8.5,
                "vegetation_health": "moderate",
                "soil_exposure_pct": 35,
            },
        }
        data = mock.get(location, mock["default"])
        ndvi = data["ndvi"]

        if ndvi < 0.2:
            veg_status = "CRITICAL — bare / dead vegetation"
        elif ndvi < 0.3:
            veg_status = "STRESSED — reduced greenness"
        elif ndvi < 0.5:
            veg_status = "MODERATE"
        else:
            veg_status = "HEALTHY"

        return (
            f"Satellite Analysis for {location}:\n"
            f"  NDVI: {ndvi} ({veg_status})\n"
            f"  Land Cover: {data['land_cover']}\n"
            f"  Surface Water: {data['surface_water_pct']}%\n"
            f"  Vegetation Health: {data['vegetation_health']}\n"
            f"  Soil Exposure: {data['soil_exposure_pct']}%\n"
        )
