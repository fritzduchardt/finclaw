import logging

from ..social.ts import trump as t


def register_social_tools(mcp) -> None:
    @mcp.tool()
    def trump_tweets(start_date: str, end_date: str) -> str:
        """Trump Tweets

        Args:
            start_date: start date
            end_date: end date
        """
        logging.info(f'Looking for Trump tweets from: {start_date} to {end_date}')
        tweets = t.shoot(start_date, end_date)
        return tweets