#!/usr/bin/env python3

from mcp.server.fastmcp import FastMCP
from social.ts import trump as t
from finance.twelvedata import historical_data as hd

# Initialize the MCP server
mcp = FastMCP("my-server-name")

@mcp.tool()
def trump_tweets(start_date: str, end_date: str) -> str:
    """Trump Tweets

    Args:
        start_date: start date
        end_date: end date
    """
    # Your existing logic here
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
    # Your existing logic here
    data = hd.claw(symbol, start_date, end_date)
    return data

if __name__ == "__main__":
    mcp.run()
