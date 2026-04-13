# START_MODULE_CONTRACT
# MODULE_NAME: M-AUTH
# PURPOSE: OAuth2 авторизация Google, кэширование токенов
# INPUTS: credentials_path (str), token_path (str), scopes (list[str])
# OUTPUTS: google.oauth2.credentials.Credentials
# ERRORS: AuthenticationError, TokenExpiredError
# END_MODULE_CONTRACT

"""Google OAuth2 authentication with token caching."""

import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# START_BLOCK_CONSTANTS
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/documents",
]

DEFAULT_CREDENTIALS_DIR = Path(__file__).parent.parent.parent / "credentials"
# END_BLOCK_CONSTANTS


# START_BLOCK_GET_CREDENTIALS
def get_credentials(
    credentials_path: str | None = None,
    token_path: str | None = None,
) -> Credentials:
    """Get valid Google API credentials, refreshing or re-authenticating as needed.

    On first run opens a browser for OAuth consent.
    Subsequent runs use the cached token.
    """
    if credentials_path is None:
        credentials_path = str(DEFAULT_CREDENTIALS_DIR / "client_secret.json")
    if token_path is None:
        token_path = str(DEFAULT_CREDENTIALS_DIR / "token.json")

    creds = None

    # Load cached token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Refresh or re-authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"Google OAuth credentials not found at {credentials_path}. "
                    f"Download from Google Cloud Console → APIs & Services → Credentials."
                )
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Cache token
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return creds
# END_BLOCK_GET_CREDENTIALS
