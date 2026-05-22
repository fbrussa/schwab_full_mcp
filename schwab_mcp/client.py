import os
from pathlib import Path

from dotenv import load_dotenv
import schwab.auth

# Load .env from the project root (where the process was launched)
# Also try the package's parent directory as fallback
_project_root = Path(__file__).resolve().parent.parent
load_dotenv(_project_root / ".env")
load_dotenv()  # also try cwd

_client = None


def _resolve_token_path() -> str:
    """Resolve the token path, expanding ~ and defaulting to project-local."""
    raw = os.environ.get("SCHWAB_TOKEN_PATH", "")
    if raw:
        return str(Path(raw).expanduser().resolve())
    # Default: token.json inside the project root (avoids sandbox issues)
    return str(_project_root / "token.json")


def get_client():
    global _client
    if _client is not None:
        return _client

    api_key = os.environ["SCHWAB_API_KEY"]
    app_secret = os.environ["SCHWAB_APP_SECRET"]
    callback_url = os.environ.get("SCHWAB_CALLBACK_URL", "https://127.0.0.1:8182")
    token_path = _resolve_token_path()

    token_file = Path(token_path)
    token_file.parent.mkdir(parents=True, exist_ok=True)

    if token_file.exists():
        _client = schwab.auth.client_from_token_file(
            token_path, api_key, app_secret, asyncio=True
        )
    else:
        raise RuntimeError(
            f"Token file not found: {token_path}\n"
            "Run 'python scripts/generate_token.py' first to authenticate."
        )

    return _client
