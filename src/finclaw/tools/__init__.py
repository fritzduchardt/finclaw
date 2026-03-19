from .news_tools import register_news_tools
from .social_tools import register_social_tools
from .weather_tools import register_weather_tools


def register_tools(mcp) -> None:
    register_social_tools(mcp)
    register_news_tools(mcp)
    register_weather_tools(mcp)
