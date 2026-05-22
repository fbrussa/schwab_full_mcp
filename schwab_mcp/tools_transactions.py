from datetime import date, datetime
from typing import Literal

from fastmcp import FastMCP

from .client import get_client
from .helpers import unwrap

mcp = FastMCP("schwab-transactions")

TRANSACTION_TYPES = [
    "TRADE", "RECEIVE_AND_DELIVER", "DIVIDEND_OR_INTEREST", "ACH_RECEIPT",
    "ACH_DISBURSEMENT", "CASH_RECEIPT", "CASH_DISBURSEMENT", "ELECTRONIC_FUND",
    "WIRE_OUT", "WIRE_IN", "JOURNAL", "MEMORANDUM", "MARGIN_CALL",
    "MONEY_MARKET", "SMA_ADJUSTMENT",
]


@mcp.tool()
async def get_transactions(
    account_hash: str,
    start_date: str | None = None,
    end_date: str | None = None,
    transaction_types: list[str] | None = None,
    symbol: str | None = None,
) -> dict:
    """Get transactions for an account.

    Args:
        account_hash: The account hash value.
        start_date: Start date (YYYY-MM-DD). Defaults to 60 days ago.
        end_date: End date (YYYY-MM-DD). Defaults to today.
        transaction_types: Filter by types: TRADE, RECEIVE_AND_DELIVER,
            DIVIDEND_OR_INTEREST, ACH_RECEIPT, ACH_DISBURSEMENT, CASH_RECEIPT,
            CASH_DISBURSEMENT, ELECTRONIC_FUND, WIRE_OUT, WIRE_IN, JOURNAL,
            MEMORANDUM, MARGIN_CALL, MONEY_MARKET, SMA_ADJUSTMENT.
        symbol: Filter by ticker symbol.
    """
    from schwab.client import Client

    client = get_client()
    kwargs: dict = {}
    if start_date:
        kwargs["start_date"] = date.fromisoformat(start_date)
    if end_date:
        kwargs["end_date"] = date.fromisoformat(end_date)
    if transaction_types:
        kwargs["transaction_types"] = [
            Client.Transactions.TransactionType[t] for t in transaction_types
        ]
    if symbol:
        kwargs["symbol"] = symbol
    r = await client.get_transactions(account_hash, **kwargs)
    return unwrap(r)


@mcp.tool()
async def get_transaction(account_hash: str, transaction_id: str) -> dict:
    """Get a single transaction by ID.

    Args:
        account_hash: The account hash value.
        transaction_id: The transaction ID.
    """
    client = get_client()
    r = await client.get_transaction(account_hash, transaction_id)
    return unwrap(r)
