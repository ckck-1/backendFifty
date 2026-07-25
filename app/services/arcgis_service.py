"""ArcGIS feature layer service for pushing climate intelligence to the dashboard."""
from __future__ import annotations

import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class ArcGISService:
    def __init__(self):
        self.api_key = settings.arcgis_api_key
        self.layer_url = settings.arcgis_feature_layer_url

    def _configured(self) -> bool:
        return bool(self.api_key and self.layer_url)

    async def update_sector_features(self, features: list[dict]) -> bool:
        """Push features to the ArcGIS feature layer.

        features: list of dicts like
        {"attributes": {"sector_name": "Nyagatare", "dsi": 0.74, "risk_level": "RED"},
         "geometry": {"x": lon, "y": lat}}
        """
        if not self._configured():
            logger.warning(
                "ArcGIS not configured yet (missing API key or layer URL) — skipping dashboard push"
            )
            return False

        url = f"{self.layer_url}/updateFeatures"
        payload = {
            "f": "json",
            "token": self.api_key,
            "features": features,
        }
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, data=payload, timeout=30)
                resp.raise_for_status()
                logger.info("ArcGIS layer updated: %d features", len(features))
                return True
        except Exception as e:
            logger.error("ArcGIS update failed: %s", e)
            return False


arcgis_service = ArcGISService()
