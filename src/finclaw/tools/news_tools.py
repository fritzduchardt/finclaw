from ..news.rapid import news_search


def register_news_tools(mcp) -> None:
    @mcp.tool()
    def world_news(query: str, limit: int, country: str, time_published: str) -> str:
        """World news

        Args:
            query: specific query about what happened
            limit: int of number of news items
            country: country code, e.g. US, UK, GE
            time_published: duration to the past from now in minutes, hours, days, or years, e.g. 1m, 1h, 1d, 1y.
        """
        data = news_search.shoot(query, limit, country, time_published)
        return data