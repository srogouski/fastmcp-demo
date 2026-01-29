import os
from typing import Any, Dict, Optional

import httpx

BASE = os.getenv("DEMO_BASE", "http://localhost:8000")


async def list_business_units(base: Optional[str] = None) -> Dict[str, Any]:
    """Return the JSON response from /newsroom/business-units on the demo server."""
    b = (base or BASE).rstrip("/")
    url = f"{b}/newsroom/business-units"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=10.0)
        resp.raise_for_status()
        return resp.json()


async def list_users(
    base: Optional[str] = None, business_unit_id: Optional[int] = None
) -> Dict[str, Any]:
    """Return the JSON response from /newsroom/users. Optionally filter by business_unit_id."""
    b = (base or BASE).rstrip("/")
    url = f"{b}/newsroom/users"
    params: Dict[str, Any] = {}
    if business_unit_id is not None:
        params["business_unit_id"] = business_unit_id

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params or None, timeout=10.0)
        resp.raise_for_status()
        return resp.json()


__all__ = ["list_business_units", "list_users"]
