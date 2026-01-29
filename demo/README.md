# Demo: Client/Server API UI

Small demo showing a single-page UI that calls an API via the demo server.

Quick start

1. Create a virtual env and install deps:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r demo/requirements.txt
```

2. Run the server:

```bash
uvicorn demo.demo_server:app --reload --port 8000
```

3. Open http://localhost:8000 in your browser.

Usage

- Set `API Base` (saved in localStorage with the Save button).
- Enter `API Path/URL` (e.g. `/status`) and click `Call API`.
- The large dark area shows the returned JSON/text.
