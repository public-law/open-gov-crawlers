# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false

import re
from typing import Any, NamedTuple, TypeAlias

from scrapy.selector.unified import Selector
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

from public_law.text import capitalize_first_char, NonemptyString, normalize_whitespace
from public_law.dates import todays_date


SelectorLike: TypeAlias = SelectorList | HtmlResponse


class ParseException(Exception):
    pass


class GlossaryEntry(NamedTuple):
    """Represents one term and its definition in a particular Glossary"""

    phrase: NonemptyString
    definition: NonemptyString

    def __repr__(self) -> str:
        return self._asdict().__repr__()


class GlossarySourceParseResult(NamedTuple):
    """All the info about a glossary source"""

    source_url: str
    name: str
    author: str
    pub_date: str
    scrape_date: str
    entries: list[GlossaryEntry]


def parse_glossary(html: HtmlResponse) -> GlossarySourceParseResult:
    name = parse_name(html)
    pub_date = first_match(html, "dl#wb-dtmd time::text", "Pub. date")

    entries: list[GlossaryEntry] = []

    # dl_lists: list[Any] = html.css("main dl")
    # if len(dl_lists) == 0:
    #     raise ParseException("No DL lists found")

    # if isinstance(dl_lists[0], Selector):
    #     first_dl_list = dl_lists[0]
    # else:
    #     raise ParseException("Expected a <dl>")

    match html.css("main dl"):
        case [first, *_] if isinstance(first, Selector):
            first_dl_list = first
        case _:
            raise ParseException("Expected a <dl>")

    prop: Any
    for prop in first_dl_list.xpath("dt"):
        assert isinstance(prop, Selector)

        match prop.xpath("./following-sibling::dd").get():
            case str(result):
                # Get the inner text and preserve inner HTML.
                definition = capitalize_first_char(
                    (result.replace("<dd>", "").replace("</dd>", "").replace("  ", " "))
                )
            case _:
                raise ParseException("Could not parse the definition")

        match prop.xpath("normalize-space(descendant::text())").get():
            case str(result):
                phrase = re.sub(r":$", "", result)
            case _:
                raise ParseException("Could not parse the phrase")

        entries.append(
            GlossaryEntry(
                phrase=NonemptyString(phrase),
                definition=NonemptyString(definition),
            )
        )

    url: str = html.url

    return GlossarySourceParseResult(
        source_url=url,
        name=name,
        author="Department of Justice Canada",
        pub_date=pub_date,
        scrape_date=todays_date(),
        entries=entries,
    )


def parse_name(html: SelectorLike) -> str:
    return first_match(html, "title::text", "name")


def first_match(node: SelectorLike, css: str, expected: str) -> str:
    match node.css(css).get():
        case str(result):
            return normalize_whitespace(result)
        case _:
            raise ParseException(f'Could not parse the {expected} using "{css}"')
