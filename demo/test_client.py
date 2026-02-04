import asyncio
import sys
import json
from pathlib import Path

# ---------- Pretty printer for MCP CallToolResult ----------
def pretty_calltool(result) -> str:
    payload = result.data if result.data is not None else result.structured_content
    if payload is None and getattr(result, "content", None):
        payload = result.content[0].text
    return json.dumps(payload, indent=2)


# ---------- Parse dynamic arguments ----------
# Usage:
#   python demo/test_client.py <app_id> <user_id>
# Defaults:
#   app_id = 1
#   user_id = 434369
def parse_args():
    app_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    user_id = int(sys.argv[2]) if len(sys.argv) > 2 else 434369
    return app_id, user_id


# ---------- Path setup ----------
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

src_path = repo_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


try:
    from fastmcp.client import Client  # type: ignore
    HAVE_CLIENT = True
except Exception:
    HAVE_CLIENT = False


async def main():
    if not HAVE_CLIENT:
        print("FastMCP Client not available in this env.")
        return

    # Dynamic values
    app_id, user_id = parse_args()

    # In-process MCP server
    from demo.mcp_server import mcp  # FastMCP("Newsroom")

    for i in range(10):
        try:
            async with Client(mcp) as client:
                tools = await client.list_tools()
                print("tools:", [t.name for t in tools])

                user_result = await client.call_tool(
                    "get_user",
                    {
                        "app_id": app_id,
                        "user_id": user_id,
                    },
                )

                print("get_user:")
                print(pretty_calltool(user_result))

            return

        except Exception as e:
            print(f"Attempt {i + 1}: Client connection failed: {e}")
            await asyncio.sleep(1)

    print("Failed after retries")


if __name__ == "__main__":
    asyncio.run(main())
