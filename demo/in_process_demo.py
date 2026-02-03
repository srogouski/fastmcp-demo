import asyncio
import json
import sys
from pathlib import Path

from starlette.testclient import TestClient

# Allow importing demo package from workspace root
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

# Import the ASGI app directly
from demo.demo_server import app

def main():
    with TestClient(app) as client:
        r = client.get("/status")
        print("/status ->", r.json())

        # Call the HTTP helper that invokes MCP tools server-side
        r2 = client.get("/tools/newsroom/list-business-units")
        print("/tools/newsroom/list-business-units ->", r2.status_code, r2.json())

if __name__ == '__main__':
    main()
