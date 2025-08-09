import re
from datetime import datetime
from typing import List, NamedTuple, Union, cast

from scrapy.http.response import Response
from scrapy.selector.unified import Selector
from toolz.functoolz import curry, pipe  # type: ignore

from public_law.shared.exceptions.parse_exception import ParseException
from public_law.shared.utils.text import normalize_whitespace

join = curry(str.join)
map  = curry(map)


class CitationSet(NamedTuple):
    """Extendable dict of citations"""

    ocga: List[str]

    def __repr__(self) -> str:
        return self._asdict().__repr__()


class OpinionParseResult(NamedTuple):
    """All the collected data from an opinion page"""

    source_url:  str
    title:       str
    is_official: bool
    date:        str
    summary:     str
    full_text:   str
    citations:   CitationSet


def parse_ag_opinion(html: Response) -> OpinionParseResult:
    summary = first(html, css=".page-top__subtitle--re p::text",   expected="summary")
    title   = first(html, css="h1.page-top__title--opinion::text", expected="title")
    date    = first(html, css="time::text",                        expected="date")
    
    full_text = cast(
        str,
        pipe(
            get_all(html, ".body-content p::text"),
            map(normalize_whitespace),
            join("\n"),
        ),
    )
    
    citations = cast(CitationSet, pipe(
        re.findall(
            r"\d+-\d+-\d+(?:\([-().A-Za-z0-9]*[-A-Za-z0-9]\))?", full_text),
        set,
        sorted,
        CitationSet,
    ))

    return OpinionParseResult(
        summary     = summary,
        title       = title,
        is_official = title.startswith("Official"),
        date        = opinion_date_to_iso8601(date),
        full_text   = full_text,
        source_url  = html.url,
        citations   = citations,
    )


def opinion_date_to_iso8601(date: str) -> str:
    return datetime.strptime(date, "%B %d, %Y").isoformat().split("T")[0]


def get_all(node: Union[Response, Selector], css: str) -> List[str]:
    return node.css(css).getall()


def first(node: Response | Selector, css: str, expected: str) -> str:
    match node.css(css).get():
        case str(result):
            return result
        case _:
            raise ParseException(f"Could not parse the {expected}")
