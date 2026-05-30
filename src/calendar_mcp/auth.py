from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from calendar_mcp.config import (
    CREDENTIALS_PATH,
    SCOPES,
    TOKEN_PATH,
    validate_credentials_file,
)

_creds: Credentials | None = None


def get_credentials() -> Credentials:
    """Load, refresh, or obtain OAuth credentials for the user's Google Calendar."""
    global _creds

    validate_credentials_file()

    if TOKEN_PATH.exists():
        _creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not _creds or not _creds.valid:
        if _creds and _creds.expired and _creds.refresh_token:
            _creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH), SCOPES
            )
            _creds = flow.run_local_server(
                port=0,
                access_type="offline",
                prompt="consent",
            )

        TOKEN_PATH.write_text(_creds.to_json(), encoding="utf-8")

    return _creds
