from fastmcp import FastMCP

from .tools_accounts import mcp as accounts_mcp
from .tools_orders import mcp as orders_mcp
from .tools_transactions import mcp as transactions_mcp
from .tools_market_data import mcp as market_data_mcp

mcp = FastMCP(
    "schwab",
    instructions=(
        "Charles Schwab brokerage MCP server. "
        "Provides tools for account management, order placement (equities, options, "
        "spreads, multi-leg strategies), transaction history, and market data "
        "(quotes, option chains with greeks/IV, price history, instruments, movers). "
        "All order tools require an account_hash which you can get from list_accounts. "
        "Option symbols use OCC format — use build_option_symbol to construct them."
    ),
)

mcp.mount(accounts_mcp)
mcp.mount(orders_mcp)
mcp.mount(transactions_mcp)
mcp.mount(market_data_mcp)


def main():
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
