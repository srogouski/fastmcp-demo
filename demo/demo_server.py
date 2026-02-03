from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import httpx
import time
import asyncio
from fastmcp.tools.tool import ToolResult
from contextlib import asynccontextmanager
from fastmcp.utilities.lifespan import combine_lifespans

# import MCP server tools
from demo import mcp_server

# Create the MCP HTTP sub-app and combine lifespans so it's started with FastAPI
mcp_app = mcp_server.mcp.http_app()

@asynccontextmanager
async def app_lifespan(app):
    yield

app = FastAPI(title="Demo API Server", lifespan=combine_lifespans(app_lifespan, mcp_app.lifespan))

# Serve static UI
app.mount("/static", StaticFiles(directory="demo/static"), name="static")

# Mount MCP HTTP app so MCP endpoints are available under `/mcp`
app.mount("/mcp", mcp_app)


@app.get("/")
async def root():
    return FileResponse("demo/static/index.html")


@app.get("/status")
async def status():
    return {"status": "ok", "time": time.time()}


@app.post("/call")
async def call(req: Request):
    data = await req.json()
    base = data.get("base", "")
    path = data.get("path", "")
    if not base:
        return JSONResponse({"error": "base required"}, status_code=400)
    url = base.rstrip("/") + "/" + path.lstrip("/")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(url)
        return {"url": url, "status_code": r.status_code, "headers": dict(r.headers), "text": r.text}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/external/demo")
async def external_demo():
    # canned external API used by the UI for testing
    return {"service": "external-demo", "message": "hello from external demo", "time": time.time()}


# --- Newsroom resources (mock data for demo) ---------------------------------
BUSINESS_UNITS = [
    {"id": 1, "name": "Editorial", "slug": "editorial"},
    {"id": 2, "name": "Design", "slug": "design"},
    {"id": 3, "name": "Product", "slug": "product"},
]

USERS = [
    {"id": 101, "name": "Alice Ramos", "email": "alice@example.com", "role": "Editor", "business_unit_id": 1},
    {"id": 102, "name": "Ben Cho", "email": "ben@example.com", "role": "Designer", "business_unit_id": 2},
    {"id": 103, "name": "Cara Singh", "email": "cara@example.com", "role": "PM", "business_unit_id": 3},
    {"id": 104, "name": "Diego Ruiz", "email": "diego@example.com", "role": "Reporter", "business_unit_id": 1},
]


@app.get("/newsroom/business-units")
async def get_business_units():
    """Return a list of business units for the demo newsroom app."""
    return {"business_units": BUSINESS_UNITS}


@app.get("/newsroom/users")
async def get_users(business_unit_id: int | None = None):
    """Return users; optionally filter by `business_unit_id` query param."""
    if business_unit_id is not None:
        filtered = [u for u in USERS if u.get("business_unit_id") == business_unit_id]
        return {"users": filtered}
    return {"users": USERS}


# --- REST helpers that call MCP tools ---------------------------------------


@app.get("/tools/newsroom/list-business-units")
async def tools_list_business_units():
    """Call the MCP tool `list_business_units` and return its structured output."""
    result = await mcp_server.mcp.call_tool("list_business_units")
    # ToolResult contains `structured_content` when returning dict-like data
    if isinstance(result, ToolResult) and result.structured_content is not None:
        return result.structured_content
    # Fallback: return raw ToolResult as dict
    return result.dict()


@app.get("/tools/newsroom/list-users")
async def tools_list_users(business_unit_id: int | None = None):
    """Call the MCP tool `list_users` and return its structured output.

    Accepts optional `business_unit_id` query param.
    """
    args: dict = {}
    if business_unit_id is not None:
        args["business_unit_id"] = business_unit_id
    result = await mcp_server.mcp.call_tool("list_users", arguments=args or None)
    if isinstance(result, ToolResult) and result.structured_content is not None:
        return result.structured_content
    return result.dict()



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # send a single connected message, then wait for client requests
        await websocket.send_json({"msg": "connected", "time": time.time()})
        while True:
            # wait for client messages; if client never sends, server will simply keep the connection open
            await websocket.receive_text()
    except WebSocketDisconnect:
        # client disconnected
        return
