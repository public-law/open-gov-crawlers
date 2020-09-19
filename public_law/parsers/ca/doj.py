from typing import List, NamedTuple, Union
from scrapy import Selector
from scrapy.http import Response
from public_law.text import normalize_whitespace


class ParseException(Exception):
    pass


class GlossarySourceParseResult(NamedTuple):
    """All the info about a glossary source"""

    name: str
    source_url: str
    # author: str
    # pub_date: str


def parse_glossary(html: Response) -> GlossarySourceParseResult:
    main = html.css("main")

    name = first(main, "h1::text", "name") + "; " + first(main, "h2::text", "name")

    return GlossarySourceParseResult(name=name, source_url=html.url)


def first(node: Union[Response, Selector], css: str, expected: str) -> str:
    result = node.css(css).get()
    if result is None:
        raise ParseException(f"Could not parse the {expected}")
    return normalize_whitespace(result)
