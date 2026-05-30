# Deploy to FastMCP Cloud

Guide for **maintainers** who publish a hosted MCP URL.  
End users who only want their own calendar locally should follow [USER_GUIDE.md](./USER_GUIDE.md).

## Important: local vs cloud credentials

| | Local MCP | FastMCP Cloud |
|--|-----------|---------------|
| `credentials.json` at project root | **Each user** adds their own file | **Not used** — paste JSON into a secret |
| `token.json` | Auto after browser sign-in | Paste into a secret (see below) |
| Whose calendar? | Each user’s own | **One** Google account per deployment |

FastMCP Cloud cannot open a browser for each visitor. You complete OAuth **once on your machine**, then upload the token to FastMCP secrets. Everyone using that URL shares that calendar.

For many users with separate calendars, each user should run the server **locally** with their own `credentials.json` ([USER_GUIDE.md](./USER_GUIDE.md)).

---

## Prerequisites

- GitHub repository with this project
- `pyproject.toml` at repo root
- FastMCP entrypoint object: `mcp` in `src/calendar_mcp/server.py`

---

## Step 1 — Create `credentials.json` (local, one time)

Same as end users ([USER_GUIDE.md](./USER_GUIDE.md)):

1. Google Cloud → Calendar API enabled  
2. OAuth client type **Desktop app**  
3. Save as `credentials.json` in the project root  

Do **not** commit this file.

---

## Step 2 — Generate `token.json` (local, one time)

From the project root:

```bash
uv sync
uv run python scripts/oauth_setup.py
```

Sign in with the Google account that should back the **hosted** server.  
This writes `token.json` in the project root.

Verify the token includes a refresh token (open `token.json` and check `"refresh_token"` is present). If missing, delete `token.json` and run the script again.

---

## Step 3 — Push to GitHub

```bash
git add .
git commit -m "Prepare Google Calendar MCP server"
git push origin main
```

Ensure `credentials.json` and `token.json` are **not** in the commit (`.gitignore` covers them).

---

## Step 4 — Deploy on FastMCP Cloud

1. Open [fastmcp.cloud](https://fastmcp.cloud) (or [horizon.prefect.io](https://horizon.prefect.io)).
2. Sign in with **GitHub**.
3. **New project** → select your repository.
4. Set **entrypoint**:

   ```text
   src/calendar_mcp/server.py:mcp
   ```

5. Add **environment variables / secrets** (paste full JSON on one line each):

   | Name | Value |
   |------|--------|
   | `GOOGLE_CREDENTIALS_JSON` | Entire contents of `credentials.json` |
   | `GOOGLE_TOKEN_JSON` | Entire contents of `token.json` |

   Copy from terminal:

   ```bash
   # Linux — copies to clipboard if xclip is installed
   cat credentials.json | xclip -selection clipboard
   cat token.json | xclip -selection clipboard
   ```

6. Click **Deploy**.

When the build succeeds, you get a URL:

```text
https://<server-name>.fastmcp.app/mcp
```

Test with the platform Inspector or Chat before sharing.

---

## Step 5 — Tell users how to connect

Share this Cursor snippet (replace the URL):

```json
{
  "mcpServers": {
    "google-calendar-mcp": {
      "url": "https://YOUR-SERVER-NAME.fastmcp.app/mcp"
    }
  }
}
```

**Tell users clearly:**

- They do **not** need `credentials.json` on their PC for the hosted URL.
- The hosted server uses **your** Google Calendar (the account you used in Step 2).
- To use **their own** calendar, they must follow [USER_GUIDE.md](./USER_GUIDE.md) and run the server locally.

---

## Verify before deploy

```bash
uv run fastmcp inspect src/calendar_mcp/server.py:mcp
```

Optional local test with cloud-style env:

```bash
export GOOGLE_CREDENTIALS_JSON="$(cat credentials.json)"
export GOOGLE_TOKEN_JSON="$(cat token.json)"
uv run python -c "from calendar_mcp.calendar import get_events_by_date; print(get_events_by_date('2026-05-30'))"
```

---

## Redeploy and token refresh

- Pushing to `main` usually triggers automatic redeploy.
- Access tokens refresh in memory; `refresh_token` in `GOOGLE_TOKEN_JSON` should stay valid for months.
- If Google revokes access, run `scripts/oauth_setup.py` again and update `GOOGLE_TOKEN_JSON` in FastMCP Cloud.

---

## Checklist

- [ ] Calendar API enabled in Google Cloud  
- [ ] Desktop OAuth client → `credentials.json` (local only)  
- [ ] `scripts/oauth_setup.py` → `token.json` with `refresh_token`  
- [ ] GitHub repo without secrets committed  
- [ ] Entrypoint `src/calendar_mcp/server.py:mcp`  
- [ ] Secrets `GOOGLE_CREDENTIALS_JSON` and `GOOGLE_TOKEN_JSON` in FastMCP Cloud  
- [ ] User docs: hosted URL vs local `credentials.json` ([USER_GUIDE.md](./USER_GUIDE.md))
