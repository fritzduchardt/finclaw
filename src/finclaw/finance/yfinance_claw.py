import logging
from typing import Optional

import yfinance as yf


def register_yfinance_tools(mcp) -> None:

    @mcp.tool()
    def get_stock_info(ticker: str) -> dict:
        """Fetch basic stock information for a given ticker symbol."""
        logging.info(f"Fetching stock information for {ticker}")
        stock = yf.Ticker(ticker)
        return stock.info


    @mcp.tool()
    def get_current_price(ticker: str) -> Optional[float]:
        """Get the current price of a stock."""
        logging.info(f"Fetching current price for {ticker}")
        stock = yf.Ticker(ticker)
        info = stock.info
        return info.get("currentPrice") or info.get("regularMarketPrice")
