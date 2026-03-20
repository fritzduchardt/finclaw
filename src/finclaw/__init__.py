from .tools import yfinance_tools
from .tools import trump_tools

def register_tools(mcp) -> None:
    yfinance_tools.register(mcp)
    trump_tools.register(mcp)
