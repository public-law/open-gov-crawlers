# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportGeneralTypeIssues=false

from typing import Any, Iterable, cast
from more_itertools import chunked

from scrapy.http.response.html import HtmlResponse

from ...text import (
    capitalize_first_char,
    ensure_ends_with_period,
    NonemptyString as NS,
    normalize_nonempty,
    Sentence,
)
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...metadata import Metadata


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=NS("Glossary of Legal Terms"),
            dcterms_language="en",
            dcterms_coverage="IRL",
            # Info about original source
            dcterms_source=NS(cast(str, html.url)),
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=NS("The Courts Service of Ireland"),
        ),
        entries=__parse_entries(html),
    )


def __parse_entries(html: HtmlResponse) -> Iterable[GlossaryEntry]:
    """TODO: Refactor into a parent class"""

    for phrase, defn in __raw_entries(html):
        yield GlossaryEntry(
            phrase=normalize_nonempty(phrase),
            definition=Sentence(
                capitalize_first_char(
                    ensure_ends_with_period(normalize_nonempty((defn)))
                )
            ),
        )


def __raw_entries(html: HtmlResponse) -> Iterable[tuple[Any, Any]]:
    """
    The core of this parser.

    TODO: Refactor all the glossary parsers to need only this function.
    """
    return chunked(
        html.xpath("//p/strong/parent::p/text() | //strong/text()").getall(), 2
    )
