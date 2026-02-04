import os
from typing import Any, Dict, Optional

import httpx

# Existing demo base (your local FastAPI demo server)
DEMO_BASE = os.getenv("DEMO_BASE", "http://localhost:8000")

# New: APCBO base (real API)
APCBO_BASE = os.getenv("APCBO_BASE", "https://apcbo.aptechdevlab.com")

# Optional: if the real API ends up needing auth later, set this env var.
# Example: set APCBO_TOKEN="xxxxx" and we will send Authorization: Bearer <token>
APCBO_TOKEN = os.getenv("APCBO_TOKEN")


def _apcbo_headers() -> Dict[str, str]:
    headers = {"accept": "*/*"}
    if APCBO_TOKEN:
        headers["Authorization"] = f"Bearer {APCBO_TOKEN}"
    return headers


async def list_business_units(base: Optional[str] = None) -> Dict[str, Any]:
    """Return the JSON response from /newsroom/business-units on the demo server."""
    b = (base or DEMO_BASE).rstrip("/")
    url = f"{b}/newsroom/business-units"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=10.0)
        resp.raise_for_status()
        return resp.json()


async def list_users(
    base: Optional[str] = None, business_unit_id: Optional[int] = None
) -> Dict[str, Any]:
    """Return the JSON response from /newsroom/users. Optionally filter by business_unit_id."""
    b = (base or DEMO_BASE).rstrip("/")
    url = f"{b}/newsroom/users"
    params: Dict[str, Any] = {}
    if business_unit_id is not None:
        params["business_unit_id"] = business_unit_id

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params or None, timeout=10.0)
        resp.raise_for_status()
        return resp.json()


async def get_apcbo_user(app_id: int, user_id: int, base: Optional[str] = None) -> Dict[str, Any]:
    """
    Call the real APCBO endpoint:
      GET /api/users/{org_id}/{user_id}
    Example:
      https://apcbo.aptechdevlab.com/api/users/1/434369
    """
    b = (base or APCBO_BASE).rstrip("/")
    url = f"{b}/api/users/{app_id}/{user_id}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=_apcbo_headers(), timeout=10.0)
        resp.raise_for_status()
        return resp.json()


__all__ = ["list_business_units", "list_users", "get_apcbo_user"]
