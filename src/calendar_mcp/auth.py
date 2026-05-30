from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from calendar_mcp.config import CREDENTIALS_PATH, SCOPES, TOKEN_PATH

_creds: Credentials | None = None


def get_credentials() -> Credentials:
    """Load, refresh, or obtain OAuth credentials for the Calendar API."""
    global _creds

    if TOKEN_PATH.exists():
        _creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not _creds or not _creds.valid:
        if _creds and _creds.expired and _creds.refresh_token:
            _creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                raise FileNotFoundError(
                    f"OAuth client secrets not found at {CREDENTIALS_PATH}"
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH), SCOPES
            )
            _creds = flow.run_local_server(port=0)

        TOKEN_PATH.write_text(_creds.to_json())

    return _creds
