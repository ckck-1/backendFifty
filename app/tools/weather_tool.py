"""Weather analysis tool for climate intelligence."""
from __future__ import annotations

from langchain_core.tools import tool

@tool
def weather_analysis(location: str) -> str:
    """Analyse current and historical weather data for a location in Rwanda."""
    mock_data = {
        "Bugesera": {
            "current_temp_c": 28,
            "humidity_pct": 45,
            "rainfall_mm_30d": 12,
            "wind_speed_kmh": 18,
            "drought_index": 0.72,
            "soil_moisture_pct": 18,
            "evapotranspiration_mm": 5.2,
        },
        "default": {
            "current_temp_c": 25,
            "humidity_pct": 55,
            "rainfall_mm_30d": 35,
            "wind_speed_kmh": 12,
            "drought_index": 0.45,
            "soil_moisture_pct": 30,
            "evapotranspiration_mm": 3.8,
        },
    }
    data = mock_data.get(location, mock_data["default"])
    drought = data["drought_index"]

    if drought > 0.7:
        severity = "SEVERE"
    elif drought > 0.5:
        severity = "MODERATE"
    elif drought > 0.3:
        severity = "MILD"
    else:
        severity = "NONE"

    return (
        f"Weather Analysis for {location}:\n"
        f"  Temperature: {data['current_temp_c']}°C\n"
        f"  Humidity: {data['humidity_pct']}%\n"
        f"  Rainfall (30d): {data['rainfall_mm_30d']} mm\n"
        f"  Wind: {data['wind_speed_kmh']} km/h\n"
        f"  Drought Index: {drought} ({severity})\n"
        f"  Soil Moisture: {data['soil_moisture_pct']}%\n"
        f"  Evapotranspiration: {data['evapotranspiration_mm']} mm/day\n"
    )
