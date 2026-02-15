import logging
import os

import requests

URL="http://api.weatherapi.com/v1/forecast.json"\

def claw(query: str, days: int) -> str:
    params = {"query": query, "days": days, "key": os.getenv("WEATHER_API")}
    logging.debug(f"Calling weather API with: {params}")
    try:
        resp = requests.get(URL, params=params)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        logging.error(f"Failed to call {URL}")
