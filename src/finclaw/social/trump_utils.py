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

@app.command(name="print-all-truth-posts")
def print_all_truth_posts_cmd(interval_days: int = 7, earliest_date: str | None = None) -> None:
    earliest_date_obj = None
    if earliest_date is not None:
        earliest_date_obj = datetime.strptime(earliest_date, "%d.%m.%Y").date()
    print_all_truth_posts(interval_days, earliest_date_obj)


@app.command(name="insert-all-truth-posts")
def insert_all_truth_posts_cmd(interval_days: int = 7, earliest_date: str | None = None) -> None:
    earliest_date_obj = None
    if earliest_date is not None:
        earliest_date_obj = datetime.strptime(earliest_date, "%d.%m.%Y").date()
    insert_all_truth_posts(interval_days, earliest_date_obj)


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
        print_truth_posts(start.isoformat(), end.isoformat())
        end = start - timedelta(days=1)


def print_truth_posts(start_date: str, end_date: str) -> None:
    feed_xml = _get_xml(start_date, end_date)
    for pub_date, title in _extract_items(feed_xml):
        print(f"{pub_date} - {title}\n---")


def insert_truth_posts(start_date: str, end_date: str) -> None:
    feed_xml = _get_xml(start_date, end_date)
    for pub_date, title in _extract_items(feed_xml):
        dt = parsedate_to_datetime(pub_date)
        mongo.insert("trump", json.dumps([{"date": dt.strftime("%Y-%m-%dT%H:%M:%S.000Z"), "title": title}]))


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
        pub_date_el = item.find("pubDate")
        if title_el is None or pub_date_el is None:
            continue
        title = (title_el.text or "").strip()
        pub_date = (pub_date_el.text or "").strip()
        if title.startswith("[No Title]") or len(title) < 20:
            continue
        items.append((pub_date, title))
    return items


def _strip_tags(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text)
