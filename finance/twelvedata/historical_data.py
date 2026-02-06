import logging
import os

import requests

URL = "https://api.twelvedata.com/time_series"

def claw(symbol: str, start_date: str, end_date: str) -> str:
    params = {"symbol": symbol, "interval": "1day", "apikey": os.getenv("TWELVE_DATA"), "timezone": "Europe/Berlin", "start_date": start_date, "end_date": end_date}
    try:
        response = requests.get(URL, params)
        return response.text
    except requests.RequestException as e:
        logging.exception(e)
