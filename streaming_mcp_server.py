#!/usr/bin/env python3

import os
from mcp.server.fastmcp import FastMCP
from social.ts import trump as t
from finance.twelvedata import historical_data as hd
from news.rapid import news_search

# Initialize the MCP server
mcp = FastMCP(name="StatelessServer",stateless_http=False)

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
def historical_data(symbol: str, start_date: str, end_date: str) -> str:
    """Historical Stock Market Valuations

    Args:
        symbol: asset symbol
        start_date: start date
        end_date: end date
    """
    data = hd.claw(symbol, start_date, end_date)
    return data

@mcp.tool()
def world_news(query: str, limit: int, country: str, time_published: str) -> str:
    """World news

    Args:
        query: specific query about what happened
        limit: int of number of news items
        country: country code, e.g. US, UK, GE
        time_published: duration to the past from now, e.g. 1h, 1d, 1w
    """
    # Your existing logic here
    data = news_search.claw(query, limit, country, time_published)
    return data


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0")
