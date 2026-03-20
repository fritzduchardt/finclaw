import json
import logging
import re
import xml.etree.ElementTree as ET
from datetime import date, timedelta, datetime
from email.utils import parsedate_to_datetime
from typing import Iterable, Tuple

import requests
import typer
from ..utils import mongo

TRUMP_URL = "https://www.trumpstruth.org/feed"
app = typer.Typer(help="Trump data")

@app.command()
def print_all_truth_posts_cmd(interval_days: int = 7, earliest_date_str: str | None = None) -> None:
    earliest_date = None
    if earliest_date_str is not None:
        earliest_date = datetime.strptime(earliest_date_str, "%d.%m.%Y").date()
    print_all_truth_posts(interval_days, earliest_date)


@app.command()
def insert_all_truth_posts_cmd(interval_days: int = 7, earliest_date_str: str | None = None) -> None:
    earliest_date = None
    if earliest_date_str is not None:
        earliest_date = datetime.strptime(earliest_date_str, "%d.%m.%Y").date()
    insert_all_truth_posts(interval_days, earliest_date)


@app.command()
def print_all_truth_posts_until_beginning(interval_days: int = 7) -> None:
    print_all_truth_posts(interval_days=interval_days)


def insert_all_truth_posts(interval_days: int = 7, earliest_date: date | None = None) -> None:
    if interval_days <= 0:
        raise ValueError("interval_days must be positive")
    if earliest_date is None:
        earliest_date = date(2022, 3, 1)
    end = date.today()
    while end >= earliest_date:
        start = end - timedelta(days=interval_days - 1)
        if start < earliest_date:
            start = earliest_date
        insert_truth_posts(start.isoformat(), end.isoformat())
        end = start - timedelta(days=1)

def print_all_truth_posts(interval_days: int = 7, earliest_date: date | None = None) -> None:
    if interval_days <= 0:
        raise ValueError("interval_days must be positive")
    if earliest_date is None:
        earliest_date = date(2022, 3, 1)
    end = date.today()
    while end >= earliest_date:
        start = end - timedelta(days=interval_days - 1)
        if start < earliest_date:
            start = earliest_date
        print_truth_headposts(start.isoformat(), end.isoformat())
        end = start - timedelta(days=1)


def print_truth_headposts(start_date: str, end_date: str) -> None:
    feed_xml = _get_xml(start_date, end_date)
    for pub_date, title, description in _extract_items(feed_xml):
        try:
            date_obj = parsedate_to_datetime(pub_date)
            date_str = date_obj.date().isoformat()
        except (TypeError, ValueError):
            date_str = pub_date
        print(f"{date_str} - {title}\n\n {description}\n\n---")


def insert_truth_posts(start_date: str, end_date: str) -> None:
    feed_xml = _get_xml(start_date, end_date)
    for pub_date, title, description in _extract_items(feed_xml):
        try:
            date_obj = parsedate_to_datetime(pub_date)
            date_str = date_obj.date().isoformat()
        except (TypeError, ValueError):
            date_str = pub_date
        mongo.insert("trump", json.dumps([{"date": date_str, "title": title, "description": description}]))


def _get_xml(start_date: str, end_date: str) -> str:
    params = {"start_date": start_date, "end_date": end_date}
    logging.info(f"Retrieving Trump data: {params}")
    try:
        response = requests.get(TRUMP_URL, params=params)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to call {TRUMP_URL}: {e}")
        return ""


def _extract_items(feed_xml: str) -> Iterable[Tuple[str, str, str]]:
    if not feed_xml:
        return []
    try:
        root = ET.fromstring(feed_xml)
    except ET.ParseError:
        return []
    items = []
    for item in root.findall(".//item"):
        title_el = item.find("title")
        description_el = item.find("description")
        pub_date_el = item.find("pubDate")
        if title_el is None or pub_date_el is None:
            continue
        title = (title_el.text or "").strip()
        pub_date = (pub_date_el.text or "").strip()
        description = (description_el.text or "").strip()
        description = _strip_tags(description)
        if title.startswith("[No Title]") or len(description) < 20:
            continue
        items.append((pub_date, title, description))
    return items


def _strip_tags(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text)
