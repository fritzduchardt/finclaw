import json
import logging

import requests

URL="https://en.wikipedia.org/w/api.php"

def claw(title: str) -> str:

    params = {
        "action": "query",
        "titles": title,
        "prop": "extracts",
        "exintro": "",
        "explaintext": "",
        "format": "json"
    }

    headers = {
        "User-Agent": "finclaw"
    }

    try:
        resp = requests.get(URL, params=params, headers=headers)
        resp.raise_for_status()
    except requests.RequestException as e:
        logging.exception(e)
        return ""

    payload = json.loads(resp.text)
    pages = payload["query"]["pages"]
    if len(pages) > 0:
        first_key = next(iter(pages))
        page = pages[first_key]
        page_id = page["pageid"]
        return json.dumps({"title": page["title"], "extract": page["extract"], "pageId": page_id})

    return ""
