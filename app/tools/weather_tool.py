"""Weather analysis tool for climate intelligence."""
from __future__ import annotations

from datetime import date, timedelta

import httpx
from langchain_core.tools import tool

NASA_POWER_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

SECTOR_COORDS: dict[str, tuple[float, float]] = {
    "nyarugenge": (-1.9536, 30.0605),
    "remera": (-1.9566, 30.106),
    "gikondo": (-1.9681, 30.0833),
    "nyamata": (-2.1472, 30.0864),
    "kigabiro": (-1.9483, 30.435),
    "mukarange": (-1.9422, 30.5458),
    "kabarore": (-1.5856, 30.4283),
    "nyagatare": (-1.2975, 30.3275),
    "kirehe": (-2.2683, 30.6517),
    "kibungo": (-2.1594, 30.5422),
    "ngoma": (-2.6067, 29.7394),
    "nyamabuye": (-2.0833, 29.75),
    "busasamana": (-2.3517, 29.7511),
    "ndora": (-2.6242, 29.8322),
    "kibeho": (-2.6672, 29.5528),
    "kigoma": (-2.2333, 29.7833),
    "gasaka": (-2.4678, 29.5683),
    "gacurabwenge": (-2.0333, 29.8667),
    "gisenyi": (-1.7, 29.25),
    "gihango": (-1.9, 29.3167),
    "bwishyura": (-2.0667, 29.35),
    "ngororero": (-1.8667, 29.5333),
    "mukamira": (-1.6333, 29.5167),
    "kagano": (-2.3667, 29.15),
    "kamembe": (-2.4833, 28.8999),
    "muhoza": (-1.4983, 29.635),
    "gahunga": (-1.4333, 29.8),
    "byumba": (-1.5761, 30.0675),
    "bushoki": (-1.7833, 29.9833),
    "gakenke": (-1.6833, 29.7833),
}

DEFAULT_COORDS = (-1.9536, 30.0605)


def _fetch_nasa_power(lat: float, lon: float, days_back: int = 7) -> dict:
    end_date = date.today()
    start_date = end_date - timedelta(days=days_back)

    params = {
        "parameters": "T2M,T2M_MAX,T2M_MIN,ALLSKY_SFC_SW_DWN,RH2M,PRECTOTCORR,WS2M",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_date.strftime("%Y%m%d"),
        "end": end_date.strftime("%Y%m%d"),
        "format": "JSON",
    }

    try:
        resp = httpx.get(NASA_POWER_URL, params=params, timeout=30)
        resp.raise_for_status()
        raw = resp.json().get("properties", {}).get("parameter", {})
        return {
            "air_temp_2m": {k: v for k, v in raw.get("T2M", {}).items() if v != -999.0},
            "air_temp_max": {k: v for k, v in raw.get("T2M_MAX", {}).items() if v != -999.0},
            "air_temp_min": {k: v for k, v in raw.get("T2M_MIN", {}).items() if v != -999.0},
            "solar_radiation": {k: v for k, v in raw.get("ALLSKY_SFC_SW_DWN", {}).items() if v != -999.0},
            "relative_humidity": {k: v for k, v in raw.get("RH2M", {}).items() if v != -999.0},
            "precipitation": {k: v for k, v in raw.get("PRECTOTCORR", {}).items() if v != -999.0},
            "wind_speed": {k: v for k, v in raw.get("WS2M", {}).items() if v != -999.0},
        }
    except Exception:
        return {}


def _get_latest_value(series: dict) -> float | None:
    for date_key in sorted(series.keys(), reverse=True):
        if series[date_key] != -999.0:
            return series[date_key]
    return None


@tool
def weather_analysis(location: str) -> str:
    """Analyse current and historical weather data for a location in Rwanda.

    Args:
        location: Sector or district name (e.g. "Nyagatare", "Bugesera").
    """
    coords = SECTOR_COORDS.get(location.lower(), DEFAULT_COORDS)
    lat, lon = coords

    data = _fetch_nasa_power(lat, lon)

    if not data:
        return f"Weather data unavailable for {location} (NASA POWER request failed)."

    temp = _get_latest_value(data.get("air_temp_2m", {}))
    temp_max = _get_latest_value(data.get("air_temp_max", {}))
    temp_min = _get_latest_value(data.get("air_temp_min", {}))
    humidity = _get_latest_value(data.get("relative_humidity", {}))
    solar = _get_latest_value(data.get("solar_radiation", {}))
    wind = _get_latest_value(data.get("wind_speed", {}))

    precip_values = [v for v in data.get("precipitation", {}).values() if v != -999.0]
    precip_7d = sum(precip_values) if precip_values else 0.0

    if precip_7d < 1.0:
        severity = "SEVERE"
    elif precip_7d < 5.0:
        severity = "MODERATE"
    elif precip_7d < 15.0:
        severity = "MILD"
    else:
        severity = "NONE"

    return (
        f"Weather Analysis for {location} ({lat}, {lon}):\n"
        f"  Temperature: {temp} C (min {temp_min} C, max {temp_max} C)\n"
        f"  Humidity: {humidity}%\n"
        f"  Solar Radiation: {solar} MJ/m2/day\n"
        f"  Rainfall (7d total): {precip_7d:.1f} mm\n"
        f"  Wind Speed: {wind} m/s\n"
        f"  Drought Severity: {severity}\n"
    )
