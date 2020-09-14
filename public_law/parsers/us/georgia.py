from datetime import datetime
import re
from typing import List, NamedTuple, Union
from scrapy import Selector
from scrapy.http import Response

from public_law.text import normalize_whitespace


class ParseException(Exception):
    pass


class CitationSet(NamedTuple):
    """Extendable dict of citations"""

    ocga: List[str]

    def __repr__(self) -> str:
        return self._asdict().__repr__()


class OpinionParseResult(NamedTuple):
    """All the collected data from an opinion page"""

    source_url: str
    title: str
    is_official: bool
    date: str
    summary: str
    full_text: str
    citations: CitationSet


def parse_ag_opinion(html: Response) -> OpinionParseResult:
    summary = _parse(html, css=".page-top__subtitle--re p::text", expected="summary")
    title = _parse(html, css="h1.page-top__title--opinion::text", expected="title")
    date = _parse(html, css="time::text", expected="date")

    paragraphs = [
        normalize_whitespace(p) for p in html.css(".body-content p::text").getall()
    ]
    full_text = "\n".join(paragraphs)

    citations = re.findall(
        r"\d+-\d+-\d+(?:\([-().A-Za-z0-9]*[-A-Za-z0-9]\))?", full_text
    )
    citation_set = list(set(citations))
    citation_set.sort()

    return OpinionParseResult(
        summary=summary,
        title=title,
        is_official=title.startswith("Official"),
        date=opinion_date_to_iso8601(date),
        full_text=full_text,
        source_url=html.url,
        citations=CitationSet(ocga=citation_set),
    )


def opinion_date_to_iso8601(date: str) -> str:
    return datetime.strptime(date, "%B %d, %Y").isoformat().split("T")[0]


def _parse(node: Union[Response, Selector], css: str, expected: str) -> str:
    result = node.css(css).get()
    if result is None:
        raise ParseException(f"Could not parse the {expected}")
    return normalize_whitespace(result)
