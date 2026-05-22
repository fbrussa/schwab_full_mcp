# schwab_full_mcp

Unofficial MCP server that exposes the full Charles Schwab brokerage API as tools, built with [FastMCP](https://github.com/jlowin/fastmcp) and [schwab-py](https://github.com/alexgolec/schwab-py).

## What it does

**54 tools** organized in 4 modules:

### Accounts
- List all linked accounts and their hashes
- Get balances, positions, and margin info per account
- User preferences

### Orders
- **Equity**: market, limit, stop, stop-limit, trailing stop (buy, sell, short sell, buy-to-cover)
- **Options single-leg**: buy/sell to open/close, market and limit
- **Vertical spreads**: bull call, bear call, bull put, bear put (open and close)
- **Advanced**: raw order spec for iron condors, butterflies, diagonals, or any multi-leg strategy
- **Composite**: one-cancels-other (OCO) and first-triggers-second
- **Management**: get, replace, cancel orders; preview before placing
- **Utility**: build OCC option symbols from components

### Transactions
- Query by date range, type (trade, dividend, ACH, wire, margin call, etc.), and symbol
- Get individual transaction details

### Market Data
- Real-time quotes (single and multi-symbol)
- Option chains with greeks (delta, gamma, theta, vega), IV, and analytical pricing
- Option expiration dates
- Price history (1min to weekly candles, intraday back ~48 days, daily back to 1985)
- Instrument search (by symbol, description, regex, fundamentals)
- CUSIP lookup
- Top movers by index
- Market hours

## Prerequisites

1. A [Schwab Developer](https://developer.schwab.com/) account with an approved app
2. Your app's **API Key** and **App Secret**
3. Callback URL set to `https://127.0.0.1:8182` in the Schwab developer portal
4. Python >= 3.10

## Setup

```bash
git clone git@github.com:fbrussa/schwab_full_mcp.git
cd schwab_full_mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Copy the env example and fill in your credentials:

```bash
cp .env.example .env
```

```env
SCHWAB_API_KEY=your_api_key_here
SCHWAB_APP_SECRET=your_app_secret_here
SCHWAB_CALLBACK_URL=https://127.0.0.1:8182
SCHWAB_TOKEN_PATH=~/.schwab/token.json
```

## Running the MCP server

### Standalone (HTTP)

```bash
source .venv/bin/activate
export SCHWAB_API_KEY=your_api_key
export SCHWAB_APP_SECRET=your_app_secret
python -m schwab_mcp.server
```

The server starts on `http://0.0.0.0:8000` using the `streamable-http` transport.

### With Claude Code

Add to your `.claude/settings.json`:

```json
{
  "mcpServers": {
    "schwab": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

Then start the server in a separate terminal and use Claude Code normally.

### With Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "schwab": {
      "command": "/path/to/schwab_full_mcp/.venv/bin/python",
      "args": ["-m", "schwab_mcp.server"],
      "cwd": "/path/to/schwab_full_mcp",
      "env": {
        "SCHWAB_API_KEY": "your_api_key",
        "SCHWAB_APP_SECRET": "your_app_secret"
      }
    }
  }
}
```

## Authentication

### First time: generate the token

```bash
python scripts/generate_token.py
```

The script will:

1. Print a URL — open it in your browser
2. Log into Schwab
3. You'll be redirected to `https://127.0.0.1:8182` (the page may show an error, that's normal)
4. Copy the full URL from your browser's address bar
5. Paste it back into the terminal

The token is saved to `~/.schwab/token.json` (or your configured `SCHWAB_TOKEN_PATH`).

### Refreshing every 7 days

Schwab refresh tokens expire after **7 days**. Within that window, access tokens auto-refresh transparently. After 7 days you must re-authenticate.

Run the same script to renew:

```bash
python scripts/generate_token.py
```

It will show the token age and warn you if it's about to expire. If it's already expired, it deletes the old token and starts a fresh OAuth flow.

## Notes

- All order tools require an `account_hash` — call `list_accounts` first to get it
- Option symbols use OCC format (e.g. `AAPL  240119C00190000`) — use `build_option_symbol` to construct them
- `place_custom_order` accepts raw order spec dicts for any strategy not covered by convenience tools
- Market data does not require an account hash
- No paper trading support (Schwab API limitation)
