#!/usr/bin/env python3
"""
Generate or refresh the Schwab OAuth token.

Run this script:
  - The first time to authenticate and create the token file.
  - Every 7 days to re-authenticate (refresh tokens expire after 7 days).

Usage:
    python scripts/generate_token.py

Environment variables (or .env file):
    SCHWAB_API_KEY       - Your Schwab app API key
    SCHWAB_APP_SECRET    - Your Schwab app secret
    SCHWAB_CALLBACK_URL  - OAuth callback URL (default: https://127.0.0.1:8182)
    SCHWAB_TOKEN_PATH    - Where to save the token (default: ./token.json in project root)
"""

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Load .env if present
env_file = Path(__file__).resolve().parent.parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

import schwab.auth  # noqa: E402


def main():
    api_key = os.environ.get("SCHWAB_API_KEY")
    app_secret = os.environ.get("SCHWAB_APP_SECRET")
    callback_url = os.environ.get("SCHWAB_CALLBACK_URL", "https://127.0.0.1:8182")
    project_root = Path(__file__).resolve().parent.parent
    raw_token_path = os.environ.get("SCHWAB_TOKEN_PATH", "")
    if raw_token_path:
        token_path = str(Path(raw_token_path).expanduser().resolve())
    else:
        token_path = str(project_root / "token.json")

    if not api_key or not app_secret:
        print("Error: SCHWAB_API_KEY and SCHWAB_APP_SECRET must be set.")
        print("Set them as environment variables or in the .env file.")
        sys.exit(1)

    token_file = Path(token_path)
    token_file.parent.mkdir(parents=True, exist_ok=True)

    # If token exists, show its age
    if token_file.exists():
        mtime = datetime.fromtimestamp(token_file.stat().st_mtime, tz=timezone.utc)
        age_days = (datetime.now(tz=timezone.utc) - mtime).total_seconds() / 86400
        print(f"Existing token: {token_file}")
        print(f"  Last modified: {mtime:%Y-%m-%d %H:%M:%S UTC}")
        print(f"  Age: {age_days:.1f} days (expires at 7 days)")

        if age_days < 6.5:
            print(f"\n  Token is still valid (~{7 - age_days:.1f} days remaining).")
            print("  Re-run this script when it's closer to expiry.")
            print("  To force re-auth, delete the token file and run again.")
            return

        print("\n  Token is expired or about to expire. Starting re-authentication...\n")
        token_file.unlink()

    # Start the manual OAuth flow
    print("=" * 60)
    print("  Schwab OAuth Authentication")
    print("=" * 60)
    print()
    print("Steps:")
    print("  1. A URL will be printed below")
    print("  2. Open it in your browser and log into Schwab")
    print("  3. After login, you'll be redirected (page may show an error)")
    print("  4. Copy the FULL URL from your browser's address bar")
    print("  5. Paste it back here")
    print()

    client = schwab.auth.client_from_manual_flow(
        api_key, app_secret, callback_url, token_path
    )

    print()
    print(f"Token saved to: {token_file}")
    print(f"Valid for 7 days (until ~{datetime.now(tz=timezone.utc).strftime('%Y-%m-%d')} + 7d)")
    print()
    print("The MCP server will auto-refresh access tokens within this window.")
    print("Re-run this script before the 7-day window expires.")


if __name__ == "__main__":
    main()
