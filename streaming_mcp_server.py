#!/usr/bin/env python3
import logging

from mcp.server.fastmcp import FastMCP
from social.ts import trump as t
from finance.twelvedata import historical_data as hd
from news.rapid import news_search
from weather.weatherapi import weatherapi
from knowledge.wikipedia import wikipedia as wp

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

mcp = FastMCP(name="StatelessServer",stateless_http=False, host="0.0.0.0")


@mcp.tool()
def trump_tweets(start_date: str, end_date: str) -> str:
    """Trump Tweets

    Args:
        start_date: start date
        end_date: end date
    """
    tweets = t.claw(start_date, end_date)
    return tweets

@mcp.tool()
def historical_data(symbol: str, start_date: str, end_date: str, interval: str) -> str:
    """Historical Stock Market Valuations

    Args:
        symbol: asset symbol
        start_date: start date
        end_date: end date
        interval: 1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 8h, 1day, 1week, 1month
    """
    data = hd.claw(symbol, start_date, end_date, interval)
    return data

@mcp.tool()
def world_news(query: str, limit: int, country: str, time_published: str) -> str:
    """World news

    Args:
        query: specific query about what happened
        limit: int of number of news items
        country: country code, e.g. US, UK, GE
        time_published: duration to the past from now in minutes, hours, days, or years, e.g. 1m, 1h, 1d, 1y.
    """
    data = news_search.claw(query, limit, country, time_published)
    return data

@mcp.tool()
def weather_forcast(city: str, days: int) -> str:
    """Weather forcast

    Args:
        city: Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude (decimal degree) or city name
        days: Number of days of weather forecast. Value ranges from 1 to 14
    """
    data = weatherapi.claw(city, days)
    return data

@mcp.tool()
def wikipedia(title: str) -> str:
    """Wikipedia

    Args:
        title: page title in singular
    """
    data = wp.claw(title)
    return data


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
