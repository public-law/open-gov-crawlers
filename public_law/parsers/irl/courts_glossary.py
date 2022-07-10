# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportGeneralTypeIssues=false

from typing import Any, Iterable, cast

from more_itertools import chunked
from scrapy.http.response.html import HtmlResponse
from toolz.functoolz import pipe

from ...flipped import lstrip, rstrip
from ...metadata import Metadata
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import NonemptyString as String
from ...text import (
    Sentence,
    capitalize_first_char,
    ensure_ends_with_period,
    normalize_nonempty,
)


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=String("Glossary of Legal Terms"),
            dcterms_language="en",
            dcterms_coverage="IRL",
            # Info about original source
            dcterms_source=String(cast(str, html.url)),
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("The Courts Service of Ireland"),
        ),
        entries=__parse_entries(html),
    )


def __parse_entries(html: HtmlResponse) -> Iterable[GlossaryEntry]:
    """TODO: Refactor into a parent class"""

    def cleanup_defn(defn: str) -> Sentence:
        return pipe(
            defn,
            normalize_nonempty,
            lstrip(":"),
            ensure_ends_with_period,
            normalize_nonempty,
            capitalize_first_char,
            Sentence,
        )

    def cleanup_phrase(phrase: str) -> String:
        return pipe(
            phrase,
            rstrip(":"),
            normalize_nonempty,
            String,
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
