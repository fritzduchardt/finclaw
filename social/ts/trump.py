import requests

URL = "https://www.trumpstruth.org/feed"

def claw(start_date: str, end_date: str) -> str:
    params = {'start_date': start_date, 'end_date': end_date}
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to call {URL}: {e}")
