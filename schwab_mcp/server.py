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
    import argparse

    parser = argparse.ArgumentParser(description="Schwab MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport mode (default: stdio for Claude Desktop, streamable-http for standalone)",
    )
    parser.add_argument("--host", default="0.0.0.0", help="HTTP host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="HTTP port (default: 8000)")
    args = parser.parse_args()

    kwargs = {}
    if args.transport == "streamable-http":
        kwargs["host"] = args.host
        kwargs["port"] = args.port

    mcp.run(transport=args.transport, **kwargs)


if __name__ == "__main__":
    main()
