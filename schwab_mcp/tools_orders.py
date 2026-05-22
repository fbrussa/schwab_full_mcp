from datetime import datetime
from typing import Literal

from fastmcp import FastMCP

from .client import get_client
from .helpers import unwrap

mcp = FastMCP("schwab-orders")


# ---------------------------------------------------------------------------
# Query orders
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_orders_for_account(
    account_hash: str,
    max_results: int | None = None,
    from_entered_datetime: str | None = None,
    to_entered_datetime: str | None = None,
    status: str | None = None,
) -> dict:
    """Get orders for a specific account.

    Args:
        account_hash: The account hash value.
        max_results: Maximum number of orders to return.
        from_entered_datetime: Start date filter (ISO format, e.g. 2024-01-15).
        to_entered_datetime: End date filter (ISO format, e.g. 2024-02-15).
        status: Filter by order status. Values: AWAITING_PARENT_ORDER, AWAITING_CONDITION,
            AWAITING_STOP_CONDITION, AWAITING_MANUAL_REVIEW, ACCEPTED, AWAITING_UR_OUT,
            PENDING_ACTIVATION, QUEUED, WORKING, REJECTED, PENDING_CANCEL, CANCELED,
            PENDING_REPLACE, REPLACED, FILLED, EXPIRED, NEW, AWAITING_RELEASE_TIME,
            PENDING_ACKNOWLEDGEMENT, PENDING_RECALL, UNKNOWN.
    """
    client = get_client()
    kwargs: dict = {}
    if max_results is not None:
        kwargs["max_results"] = max_results
    if from_entered_datetime:
        kwargs["from_entered_datetime"] = datetime.fromisoformat(from_entered_datetime)
    if to_entered_datetime:
        kwargs["to_entered_datetime"] = datetime.fromisoformat(to_entered_datetime)
    if status:
        from schwab.client import Client
        kwargs["status"] = Client.Order.Status[status]
    r = await client.get_orders_for_account(account_hash, **kwargs)
    return unwrap(r)


@mcp.tool()
async def get_orders_for_all_accounts(
    max_results: int | None = None,
    from_entered_datetime: str | None = None,
    to_entered_datetime: str | None = None,
    status: str | None = None,
) -> dict:
    """Get orders across all linked accounts.

    Args:
        max_results: Maximum number of orders to return.
        from_entered_datetime: Start date filter (ISO format).
        to_entered_datetime: End date filter (ISO format).
        status: Filter by order status (see get_orders_for_account for values).
    """
    client = get_client()
    kwargs: dict = {}
    if max_results is not None:
        kwargs["max_results"] = max_results
    if from_entered_datetime:
        kwargs["from_entered_datetime"] = datetime.fromisoformat(from_entered_datetime)
    if to_entered_datetime:
        kwargs["to_entered_datetime"] = datetime.fromisoformat(to_entered_datetime)
    if status:
        from schwab.client import Client
        kwargs["status"] = Client.Order.Status[status]
    r = await client.get_orders_for_all_linked_accounts(**kwargs)
    return unwrap(r)


@mcp.tool()
async def get_order(account_hash: str, order_id: str) -> dict:
    """Get details of a specific order.

    Args:
        account_hash: The account hash value.
        order_id: The order ID to look up.
    """
    client = get_client()
    r = await client.get_order(order_id, account_hash)
    return unwrap(r)


# ---------------------------------------------------------------------------
# Equity orders
# ---------------------------------------------------------------------------


@mcp.tool()
async def equity_buy_market(account_hash: str, symbol: str, quantity: int) -> dict:
    """Place a market buy order for an equity.

    Args:
        account_hash: The account hash value.
        symbol: Ticker symbol (e.g. AAPL).
        quantity: Number of shares to buy.
    """
    from schwab.orders.equities import equity_buy_market as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(symbol, quantity))
    return unwrap(r)


@mcp.tool()
async def equity_buy_limit(
    account_hash: str, symbol: str, quantity: int, price: float
) -> dict:
    """Place a limit buy order for an equity.

    Args:
        account_hash: The account hash value.
        symbol: Ticker symbol (e.g. AAPL).
        quantity: Number of shares.
        price: Limit price.
    """
    from schwab.orders.equities import equity_buy_limit as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(symbol, quantity, price))
    return unwrap(r)


@mcp.tool()
async def equity_sell_market(account_hash: str, symbol: str, quantity: int) -> dict:
    """Place a market sell order for an equity.

    Args:
        account_hash: The account hash value.
        symbol: Ticker symbol.
        quantity: Number of shares to sell.
    """
    from schwab.orders.equities import equity_sell_market as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(symbol, quantity))
    return unwrap(r)


@mcp.tool()
async def equity_sell_limit(
    account_hash: str, symbol: str, quantity: int, price: float
) -> dict:
    """Place a limit sell order for an equity.

    Args:
        account_hash: The account hash value.
        symbol: Ticker symbol.
        quantity: Number of shares.
        price: Limit price.
    """
    from schwab.orders.equities import equity_sell_limit as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(symbol, quantity, price))
    return unwrap(r)


@mcp.tool()
async def equity_sell_short_market(account_hash: str, symbol: str, quantity: int) -> dict:
    """Place a market short sell order.

    Args:
        account_hash: The account hash value.
        symbol: Ticker symbol.
        quantity: Number of shares to short.
    """
    from schwab.orders.equities import equity_sell_short_market as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(symbol, quantity))
    return unwrap(r)


@mcp.tool()
async def equity_sell_short_limit(
    account_hash: str, symbol: str, quantity: int, price: float
) -> dict:
    """Place a limit short sell order.

    Args:
        account_hash: The account hash value.
        symbol: Ticker symbol.
        quantity: Number of shares.
        price: Limit price.
    """
    from schwab.orders.equities import equity_sell_short_limit as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(symbol, quantity, price))
    return unwrap(r)


@mcp.tool()
async def equity_buy_to_cover_market(account_hash: str, symbol: str, quantity: int) -> dict:
    """Place a market buy-to-cover order (close a short position).

    Args:
        account_hash: The account hash value.
        symbol: Ticker symbol.
        quantity: Number of shares.
    """
    from schwab.orders.equities import equity_buy_to_cover_market as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(symbol, quantity))
    return unwrap(r)


@mcp.tool()
async def equity_buy_to_cover_limit(
    account_hash: str, symbol: str, quantity: int, price: float
) -> dict:
    """Place a limit buy-to-cover order (close a short position).

    Args:
        account_hash: The account hash value.
        symbol: Ticker symbol.
        quantity: Number of shares.
        price: Limit price.
    """
    from schwab.orders.equities import equity_buy_to_cover_limit as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(symbol, quantity, price))
    return unwrap(r)


# ---------------------------------------------------------------------------
# Stop and stop-limit equity orders
# ---------------------------------------------------------------------------


@mcp.tool()
async def equity_buy_stop(
    account_hash: str, symbol: str, quantity: int, stop_price: float
) -> dict:
    """Place a stop buy order for an equity.

    Args:
        account_hash: The account hash value.
        symbol: Ticker symbol.
        quantity: Number of shares.
        stop_price: The stop trigger price.
    """
    from schwab.orders.common import OrderBuilder, OrderType, Session, Duration, EquityInstruction
    order = (
        OrderBuilder()
        .set_order_type(OrderType.STOP)
        .set_session(Session.NORMAL)
        .set_duration(Duration.DAY)
        .set_stop_price(str(stop_price))
        .add_equity_leg(EquityInstruction.BUY, symbol, quantity)
    )
    client = get_client()
    r = await client.place_order(account_hash, order)
    return unwrap(r)


@mcp.tool()
async def equity_sell_stop(
    account_hash: str, symbol: str, quantity: int, stop_price: float
) -> dict:
    """Place a stop sell order for an equity (stop loss).

    Args:
        account_hash: The account hash value.
        symbol: Ticker symbol.
        quantity: Number of shares.
        stop_price: The stop trigger price.
    """
    from schwab.orders.common import OrderBuilder, OrderType, Session, Duration, EquityInstruction
    order = (
        OrderBuilder()
        .set_order_type(OrderType.STOP)
        .set_session(Session.NORMAL)
        .set_duration(Duration.DAY)
        .set_stop_price(str(stop_price))
        .add_equity_leg(EquityInstruction.SELL, symbol, quantity)
    )
    client = get_client()
    r = await client.place_order(account_hash, order)
    return unwrap(r)


@mcp.tool()
async def equity_buy_stop_limit(
    account_hash: str,
    symbol: str,
    quantity: int,
    stop_price: float,
    limit_price: float,
) -> dict:
    """Place a stop-limit buy order for an equity.

    Args:
        account_hash: The account hash value.
        symbol: Ticker symbol.
        quantity: Number of shares.
        stop_price: The stop trigger price.
        limit_price: The limit price once triggered.
    """
    from schwab.orders.common import OrderBuilder, OrderType, Session, Duration, EquityInstruction
    order = (
        OrderBuilder()
        .set_order_type(OrderType.STOP_LIMIT)
        .set_session(Session.NORMAL)
        .set_duration(Duration.DAY)
        .set_stop_price(str(stop_price))
        .set_price(str(limit_price))
        .add_equity_leg(EquityInstruction.BUY, symbol, quantity)
    )
    client = get_client()
    r = await client.place_order(account_hash, order)
    return unwrap(r)


@mcp.tool()
async def equity_sell_stop_limit(
    account_hash: str,
    symbol: str,
    quantity: int,
    stop_price: float,
    limit_price: float,
) -> dict:
    """Place a stop-limit sell order for an equity.

    Args:
        account_hash: The account hash value.
        symbol: Ticker symbol.
        quantity: Number of shares.
        stop_price: The stop trigger price.
        limit_price: The limit price once triggered.
    """
    from schwab.orders.common import OrderBuilder, OrderType, Session, Duration, EquityInstruction
    order = (
        OrderBuilder()
        .set_order_type(OrderType.STOP_LIMIT)
        .set_session(Session.NORMAL)
        .set_duration(Duration.DAY)
        .set_stop_price(str(stop_price))
        .set_price(str(limit_price))
        .add_equity_leg(EquityInstruction.SELL, symbol, quantity)
    )
    client = get_client()
    r = await client.place_order(account_hash, order)
    return unwrap(r)


@mcp.tool()
async def equity_trailing_stop(
    account_hash: str,
    symbol: str,
    quantity: int,
    trail_offset: float,
    trail_type: Literal["VALUE", "PERCENT"] = "VALUE",
    instruction: Literal["BUY", "SELL"] = "SELL",
) -> dict:
    """Place a trailing stop order for an equity.

    Args:
        account_hash: The account hash value.
        symbol: Ticker symbol.
        quantity: Number of shares.
        trail_offset: The trailing amount (dollar value or percentage).
        trail_type: VALUE for dollar amount, PERCENT for percentage.
        instruction: BUY or SELL.
    """
    from schwab.orders.common import (
        OrderBuilder, OrderType, Session, Duration, EquityInstruction,
        StopPriceLinkBasis, StopPriceLinkType, StopType,
    )
    instr = EquityInstruction.BUY if instruction == "BUY" else EquityInstruction.SELL
    link_type = StopPriceLinkType.PERCENT if trail_type == "PERCENT" else StopPriceLinkType.VALUE
    order = (
        OrderBuilder()
        .set_order_type(OrderType.TRAILING_STOP)
        .set_session(Session.NORMAL)
        .set_duration(Duration.DAY)
        .set_stop_price_link_basis(StopPriceLinkBasis.LAST)
        .set_stop_price_link_type(link_type)
        .set_stop_price_offset(str(trail_offset))
        .set_stop_type(StopType.STANDARD)
        .add_equity_leg(instr, symbol, quantity)
    )
    client = get_client()
    r = await client.place_order(account_hash, order)
    return unwrap(r)


# ---------------------------------------------------------------------------
# Option orders — single leg
# ---------------------------------------------------------------------------


@mcp.tool()
async def option_buy_to_open_market(
    account_hash: str, option_symbol: str, quantity: int
) -> dict:
    """Buy to open an option at market price.

    Args:
        account_hash: The account hash value.
        option_symbol: Full OCC option symbol (e.g. AAPL  240119C00190000).
        quantity: Number of contracts.
    """
    from schwab.orders.options import option_buy_to_open_market as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(option_symbol, quantity))
    return unwrap(r)


@mcp.tool()
async def option_buy_to_open_limit(
    account_hash: str, option_symbol: str, quantity: int, price: float
) -> dict:
    """Buy to open an option at a limit price.

    Args:
        account_hash: The account hash value.
        option_symbol: Full OCC option symbol.
        quantity: Number of contracts.
        price: Limit price per contract.
    """
    from schwab.orders.options import option_buy_to_open_limit as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(option_symbol, quantity, price))
    return unwrap(r)


@mcp.tool()
async def option_sell_to_open_market(
    account_hash: str, option_symbol: str, quantity: int
) -> dict:
    """Sell to open an option at market price (write an option).

    Args:
        account_hash: The account hash value.
        option_symbol: Full OCC option symbol.
        quantity: Number of contracts.
    """
    from schwab.orders.options import option_sell_to_open_market as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(option_symbol, quantity))
    return unwrap(r)


@mcp.tool()
async def option_sell_to_open_limit(
    account_hash: str, option_symbol: str, quantity: int, price: float
) -> dict:
    """Sell to open an option at a limit price (write an option).

    Args:
        account_hash: The account hash value.
        option_symbol: Full OCC option symbol.
        quantity: Number of contracts.
        price: Limit price per contract (credit received).
    """
    from schwab.orders.options import option_sell_to_open_limit as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(option_symbol, quantity, price))
    return unwrap(r)


@mcp.tool()
async def option_buy_to_close_market(
    account_hash: str, option_symbol: str, quantity: int
) -> dict:
    """Buy to close an option at market price.

    Args:
        account_hash: The account hash value.
        option_symbol: Full OCC option symbol.
        quantity: Number of contracts.
    """
    from schwab.orders.options import option_buy_to_close_market as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(option_symbol, quantity))
    return unwrap(r)


@mcp.tool()
async def option_buy_to_close_limit(
    account_hash: str, option_symbol: str, quantity: int, price: float
) -> dict:
    """Buy to close an option at a limit price.

    Args:
        account_hash: The account hash value.
        option_symbol: Full OCC option symbol.
        quantity: Number of contracts.
        price: Limit price per contract.
    """
    from schwab.orders.options import option_buy_to_close_limit as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(option_symbol, quantity, price))
    return unwrap(r)


@mcp.tool()
async def option_sell_to_close_market(
    account_hash: str, option_symbol: str, quantity: int
) -> dict:
    """Sell to close an option at market price.

    Args:
        account_hash: The account hash value.
        option_symbol: Full OCC option symbol.
        quantity: Number of contracts.
    """
    from schwab.orders.options import option_sell_to_close_market as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(option_symbol, quantity))
    return unwrap(r)


@mcp.tool()
async def option_sell_to_close_limit(
    account_hash: str, option_symbol: str, quantity: int, price: float
) -> dict:
    """Sell to close an option at a limit price.

    Args:
        account_hash: The account hash value.
        option_symbol: Full OCC option symbol.
        quantity: Number of contracts.
        price: Limit price per contract (credit received).
    """
    from schwab.orders.options import option_sell_to_close_limit as _order
    client = get_client()
    r = await client.place_order(account_hash, _order(option_symbol, quantity, price))
    return unwrap(r)


# ---------------------------------------------------------------------------
# Option spreads
# ---------------------------------------------------------------------------


@mcp.tool()
async def bull_call_spread_open(
    account_hash: str,
    long_call_symbol: str,
    short_call_symbol: str,
    quantity: int,
    net_debit: float,
) -> dict:
    """Open a bull call vertical spread (buy lower strike call, sell higher strike call).

    Args:
        account_hash: The account hash value.
        long_call_symbol: OCC symbol for the long (lower strike) call.
        short_call_symbol: OCC symbol for the short (higher strike) call.
        quantity: Number of spreads.
        net_debit: Maximum net debit to pay per spread.
    """
    from schwab.orders.options import bull_call_vertical_open
    client = get_client()
    r = await client.place_order(
        account_hash,
        bull_call_vertical_open(long_call_symbol, short_call_symbol, quantity, net_debit),
    )
    return unwrap(r)


@mcp.tool()
async def bull_call_spread_close(
    account_hash: str,
    long_call_symbol: str,
    short_call_symbol: str,
    quantity: int,
    net_credit: float,
) -> dict:
    """Close a bull call vertical spread.

    Args:
        account_hash: The account hash value.
        long_call_symbol: OCC symbol for the long call to sell.
        short_call_symbol: OCC symbol for the short call to buy back.
        quantity: Number of spreads.
        net_credit: Minimum net credit to receive per spread.
    """
    from schwab.orders.options import bull_call_vertical_close
    client = get_client()
    r = await client.place_order(
        account_hash,
        bull_call_vertical_close(long_call_symbol, short_call_symbol, quantity, net_credit),
    )
    return unwrap(r)


@mcp.tool()
async def bear_call_spread_open(
    account_hash: str,
    short_call_symbol: str,
    long_call_symbol: str,
    quantity: int,
    net_credit: float,
) -> dict:
    """Open a bear call vertical spread (sell lower strike call, buy higher strike call).

    Args:
        account_hash: The account hash value.
        short_call_symbol: OCC symbol for the short (lower strike) call.
        long_call_symbol: OCC symbol for the long (higher strike) call.
        quantity: Number of spreads.
        net_credit: Minimum net credit to receive per spread.
    """
    from schwab.orders.options import bear_call_vertical_open
    client = get_client()
    r = await client.place_order(
        account_hash,
        bear_call_vertical_open(short_call_symbol, long_call_symbol, quantity, net_credit),
    )
    return unwrap(r)


@mcp.tool()
async def bear_call_spread_close(
    account_hash: str,
    short_call_symbol: str,
    long_call_symbol: str,
    quantity: int,
    net_debit: float,
) -> dict:
    """Close a bear call vertical spread.

    Args:
        account_hash: The account hash value.
        short_call_symbol: OCC symbol for the short call to buy back.
        long_call_symbol: OCC symbol for the long call to sell.
        quantity: Number of spreads.
        net_debit: Maximum net debit to pay per spread.
    """
    from schwab.orders.options import bear_call_vertical_close
    client = get_client()
    r = await client.place_order(
        account_hash,
        bear_call_vertical_close(short_call_symbol, long_call_symbol, quantity, net_debit),
    )
    return unwrap(r)


@mcp.tool()
async def bull_put_spread_open(
    account_hash: str,
    long_put_symbol: str,
    short_put_symbol: str,
    quantity: int,
    net_credit: float,
) -> dict:
    """Open a bull put vertical spread (sell higher strike put, buy lower strike put).

    Args:
        account_hash: The account hash value.
        long_put_symbol: OCC symbol for the long (lower strike) put.
        short_put_symbol: OCC symbol for the short (higher strike) put.
        quantity: Number of spreads.
        net_credit: Minimum net credit to receive per spread.
    """
    from schwab.orders.options import bull_put_vertical_open
    client = get_client()
    r = await client.place_order(
        account_hash,
        bull_put_vertical_open(long_put_symbol, short_put_symbol, quantity, net_credit),
    )
    return unwrap(r)


@mcp.tool()
async def bull_put_spread_close(
    account_hash: str,
    long_put_symbol: str,
    short_put_symbol: str,
    quantity: int,
    net_debit: float,
) -> dict:
    """Close a bull put vertical spread.

    Args:
        account_hash: The account hash value.
        long_put_symbol: OCC symbol for the long put to sell.
        short_put_symbol: OCC symbol for the short put to buy back.
        quantity: Number of spreads.
        net_debit: Maximum net debit to pay per spread.
    """
    from schwab.orders.options import bull_put_vertical_close
    client = get_client()
    r = await client.place_order(
        account_hash,
        bull_put_vertical_close(long_put_symbol, short_put_symbol, quantity, net_debit),
    )
    return unwrap(r)


@mcp.tool()
async def bear_put_spread_open(
    account_hash: str,
    short_put_symbol: str,
    long_put_symbol: str,
    quantity: int,
    net_debit: float,
) -> dict:
    """Open a bear put vertical spread (buy higher strike put, sell lower strike put).

    Args:
        account_hash: The account hash value.
        short_put_symbol: OCC symbol for the short (lower strike) put.
        long_put_symbol: OCC symbol for the long (higher strike) put.
        quantity: Number of spreads.
        net_debit: Maximum net debit to pay per spread.
    """
    from schwab.orders.options import bear_put_vertical_open
    client = get_client()
    r = await client.place_order(
        account_hash,
        bear_put_vertical_open(short_put_symbol, long_put_symbol, quantity, net_debit),
    )
    return unwrap(r)


@mcp.tool()
async def bear_put_spread_close(
    account_hash: str,
    short_put_symbol: str,
    long_put_symbol: str,
    quantity: int,
    net_credit: float,
) -> dict:
    """Close a bear put vertical spread.

    Args:
        account_hash: The account hash value.
        short_put_symbol: OCC symbol for the short put to buy back.
        long_put_symbol: OCC symbol for the long put to sell.
        quantity: Number of spreads.
        net_credit: Minimum net credit to receive per spread.
    """
    from schwab.orders.options import bear_put_vertical_close
    client = get_client()
    r = await client.place_order(
        account_hash,
        bear_put_vertical_close(short_put_symbol, long_put_symbol, quantity, net_credit),
    )
    return unwrap(r)


# ---------------------------------------------------------------------------
# Custom / advanced orders
# ---------------------------------------------------------------------------


@mcp.tool()
async def place_custom_order(account_hash: str, order_spec: dict) -> dict:
    """Place a fully custom order using a raw order specification dict.

    Use this for complex multi-leg options, iron condors, butterflies, or any
    order type not covered by the convenience tools. The order_spec follows the
    Schwab API order schema.

    Example order_spec for an iron condor:
    {
        "orderType": "NET_CREDIT",
        "session": "NORMAL",
        "duration": "DAY",
        "price": "1.50",
        "complexOrderStrategyType": "IRON_CONDOR",
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {"instruction": "BUY_TO_OPEN", "quantity": 1, "instrument": {"symbol": "...", "assetType": "OPTION"}},
            {"instruction": "SELL_TO_OPEN", "quantity": 1, "instrument": {"symbol": "...", "assetType": "OPTION"}},
            {"instruction": "SELL_TO_OPEN", "quantity": 1, "instrument": {"symbol": "...", "assetType": "OPTION"}},
            {"instruction": "BUY_TO_OPEN", "quantity": 1, "instrument": {"symbol": "...", "assetType": "OPTION"}}
        ]
    }

    Args:
        account_hash: The account hash value.
        order_spec: Complete order specification as a dict.
    """
    client = get_client()
    r = await client.place_order(account_hash, order_spec)
    return unwrap(r)


@mcp.tool()
async def preview_order(account_hash: str, order_spec: dict) -> dict:
    """Preview an order without placing it. Returns estimated fills and commissions.

    Args:
        account_hash: The account hash value.
        order_spec: Complete order specification as a dict (same format as place_custom_order).
    """
    client = get_client()
    r = await client.preview_order(account_hash, order_spec)
    return unwrap(r)


# ---------------------------------------------------------------------------
# Modify / cancel
# ---------------------------------------------------------------------------


@mcp.tool()
async def replace_order(account_hash: str, order_id: str, new_order_spec: dict) -> dict:
    """Replace (modify) an existing order. Cancels the old order and creates a new one.

    Args:
        account_hash: The account hash value.
        order_id: The existing order ID to replace.
        new_order_spec: The new order specification dict.
    """
    client = get_client()
    r = await client.replace_order(account_hash, order_id, new_order_spec)
    return unwrap(r)


@mcp.tool()
async def cancel_order(account_hash: str, order_id: str) -> dict:
    """Cancel an open order.

    Args:
        account_hash: The account hash value.
        order_id: The order ID to cancel.
    """
    client = get_client()
    r = await client.cancel_order(order_id, account_hash)
    return unwrap(r)


# ---------------------------------------------------------------------------
# Composite orders (OCO, triggers)
# ---------------------------------------------------------------------------


@mcp.tool()
async def place_oco_order(
    account_hash: str, order1: dict, order2: dict
) -> dict:
    """Place a one-cancels-other (OCO) order. When one order fills, the other is cancelled.

    Useful for bracket orders: e.g. a take-profit limit and a stop-loss.

    Args:
        account_hash: The account hash value.
        order1: First order specification dict.
        order2: Second order specification dict.
    """
    from schwab.orders.common import one_cancels_other
    client = get_client()
    r = await client.place_order(account_hash, one_cancels_other(order1, order2))
    return unwrap(r)


@mcp.tool()
async def place_trigger_order(
    account_hash: str, first_order: dict, second_order: dict
) -> dict:
    """Place a first-triggers-second order. The second order activates only after the first fills.

    Useful for: buy stock, then immediately set a trailing stop.

    Args:
        account_hash: The account hash value.
        first_order: The initial order spec (trigger).
        second_order: The conditional order spec (fires on first fill).
    """
    from schwab.orders.common import first_triggers_second
    client = get_client()
    r = await client.place_order(
        account_hash, first_triggers_second(first_order, second_order)
    )
    return unwrap(r)


# ---------------------------------------------------------------------------
# Option symbol builder
# ---------------------------------------------------------------------------


@mcp.tool()
async def build_option_symbol(
    underlying: str,
    expiration_date: str,
    contract_type: Literal["C", "P"],
    strike_price: str,
) -> str:
    """Build an OCC option symbol from components.

    Args:
        underlying: Underlying ticker (e.g. AAPL).
        expiration_date: Expiration date (YYYY-MM-DD).
        contract_type: C for call, P for put.
        strike_price: Strike price as string (e.g. "190", "52.5").

    Returns:
        The full OCC option symbol (e.g. AAPL  240119C00190000).
    """
    from datetime import date
    from schwab.orders.options import OptionSymbol
    parts = expiration_date.split("-")
    exp = date(int(parts[0]), int(parts[1]), int(parts[2]))
    return OptionSymbol(underlying, exp, contract_type, strike_price).build()
