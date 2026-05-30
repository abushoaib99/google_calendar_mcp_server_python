# Google Calendar MCP Server (Python)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that connects to **your own** Google Calendar. Built with [FastMCP](https://github.com/jlowin/fastmcp) and the Google Calendar API.

Each user runs the server locally and authenticates with their Google account. No shared calendar or shared Google Cloud project is required beyond each user's own `credentials.json`.

## Quick start (use your own calendar)

### 1. Clone and install

```bash
git clone <your-repo-url>
cd google_calendar_mcp_server_python
uv sync
```

### 2. Add `credentials.json` at the project root

You **must** place a Google OAuth client file here (same folder as `pyproject.toml`):

```
google_calendar_mcp_server_python/
├── credentials.json   ← required (your file from Google)
├── pyproject.toml
└── ...
```

**How to get `credentials.json`:**

1. Open [Google Cloud Console → Credentials](https://console.cloud.google.com/apis/credentials).
2. Create or select a project and enable the [Google Calendar API](https://console.cloud.google.com/apis/library/calendar-json.googleapis.com).
3. Configure the [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent) (add yourself as a test user if the app is in testing mode).
4. Click **Create credentials** → **OAuth client ID** → application type **Desktop app**.
5. Download the JSON file and rename it to `credentials.json`.
6. Copy it to the **project root** (next to `pyproject.toml`).

Copy the template if helpful:

```bash
cp credentials.json.example credentials.json
# then replace placeholder values with your downloaded OAuth client JSON
```

The file must contain an `"installed"` block (Desktop app). Web client credentials are not supported.

### 3. Sign in once (creates `token.json`)

The first time the server needs your calendar, it opens a browser so you can sign in with **your** Google account. A `token.json` file is saved in the project root for later runs.

```bash
uv run python -m calendar_mcp
```

Stop the process after the browser sign-in completes (Ctrl+C). `token.json` is created automatically and is git-ignored.

### 4. Connect Cursor (or another MCP client)

Set `cwd` to the project root so the server finds your `credentials.json`:

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

Restart Cursor, then ask for events on a date. If `credentials.json` is missing, the tool returns an error with setup instructions.

## Features

- **Tool:** `get_my_calendar_data_by_date_tool` — list up to 10 events from your primary calendar for a given date
- **Per-user OAuth** — each user supplies their own `credentials.json` and signs in to their own Google account
- **Input validation** — dates are validated with Pydantic before calling the API

## Requirements

- Python **3.13+**
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Your own Google Cloud OAuth **Desktop app** client (`credentials.json`)

## Optional: custom project root

If the server cannot find `credentials.json`, set the root explicitly:

```bash
export CALENDAR_MCP_ROOT=/absolute/path/to/google_calendar_mcp_server_python
```

## Tool reference

| Tool | Description |
|------|-------------|
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

On error (e.g. missing `credentials.json`):

```json
{
  "error": "Place your Google OAuth client file at: ..."
}
```

## Project layout

```
google_calendar_mcp_server_python/
├── src/calendar_mcp/
│   ├── __main__.py
│   ├── server.py
│   ├── calendar.py
│   ├── auth.py
│   └── config.py
├── pyproject.toml
├── credentials.json.example   # template (safe to commit)
├── credentials.json           # your OAuth client (local only, required)
└── token.json                 # your sign-in token (local only, auto-created)
```

| File | Who provides it | Purpose |
|------|-----------------|--------|
| `credentials.json` | **You** (from Google Cloud) | OAuth client for your Google Cloud project |
| `token.json` | **Auto** (after browser sign-in) | Access to **your** Google Calendar |

## Security

- Do **not** commit `credentials.json` or `token.json` (listed in `.gitignore`).
- Read-only Calendar scope: `https://www.googleapis.com/auth/calendar.readonly`.
- Each machine/user has their own `token.json` tied to their Google account.

## License

No license file is included yet; add one if you plan to distribute this project.
