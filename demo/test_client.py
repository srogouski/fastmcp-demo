import asyncio
import sys
from pathlib import Path

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

    # Import the FastMCP server object directly (in-process transport)
    from demo.mcp_server import mcp  # <-- this is the file containing your FastMCP("Newsroom")

    for i in range(10):
        try:
            async with Client(mcp) as client:
                tools = await client.list_tools()
                print("tools:", [t.name for t in tools])

                result = await client.call_tool("list_business_units", {})
                print("list_business_units:", result)

            return
        except Exception as e:
            print(f"Attempt {i + 1}: Client connection failed: {e}")
            await asyncio.sleep(1)

    print("Failed after retries")


if __name__ == "__main__":
    asyncio.run(main())
