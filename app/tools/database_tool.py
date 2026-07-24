"""Tool for querying and storing intelligence reports via the memory service."""
from __future__ import annotations

import json
from datetime import datetime
from langchain_core.tools import tool
from app.services.memory import memory_service

@tool
def database_lookup(input_data: str) -> str:
    """Look up or store previous climate intelligence reports.
    Input should be a JSON string with 'action' ('store' or 'lookup') and
    a 'location' key, optionally followed by 'data' for storage.
    """
    try:
        payload = json.loads(input_data) if isinstance(input_data, str) else input_data
    except (json.JSONDecodeError, TypeError):
        payload = {"action": "lookup", "location": str(input_data)}

    action = payload.get("action", "lookup")
    location = payload.get("location", "unknown")

    if action == "store":
        key = f"report:{location}:{datetime.utcnow().isoformat()}"
        data = payload.get("data", {})
        memory_service.set(key, data)
        return f"Stored report for {location} under key {key}"

    # lookup
    store = memory_service._store
    keys = [k for k in store if location.lower() in k.lower()] if not memory_service._redis_client else []
    if not keys:
        return f"No previous reports found for {location}."
    latest_key = keys[-1]
    report = memory_service.get(latest_key)
    return f"Previous report ({latest_key}):\n{json.dumps(report, indent=2, default=str)}"
