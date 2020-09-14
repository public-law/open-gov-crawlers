from datetime import datetime
from typing import NamedTuple, Union
from public_law.text import normalize_whitespace

from scrapy import Selector
from scrapy.http import Response


class ParseException(Exception):
    pass


class OpinionParseResult(NamedTuple):
    """All the collected data from an opinion page"""

    title: str
    is_official: bool
    date: str
    summary: str


def parse_ag_opinion(html: Union[Response, Selector]) -> OpinionParseResult:
    summary = _parse(html, css=".page-top__subtitle--re p::text", expected="summary")
    title = _parse(html, css="h1.page-top__title--opinion::text", expected="title")
    date = _parse(html, css="time::text", expected="date")

    return OpinionParseResult(
        summary=summary,
        title=title,
        is_official=title.startswith("Official"),
        date=opinion_date_to_iso8601(date),
    )


def opinion_date_to_iso8601(date: str) -> str:
    return datetime.strptime(date, "%B %d, %Y").isoformat().split("T")[0]


def _parse(node: Union[Response, Selector], css: str, expected: str) -> str:
    result = node.css(css).get()
    if result is None:
        raise ParseException(f"Could not parse the {expected}")
    return normalize_whitespace(result)
