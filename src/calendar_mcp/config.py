import json
import os
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

CREDENTIALS_FILENAME = "credentials.json"
TOKEN_FILENAME = "token.json"

ENV_CREDENTIALS_JSON = "GOOGLE_CREDENTIALS_JSON"
ENV_TOKEN_JSON = "GOOGLE_TOKEN_JSON"


def find_project_root() -> Path:
    """Resolve the project root where users place credentials.json."""
    if root := os.environ.get("CALENDAR_MCP_ROOT"):
        return Path(root).expanduser().resolve()

    start = Path(__file__).resolve().parent
    for directory in (start, *start.parents):
        if (directory / "pyproject.toml").exists():
            return directory

    cwd = Path.cwd()
    if (cwd / CREDENTIALS_FILENAME).exists() or (cwd / "pyproject.toml").exists():
        return cwd

    return Path(__file__).resolve().parents[2]


PROJECT_ROOT = find_project_root()
CREDENTIALS_PATH = PROJECT_ROOT / CREDENTIALS_FILENAME
TOKEN_PATH = PROJECT_ROOT / TOKEN_FILENAME


def uses_cloud_secrets() -> bool:
    """True when OAuth config is supplied via environment (e.g. FastMCP Cloud)."""
    return bool(os.environ.get(ENV_CREDENTIALS_JSON))


def credentials_setup_instructions() -> str:
    if uses_cloud_secrets():
        return (
            "FastMCP Cloud deployment is missing Google OAuth configuration.\n\n"
            "The server operator must set these environment variables in the FastMCP Cloud project:\n"
            f"  - {ENV_CREDENTIALS_JSON}  (full contents of credentials.json)\n"
            f"  - {ENV_TOKEN_JSON}        (full contents of token.json after one local sign-in)\n\n"
            "See docs/DEPLOYMENT.md for the maintainer setup guide."
        )

    return (
        f"Place your Google OAuth client file at:\n"
        f"  {CREDENTIALS_PATH}\n\n"
        "Steps:\n"
        "  1. Open https://console.cloud.google.com/apis/credentials\n"
        "  2. Create an OAuth 2.0 Client ID (Application type: Desktop app)\n"
        "  3. Download the JSON and save it as credentials.json in the project root\n"
        "  4. Restart the MCP server; a browser opens on first use to sign in to Google\n\n"
        "See docs/USER_GUIDE.md for details."
    )


def _parse_json_env(name: str) -> dict:
    raw = os.environ.get(name, "").strip()
    if not raw:
        raise FileNotFoundError(credentials_setup_instructions())
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{name} must be valid JSON (paste the full credentials.json or token.json file)."
        ) from exc


def _validate_client_config(data: dict) -> dict:
    if "installed" not in data:
        raise ValueError(
            "OAuth client JSON must be a Desktop app (JSON with an \"installed\" key). "
            "Web application credentials are not supported."
        )
    return data


def load_client_config() -> dict:
    """OAuth client config from env (cloud) or credentials.json (local)."""
    if uses_cloud_secrets():
        return _validate_client_config(_parse_json_env(ENV_CREDENTIALS_JSON))

    validate_credentials_file()
    data = json.loads(CREDENTIALS_PATH.read_text(encoding="utf-8"))
    return _validate_client_config(data)


def load_token_data() -> dict | None:
    """Saved user token from env (cloud) or token.json (local), if present."""
    if os.environ.get(ENV_TOKEN_JSON):
        return _parse_json_env(ENV_TOKEN_JSON)
    if TOKEN_PATH.is_file():
        return json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
    return None


def validate_credentials_file(path: Path = CREDENTIALS_PATH) -> None:
    """Ensure credentials.json exists and is a Desktop OAuth client (local mode)."""
    if uses_cloud_secrets():
        return

    if not path.is_file():
        raise FileNotFoundError(credentials_setup_instructions())

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{path} is not valid JSON. Download a fresh OAuth client file from Google Cloud."
        ) from exc

    _validate_client_config(data)
