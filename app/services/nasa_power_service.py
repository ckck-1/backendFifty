"""NASA POWER API service for real weather data (temperature, solar, humidity, precipitation)."""
from __future__ import annotations

import logging
from datetime import date, timedelta

import httpx

logger = logging.getLogger(__name__)

NASA_POWER_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"


class NASAPowerService:
    async def get_weather_data(
        self, latitude: float, longitude: float, days_back: int = 7
    ) -> dict:
        end_date = date.today()
        start_date = end_date - timedelta(days=days_back)

        params = {
            "parameters": "T2M,T2M_MAX,T2M_MIN,ALLSKY_SFC_SW_DWN,RH2M,PRECTOTCORR,WS2M",
            "community": "AG",
            "longitude": longitude,
            "latitude": latitude,
            "start": start_date.strftime("%Y%m%d"),
            "end": end_date.strftime("%Y%m%d"),
            "format": "JSON",
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(NASA_POWER_URL, params=params)
                resp.raise_for_status()
                data = resp.json()
                return self._parse_response(data)
        except Exception as e:
            logger.error("NASA POWER fetch failed for (%s, %s): %s", latitude, longitude, e)
            return {}

    def _parse_response(self, data: dict) -> dict:
        raw = data.get("properties", {}).get("parameter", {})
        return {
            "air_temp_2m": {k: v for k, v in raw.get("T2M", {}).items() if v != -999.0},
            "air_temp_max": {k: v for k, v in raw.get("T2M_MAX", {}).items() if v != -999.0},
            "air_temp_min": {k: v for k, v in raw.get("T2M_MIN", {}).items() if v != -999.0},
            "solar_radiation": {k: v for k, v in raw.get("ALLSKY_SFC_SW_DWN", {}).items() if v != -999.0},
            "relative_humidity": {k: v for k, v in raw.get("RH2M", {}).items() if v != -999.0},
            "precipitation": {k: v for k, v in raw.get("PRECTOTCORR", {}).items() if v != -999.0},
            "wind_speed": {k: v for k, v in raw.get("WS2M", {}).items() if v != -999.0},
        }


nasa_power_service = NASAPowerService()
