import logging
import os

import requests

URL = "https://api.twelvedata.com/time_series"

def shoot(symbol: str, start_date: str, end_date: str, interval: str) -> str:
    params = {"symbol": symbol, "interval": interval, "apikey": os.getenv("TWELVE_DATA"), "timezone": "Europe/Berlin", "start_date": start_date, "end_date": end_date}
    logging.info(f"Historical data for: {params}")
    try:
        response = requests.get(URL, params)
        return response.text
    except requests.RequestException as e:
        logging.exception(e)
