# User guide — Google Calendar MCP

This server reads **your** Google Calendar. You must provide Google OAuth credentials before it can work.

## Two ways to run the server

| Mode | Who sets up Google OAuth | Best for |
|------|--------------------------|----------|
| **Local (recommended)** | **You** — `credentials.json` in the project folder | Private use; each person uses their own calendar |
| **FastMCP Cloud URL** | **Server operator** — secrets in FastMCP Cloud | One shared hosted URL; one Google account per deployment |

If someone gave you a URL like `https://something.fastmcp.app/mcp`, you do **not** upload `credentials.json` yourself — ask the operator to complete [DEPLOYMENT.md](./DEPLOYMENT.md).

---

## Local setup (you use your own calendar)

### What you need

| File | Required | Description |
|------|----------|-------------|
| `credentials.json` | **Yes** | OAuth **Desktop app** client from **your** Google Cloud project |
| `token.json` | Auto | Created after you sign in with Google once |

Both files live in the **project root** (same folder as `pyproject.toml`). Never commit them to git.

### Step 1 — Get `credentials.json` from Google

1. Open [Google Cloud Console → Credentials](https://console.cloud.google.com/apis/credentials).
2. Create or select a project.
3. Enable [Google Calendar API](https://console.cloud.google.com/apis/library/calendar-json.googleapis.com).
4. Configure [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent).  
   - If the app is in **Testing**, add your Gmail under **Test users**.
5. **Create credentials** → **OAuth client ID** → type **Desktop app**.
6. Download the JSON file.
7. Rename it to `credentials.json` and place it here:

```text
google_calendar_mcp_server_python/
├── credentials.json    ← you add this
├── pyproject.toml
└── src/
```

Template:

```bash
cp credentials.json.example credentials.json
# then replace with your downloaded JSON (must include an "installed" section)
```

### Step 2 — Install dependencies

```bash
cd google_calendar_mcp_server_python
uv sync
```

### Step 3 — Sign in to Google (creates `token.json`)

```bash
uv run python -m calendar_mcp
```

A browser opens. Sign in with the Google account whose calendar you want. When finished, press Ctrl+C.  
`token.json` appears in the project root.

### Step 4 — Connect Cursor

In `~/.cursor/mcp.json` (use your real paths):

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

`cwd` **must** be the folder that contains your `credentials.json`.

Restart Cursor, then try: *“What’s on my calendar on 2026-05-30?”*

### Troubleshooting

| Problem | Fix |
|---------|-----|
| Error about missing `credentials.json` | Put the file in the project root; check `cwd` in MCP config |
| `invalid_client` | Use **Desktop app**, not Web client |
| `access_denied` / consent | Add yourself as a test user on the OAuth consent screen |
| Browser does not open | Run `uv run python -m calendar_mcp` manually once from the project folder |

---

## Using a hosted URL (FastMCP Cloud)

If you only have a URL:

```json
{
  "mcpServers": {
    "google-calendar-mcp": {
      "url": "https://YOUR-SERVER.fastmcp.app/mcp"
    }
  }
}
```

You **do not** add `credentials.json` on your machine. The person who deployed the server configured Google OAuth in FastMCP Cloud. All clients of that URL see the **same** Google Calendar (the account used at deploy time).

To use **your own** calendar, use **local setup** above instead.
