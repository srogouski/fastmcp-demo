from fastmcp import FastMCP

from demo.tools import list_business_units as _list_business_units
from demo.tools import list_users as _list_users


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


__all__ = ["mcp", "list_business_units", "list_users"]
