# curl --request GET \
#                --url 'https://real-time-news-data.p.rapidapi.com/search?query=Football&limit=10&time_published=anytime&country=US&lang=en' \
#                      --header 'x-rapidapi-host: real-time-news-data.p.rapidapi.com' \
#                               --header 'x-rapidapi-key: 434d58574bmsh882d26a432fc248p1b820ajsn647a046dc17e'
import logging
import os

import requests

URL = "https://real-time-news-data.p.rapidapi.com/search"

def claw(query: str, limit: int, country: str, time_published: str) -> str:
    params = {"query": query, "limit": limit, "country": country, "time_published": time_published}
    headers = { "x-rapidapi-host": "real-time-news-data.p.rapidapi.com", "x-rapidapi-key": os.getenv("RAPID") }
    try:
        response = requests.get(URL, params=params, headers=headers)
        return response.text
    except requests.RequestException as e:
        logging.exception(e)
