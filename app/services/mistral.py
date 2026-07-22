"""Mistral AI service — reusable client with retry and error handling."""
from __future__ import annotations

import logging
from typing import Optional

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class MistralService:
    """Wrapper around the Mistral AI API."""

    def __init__(self) -> None:
        self._api_key: str = settings.MISTRAL_API_KEY
        self._model: str = settings.MISTRAL_MODEL
        self._max_retries: int = settings.MISTRAL_MAX_RETRIES
        self._timeout: int = settings.MISTRAL_TIMEOUT

    def _get_client(self):
        """Create a fresh Mistral client."""
        from mistralai.client import Mistral
        return Mistral(api_key=self._api_key)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> str:
        """Send a completion request to Mistral with retry logic."""
        try:
            client = self._get_client()
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.complete(
                model=self._model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as exc:
            logger.error("Mistral API call failed: %s", exc)
            raise

    def validate_api_key(self) -> bool:
        """Return True if the API key is configured."""
        return bool(self._api_key)


# Module-level singleton
mistral_service = MistralService()
