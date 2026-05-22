import os
from pathlib import Path

import schwab.auth

_client = None


def get_client():
    global _client
    if _client is not None:
        return _client

    api_key = os.environ["SCHWAB_API_KEY"]
    app_secret = os.environ["SCHWAB_APP_SECRET"]
    callback_url = os.environ.get("SCHWAB_CALLBACK_URL", "https://127.0.0.1:8182")
    token_path = os.environ.get("SCHWAB_TOKEN_PATH", str(Path.home() / ".schwab" / "token.json"))

    Path(token_path).parent.mkdir(parents=True, exist_ok=True)

    if Path(token_path).exists():
        _client = schwab.auth.client_from_token_file(
            token_path, api_key, app_secret, asyncio=True
        )
    else:
        _client = schwab.auth.client_from_manual_flow(
            api_key, app_secret, callback_url, token_path, asyncio=True
        )

    return _client
