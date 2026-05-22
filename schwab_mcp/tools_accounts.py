from fastmcp import FastMCP

from .client import get_client
from .helpers import unwrap

mcp = FastMCP("schwab-accounts")


@mcp.tool()
async def list_accounts() -> dict:
    """List all linked Schwab brokerage accounts with their hash values.

    Returns account numbers and hash values needed for other API calls.
    """
    client = get_client()
    r = await client.get_account_numbers()
    return unwrap(r)


@mcp.tool()
async def get_account(
    account_hash: str,
    include_positions: bool = False,
) -> dict:
    """Get detailed information for a single account.

    Args:
        account_hash: The account hash value (from list_accounts).
        include_positions: Whether to include position details.
    """
    client = get_client()
    fields = None
    if include_positions:
        from schwab.client import Client
        fields = Client.Account.Fields.POSITIONS
    r = await client.get_account(account_hash, fields=fields)
    return unwrap(r)


@mcp.tool()
async def get_all_accounts(include_positions: bool = False) -> dict:
    """Get information for all linked accounts at once.

    Args:
        include_positions: Whether to include position details for each account.
    """
    client = get_client()
    fields = None
    if include_positions:
        from schwab.client import Client
        fields = Client.Account.Fields.POSITIONS
    r = await client.get_accounts(fields=fields)
    return unwrap(r)


@mcp.tool()
async def get_user_preferences() -> dict:
    """Get user preferences for the logged-in account and all linked accounts.

    Returns trading preferences, display preferences, and account details.
    """
    client = get_client()
    r = await client.get_user_preferences()
    return unwrap(r)
