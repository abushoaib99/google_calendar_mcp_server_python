from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from calendar_mcp.config import (
    SCOPES,
    TOKEN_PATH,
    credentials_setup_instructions,
    load_client_config,
    load_token_data,
    uses_cloud_secrets,
)

_creds: Credentials | None = None


def get_credentials() -> Credentials:
    """Load, refresh, or obtain OAuth credentials for the user's Google Calendar."""
    global _creds

    client_config = load_client_config()
    token_data = load_token_data()

    if token_data:
        _creds = Credentials.from_authorized_user_info(token_data, SCOPES)

    if not _creds or not _creds.valid:
        if _creds and _creds.expired and _creds.refresh_token:
            _creds.refresh(Request())
        elif uses_cloud_secrets():
            raise FileNotFoundError(
                credentials_setup_instructions()
                + "\n\nGenerate token.json locally with: uv run python scripts/oauth_setup.py"
            )
        else:
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            _creds = flow.run_local_server(
                port=0,
                access_type="offline",
                prompt="consent",
            )

        if not uses_cloud_secrets():
            TOKEN_PATH.write_text(_creds.to_json(), encoding="utf-8")

    return _creds
