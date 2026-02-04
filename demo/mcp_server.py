from fastmcp import FastMCP

from demo.tools import list_business_units as _list_business_units
from demo.tools import list_users as _list_users
from demo.tools import get_apcbo_user as _get_apcbo_user


mcp = FastMCP("Newsroom")


@mcp.tool
async def list_business_units() -> dict:
    """MCP tool wrapper around the demo /newsroom/business-units endpoint."""
    return await _list_business_units()


@mcp.tool
async def list_users(business_unit_id: int | None = None) -> dict:
    """MCP tool wrapper around the demo /newsroom/users endpoint.

    `business_unit_id` is optional and will be passed through to the underlying
    HTTP endpoint as a query parameter.
    """
    return await _list_users(business_unit_id=business_unit_id)

@mcp.tool
async def get_user(app_id: int, user_id: int) -> dict:
    """Fetch a user from the real APCBO API."""
    return await _get_apcbo_user(app_id=app_id, user_id=user_id)

__all__ = ["mcp", "list_business_units", "list_users"]
