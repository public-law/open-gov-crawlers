# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportGeneralTypeIssues=false

from typing import Any, Iterable, cast
from more_itertools import chunked
from toolz.functoolz import pipe

from scrapy.http.response.html import HtmlResponse

from ...text import (
    capitalize_first_char,
    ensure_ends_with_period,
    NonemptyString as NS,
    normalize_nonempty,
    remove_beginning_colon,
    remove_end_colon,
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

    def cleanup_defn(defn: str) -> Sentence:
        return pipe(
            defn,
            normalize_nonempty,
            remove_beginning_colon,
            ensure_ends_with_period,
            normalize_nonempty,
            capitalize_first_char,
            Sentence,
        )

    def cleanup_phrase(phrase: str) -> NS:
        return pipe(
            phrase,
            remove_end_colon,
            normalize_nonempty,
            NS,
        )

    for phrase, defn in __raw_entries(html):
        yield GlossaryEntry(
            phrase=cleanup_phrase(phrase),
            definition=cleanup_defn(defn),
        )


def __raw_entries(html: HtmlResponse) -> Iterable[tuple[Any, Any]]:
    """
    The core of this parser.

    TODO: Refactor all the glossary parsers to need only this function.
    """
    return chunked(
        html.xpath("//p/strong/parent::p/text() | //strong/text()").getall(), 2
    )
