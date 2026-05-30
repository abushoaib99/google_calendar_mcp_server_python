#!/usr/bin/env python3
"""Run once locally to create token.json for FastMCP Cloud deployment."""

from pathlib import Path
import sys

# Allow running before install: uv run python scripts/oauth_setup.py
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from calendar_mcp.auth import get_credentials  # noqa: E402
from calendar_mcp.config import CREDENTIALS_PATH, TOKEN_PATH, validate_credentials_file  # noqa: E402


def main() -> None:
    print("Google Calendar MCP — OAuth setup\n")
    print(f"Expected credentials file: {CREDENTIALS_PATH}\n")

    try:
        validate_credentials_file()
    except FileNotFoundError as exc:
        print(exc)
        sys.exit(1)

    print("Opening browser for Google sign-in...")
    get_credentials()

    if not TOKEN_PATH.is_file():
        print("Error: token.json was not created.", file=sys.stderr)
        sys.exit(1)

    print(f"\nSuccess. Token saved to:\n  {TOKEN_PATH}\n")
    print("For FastMCP Cloud, copy these files into project secrets:")
    print("  GOOGLE_CREDENTIALS_JSON  ← full contents of credentials.json")
    print("  GOOGLE_TOKEN_JSON        ← full contents of token.json")
    print("\nSee docs/DEPLOYMENT.md")


if __name__ == "__main__":
    main()
