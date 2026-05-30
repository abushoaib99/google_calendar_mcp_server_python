# Google Calendar MCP Server (Python)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that exposes your Google Calendar events to AI clients (e.g. Cursor). Built with [FastMCP](https://github.com/jlowin/fastmcp) and the Google Calendar API.

## Features

- **Tool:** `get_my_calendar_data_by_date_tool` — list up to 10 events from your primary calendar for a given date
- **OAuth 2.0** — desktop flow with token refresh; credentials are stored locally after the first sign-in
- **Input validation** — dates are validated with Pydantic before calling the API

## Requirements

- Python **3.13+**
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A Google Cloud project with the Calendar API enabled and OAuth 2.0 client credentials (Desktop app)

## Google Cloud setup

1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a project and enable the [Google Calendar API](https://console.cloud.google.com/apis/library/calendar-json.googleapis.com).
3. Configure the [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent).
4. Create **OAuth 2.0 Client ID** credentials of type **Desktop app**.
5. Download the JSON file and save it as `credentials.json` in the **project root** (next to `pyproject.toml`).

See also: [Calendar API Python quickstart](https://developers.google.com/workspace/calendar/api/quickstart/python).

## Installation

```bash
cd google_calendar_mcp_server_python
uv sync
```

Or with pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## First run (OAuth)

The first time the server needs calendar access, it opens a browser for Google sign-in and writes `token.json` in the project root.

```bash
uv run calendar-mcp
# or
uv run python -m calendar_mcp
```

If `credentials.json` is missing, the server raises `FileNotFoundError` with the expected path.

## Use with Cursor

Add the server to your MCP config. Use the **full path** to the venv Python — Cursor often runs MCP with a minimal `PATH`, so `"command": "uv"` frequently causes `connect_failure`:

```json
{
  "mcpServers": {
    "google-calendar-mcp": {
      "command": "/absolute/path/to/google_calendar_mcp_server_python/.venv/bin/python",
      "args": ["-m", "calendar_mcp"],
      "cwd": "/absolute/path/to/google_calendar_mcp_server_python"
    }
  }
}
```

Restart Cursor after changing MCP settings.

## Tool reference


| Tool                                | Description                                                      |
| ----------------------------------- | ---------------------------------------------------------------- |
| `get_my_calendar_data_by_date_tool` | Returns calendar events for `date` (ISO date, e.g. `2026-05-30`) |


**Example response:**

```json
{
  "meetings": [
    "Team standup at 2026-05-30T09:00:00+06:00",
    "Lunch at 2026-05-30"
  ]
}
```

On error:

```json
{
  "error": "description of the problem"
}
```

## Project layout

```
google_calendar_mcp_server_python/
├── src/
│   └── calendar_mcp/
│       ├── __init__.py
│       ├── __main__.py      # Entry point: python -m 
│       ├── server.py        # FastMCP tool registration
│       ├── calendar.py      # Calendar API and date 
│       ├── auth.py          # OAuth load / refresh / 
│       └── config.py        # Paths and scopes
├── pyproject.toml
├── uv.lock
├── README.md
├── .gitignore
├── credentials.json         # OAuth client secrets (local only)
└── token.json               # Saved user token (local only)
```


| Module     | Responsibility                               |
| ---------- | -------------------------------------------- |
| `config`   | `PROJECT_ROOT`, credential paths, API scopes |
| `auth`     | OAuth desktop flow and token persistence     |
| `calendar` | Pydantic input model and event fetching      |
| `server`   | MCP server instance and tool handler         |


## Security

- Do **not** commit `credentials.json` or `token.json`. They are listed in `.gitignore`.
- The server uses read-only scope: `https://www.googleapis.com/auth/calendar.readonly`.

## License

No license file is included yet; add one if you plan to distribute this project.