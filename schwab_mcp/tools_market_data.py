from datetime import date, datetime
from typing import Literal

from fastmcp import FastMCP

from .client import get_client
from .helpers import unwrap

mcp = FastMCP("schwab-market-data")


# ---------------------------------------------------------------------------
# Quotes
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_quote(symbol: str) -> dict:
    """Get a real-time quote for a single symbol.

    Args:
        symbol: Ticker symbol (e.g. AAPL, MSFT). For futures use get_quotes instead.
    """
    client = get_client()
    r = await client.get_quote(symbol)
    return unwrap(r)


@mcp.tool()
async def get_quotes(symbols: list[str]) -> dict:
    """Get real-time quotes for multiple symbols at once.

    Handles all symbol types including futures (e.g. /ES).

    Args:
        symbols: List of ticker symbols.
    """
    client = get_client()
    r = await client.get_quotes(symbols)
    return unwrap(r)


# ---------------------------------------------------------------------------
# Option chains
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_option_chain(
    symbol: str,
    contract_type: Literal["CALL", "PUT", "ALL"] | None = None,
    strike_count: int | None = None,
    include_underlying_quote: bool | None = None,
    strategy: Literal[
        "SINGLE", "ANALYTICAL", "COVERED", "VERTICAL", "CALENDAR",
        "STRANGLE", "STRADDLE", "BUTTERFLY", "CONDOR", "DIAGONAL",
        "COLLAR", "ROLL"
    ] | None = None,
    interval: float | None = None,
    strike: float | None = None,
    strike_range: Literal[
        "IN_THE_MONEY", "NEAR_THE_MONEY", "OUT_OF_THE_MONEY",
        "STRIKES_ABOVE_MARKET", "STRIKES_BELOW_MARKET",
        "STRIKES_NEAR_MARKET", "ALL"
    ] | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
    volatility: float | None = None,
    underlying_price: float | None = None,
    interest_rate: float | None = None,
    days_to_expiration: int | None = None,
    exp_month: Literal[
        "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
        "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER", "ALL"
    ] | None = None,
    option_type: Literal["STANDARD", "NON_STANDARD", "ALL"] | None = None,
    entitlement: Literal["PAYING_PRO", "NON_PRO", "NON_PAYING_PRO"] | None = None,
) -> dict:
    """Get the option chain for a symbol. Includes greeks, IV, bid/ask, open interest.

    When strategy is ANALYTICAL, you can pass custom volatility, underlying_price,
    interest_rate, and days_to_expiration to compute theoretical values.

    Args:
        symbol: Underlying ticker (e.g. AAPL).
        contract_type: CALL, PUT, or ALL.
        strike_count: Number of strikes above and below at-the-money.
        include_underlying_quote: Include underlying quote data.
        strategy: Pricing strategy. Use ANALYTICAL for custom greeks calculation.
        interval: Strike interval for spread strategies.
        strike: Specific strike price to filter.
        strike_range: Filter by moneyness.
        from_date: Start expiration date filter (YYYY-MM-DD).
        to_date: End expiration date filter (YYYY-MM-DD).
        volatility: Custom volatility for ANALYTICAL strategy.
        underlying_price: Custom underlying price for ANALYTICAL strategy.
        interest_rate: Custom interest rate for ANALYTICAL strategy.
        days_to_expiration: Custom DTE for ANALYTICAL strategy.
        exp_month: Filter by expiration month.
        option_type: STANDARD, NON_STANDARD, or ALL.
        entitlement: Market data entitlement level.
    """
    from schwab.client import Client

    client = get_client()
    kwargs: dict = {}

    if contract_type:
        kwargs["contract_type"] = Client.Options.ContractType[contract_type]
    if strike_count is not None:
        kwargs["strike_count"] = strike_count
    if include_underlying_quote is not None:
        kwargs["include_underlying_quote"] = include_underlying_quote
    if strategy:
        kwargs["strategy"] = Client.Options.Strategy[strategy]
    if interval is not None:
        kwargs["interval"] = interval
    if strike is not None:
        kwargs["strike"] = strike
    if strike_range:
        kwargs["strike_range"] = Client.Options.StrikeRange[strike_range]
    if from_date:
        kwargs["from_date"] = date.fromisoformat(from_date)
    if to_date:
        kwargs["to_date"] = date.fromisoformat(to_date)
    if volatility is not None:
        kwargs["volatility"] = volatility
    if underlying_price is not None:
        kwargs["underlying_price"] = underlying_price
    if interest_rate is not None:
        kwargs["interest_rate"] = interest_rate
    if days_to_expiration is not None:
        kwargs["days_to_expiration"] = days_to_expiration
    if exp_month:
        kwargs["exp_month"] = Client.Options.ExpirationMonth[exp_month]
    if option_type:
        kwargs["option_type"] = Client.Options.Type[option_type]
    if entitlement:
        kwargs["entitlement"] = Client.Options.Entitlement[entitlement]

    r = await client.get_option_chain(symbol, **kwargs)
    return unwrap(r)


@mcp.tool()
async def get_option_expiration_chain(symbol: str) -> dict:
    """Get all available option expiration dates for a symbol.

    Args:
        symbol: Underlying ticker symbol.
    """
    client = get_client()
    r = await client.get_option_expiration_chain(symbol)
    return unwrap(r)


# ---------------------------------------------------------------------------
# Price history
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_price_history(
    symbol: str,
    frequency: Literal[
        "1min", "5min", "10min", "15min", "30min", "daily", "weekly"
    ] = "daily",
    start_date: str | None = None,
    end_date: str | None = None,
    need_extended_hours: bool | None = None,
    need_previous_close: bool | None = None,
) -> dict:
    """Get historical price candles for a symbol.

    Data availability by frequency:
    - 1min: ~48 days
    - 5min, 10min, 15min, 30min: ~9 months
    - daily, weekly: back to 1985

    Args:
        symbol: Ticker symbol.
        frequency: Candle frequency. One of: 1min, 5min, 10min, 15min, 30min, daily, weekly.
        start_date: Start datetime (ISO format, e.g. 2024-01-15 or 2024-01-15T09:30:00).
        end_date: End datetime (ISO format).
        need_extended_hours: Include extended hours data (pre/post market).
        need_previous_close: Include previous close price.
    """
    client = get_client()

    freq_map = {
        "1min": "get_price_history_every_minute",
        "5min": "get_price_history_every_five_minutes",
        "10min": "get_price_history_every_ten_minutes",
        "15min": "get_price_history_every_fifteen_minutes",
        "30min": "get_price_history_every_thirty_minutes",
        "daily": "get_price_history_every_day",
        "weekly": "get_price_history_every_week",
    }

    method = getattr(client, freq_map[frequency])
    kwargs: dict = {}
    if start_date:
        kwargs["start_datetime"] = datetime.fromisoformat(start_date)
    if end_date:
        kwargs["end_datetime"] = datetime.fromisoformat(end_date)
    if need_extended_hours is not None:
        kwargs["need_extended_hours_data"] = need_extended_hours
    if need_previous_close is not None:
        kwargs["need_previous_close"] = need_previous_close

    r = await method(symbol, **kwargs)
    return unwrap(r)


# ---------------------------------------------------------------------------
# Instruments
# ---------------------------------------------------------------------------


@mcp.tool()
async def search_instruments(
    symbols: str,
    projection: Literal[
        "SYMBOL_SEARCH", "SYMBOL_REGEX", "DESCRIPTION_SEARCH",
        "DESCRIPTION_REGEX", "SEARCH", "FUNDAMENTAL"
    ] = "SYMBOL_SEARCH",
) -> dict:
    """Search for instruments (stocks, ETFs, etc.) by symbol or description.

    Args:
        symbols: Search query. Can be a symbol, partial symbol, or description text
            depending on the projection type.
        projection: Search type:
            - SYMBOL_SEARCH: Exact or prefix symbol match.
            - SYMBOL_REGEX: Regex match on symbols.
            - DESCRIPTION_SEARCH: Search descriptions.
            - DESCRIPTION_REGEX: Regex match on descriptions.
            - SEARCH: Search across symbol and description.
            - FUNDAMENTAL: Get fundamental data (PE, div yield, etc).
    """
    from schwab.client import Client
    client = get_client()
    r = await client.get_instruments(symbols, Client.Instrument.Projection[projection])
    return unwrap(r)


@mcp.tool()
async def get_instrument_by_cusip(cusip: str) -> dict:
    """Look up an instrument by its CUSIP identifier.

    Args:
        cusip: The CUSIP number (preserve leading zeros).
    """
    client = get_client()
    r = await client.get_instrument_by_cusip(cusip)
    return unwrap(r)


# ---------------------------------------------------------------------------
# Movers
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_movers(
    index: Literal[
        "DJI", "COMPX", "SPX", "NYSE", "NASDAQ", "OTCBB",
        "INDEX_ALL", "EQUITY_ALL", "OPTION_ALL", "OPTION_PUT", "OPTION_CALL"
    ],
    sort_order: Literal[
        "VOLUME", "TRADES", "PERCENT_CHANGE_UP", "PERCENT_CHANGE_DOWN"
    ] | None = None,
    frequency: int | None = None,
) -> dict:
    """Get top 10 movers for a market index.

    Args:
        index: Market index. DJI (Dow Jones), COMPX (NASDAQ Composite), SPX (S&P 500),
            NYSE, NASDAQ, OTCBB, INDEX_ALL, EQUITY_ALL, OPTION_ALL, OPTION_PUT, OPTION_CALL.
        sort_order: Sort by VOLUME, TRADES, PERCENT_CHANGE_UP, or PERCENT_CHANGE_DOWN.
        frequency: Time frequency in minutes (0, 1, 5, 10, 30, 60).
    """
    from schwab.client import Client
    client = get_client()
    kwargs: dict = {}
    if sort_order:
        kwargs["sort_order"] = Client.Movers.SortOrder[sort_order]
    if frequency is not None:
        kwargs["frequency"] = Client.Movers.Frequency(frequency)
    r = await client.get_movers(Client.Movers.Index[index], **kwargs)
    return unwrap(r)


# ---------------------------------------------------------------------------
# Market hours
# ---------------------------------------------------------------------------


@mcp.tool()
async def get_market_hours(
    markets: list[Literal["EQUITY", "OPTION", "BOND", "FUTURE", "FOREX"]],
    date_str: str | None = None,
) -> dict:
    """Get trading hours for specified markets.

    Args:
        markets: List of markets: EQUITY, OPTION, BOND, FUTURE, FOREX.
        date_str: Date to check (YYYY-MM-DD). Defaults to today. Up to 1 year forward.
    """
    from schwab.client import Client
    client = get_client()
    market_enums = [Client.MarketHours.Market[m] for m in markets]
    kwargs: dict = {}
    if date_str:
        kwargs["date"] = date.fromisoformat(date_str)
    r = await client.get_market_hours(market_enums, **kwargs)
    return unwrap(r)
