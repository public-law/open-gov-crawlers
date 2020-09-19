from typing import List, NamedTuple, Union
from scrapy import Selector
from scrapy.http import Response
from public_law.text import normalize_whitespace


class ParseException(Exception):
    pass


class GlossarySourceParseResult(NamedTuple):
    """All the info about a glossary source"""

    name: str


def parse_glossary(html: Response) -> GlossarySourceParseResult:
    name = html.css("h1::text").get()
    return GlossarySourceParseResult(name=name)


# def first(node: Union[Response, Selector], css: str, expected: str) -> str:
#     result = node.css(css).get()
#     if result is None:
#         raise ParseException(f"Could not parse the {expected}")
#     return normalize_whitespace(result)
