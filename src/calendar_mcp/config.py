import json
import os
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

CREDENTIALS_FILENAME = "credentials.json"
TOKEN_FILENAME = "token.json"


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


def credentials_setup_instructions() -> str:
    return (
        f"Place your Google OAuth client file at:\n"
        f"  {CREDENTIALS_PATH}\n\n"
        "Steps:\n"
        "  1. Open https://console.cloud.google.com/apis/credentials\n"
        "  2. Create an OAuth 2.0 Client ID (Application type: Desktop app)\n"
        "  3. Download the JSON and save it as credentials.json in the project root\n"
        "  4. Restart the MCP server; a browser opens on first use to sign in to Google\n\n"
        "See README.md for details."
    )


def validate_credentials_file(path: Path = CREDENTIALS_PATH) -> None:
    """Ensure credentials.json exists and is a Desktop OAuth client."""
    if not path.is_file():
        raise FileNotFoundError(credentials_setup_instructions())

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{path} is not valid JSON. Download a fresh OAuth client file from Google Cloud."
        ) from exc

    if "installed" not in data:
        raise ValueError(
            f"{path} must be a Desktop app OAuth client (JSON with an \"installed\" key). "
            "Web application credentials are not supported."
        )
