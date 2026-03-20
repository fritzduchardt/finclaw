import json
import logging
from typing import Optional

import typer
import yfinance as yf

app = typer.Typer()

@app.command()
def get_stock_info(ticker: str) -> dict:
    """Fetch basic stock information for a given ticker symbol."""
    logging.info(f"Fetching stock information for {ticker}")
    stock = yf.Ticker(ticker)
    print(json.dumps(stock.info))
    return stock.info

@app.command()
def get_current_price(ticker: str) -> Optional[float]:
    """Get the current price of a stock."""
    logging.info(f"Fetching current price for {ticker}")
    stock = yf.Ticker(ticker)
    info = stock.info
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    print(price)
    return price

def get_historical_data(
    ticker: str,
    period: str = "1mo",
    interval: str = "1d",
    auto_adjust: bool = True,
) -> dict:
    """Fetch historical price data for a stock."""
    logging.info(
        f"Fetching historical data for {ticker} period={period} interval={interval}"
    )
    stock = yf.Ticker(ticker)
    history = stock.history(
        period=period,
        interval=interval,
        auto_adjust=auto_adjust,
    )
    if history.empty:
        return {}
    history.index = history.index.astype(str)
    return history.to_dict(orient="index")

def get_historical_data_by_date(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "1d",
    auto_adjust: bool = True,
) -> dict:
    """Fetch historical price data for a stock between start and end dates."""
    logging.info(
        "Fetching historical data for %s start_date=%s end_date=%s interval=%s",
        ticker,
        start_date,
        end_date,
        interval,
    )
    stock = yf.Ticker(ticker)
    history = stock.history(
        start=start_date,
        end=end_date,
        interval=interval,
        auto_adjust=auto_adjust,
    )
    if history.empty:
        return {}
    history.index = history.index.astype(str)
    return history.to_dict(orient="index")
