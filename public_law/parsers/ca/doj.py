# pyright: reportUnknownMemberType=false

from datetime import date
import re
from typing import Any, TypeAlias

from scrapy.selector.unified import Selector
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList

from public_law.models.glossary import *
from public_law.text import capitalize_first_char, NonemptyString, normalize_whitespace
from public_law.metadata import Metadata


SelectorLike: TypeAlias = SelectorList | HtmlResponse


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    name = parse_name(html)
    pub_date = first_match(html, "dl#wb-dtmd time::text", "Pub. date")

    entries: list[GlossaryEntry] = []

    match html.css("main dl"):
        case [first, *_] if isinstance(
            first, Selector  # pylint:disable=used-before-assignment
        ):  # pyright: reportUnknownVariableType=false
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

    metadata = Metadata(
        dcterms_source=NonemptyString(url),
        dcterms_title=NonemptyString(name),
        dcterms_language="en",
        dcterms_coverage=NonemptyString("Canada"),
        publiclaw_sourceModified=date.fromisoformat(pub_date),
        publiclaw_sourceCreator=NonemptyString("Department of Justice Canada"),
    )

    return GlossaryParseResult(
        metadata=metadata,
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
