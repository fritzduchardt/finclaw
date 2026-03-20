import typer

from ..finance import yfinance_utils

yfinance_app = typer.Typer()

def register(mcp) -> None:

    @mcp.tool()
    def get_stock_info(ticker: str) -> dict:
        """Fetch basic stock information for a given ticker symbol."""
        return yfinance_utils.get_stock_info(ticker)

    @mcp.tool()
    def get_current_price(ticker: str):
        """Get the current price of a stock."""
        return yfinance_utils.get_current_price(ticker)

    @mcp.tool()
    def get_historical_data(
        ticker: str,
        period: str = "1mo",
        interval: str = "1d",
        auto_adjust: bool = True,
    ) -> dict:
        """Fetch historical price data for a stock."""
        return yfinance_utils.get_historical_data(
            ticker=ticker,
            period=period,
            interval=interval,
            auto_adjust=auto_adjust,
        )

    @mcp.tool()
    def get_historical_data_by_date(
        ticker: str,
        start_date: str,
        end_date: str,
        interval: str = "1d",
        auto_adjust: bool = True,
    ) -> dict:
        """Fetch historical price data for a stock between start and end dates."""
        return yfinance_utils.get_historical_data_by_date(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            interval=interval,
            auto_adjust=auto_adjust,
        )
