from typing import Any, Iterable, cast

from more_itertools import chunked
from scrapy.http.response.html import HtmlResponse
from toolz.functoolz import pipe  # type: ignore

from ...flipped import lstrip, rstrip
from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult, reading_ease
from ...text import URL, LoCSubject, NonemptyString as String, WikidataTopic
from ...text import (
    Sentence,
    capitalize_first_char,
    ensure_ends_with_period,
    normalize_nonempty,
)


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    entries = tuple(_parse_entries(html))

    subject = (
                Subject(
                    uri=LoCSubject("sh85033571"),  # type: ignore
                    rdfs_label=String("Courts"),
                ),
                Subject(
                    uri=WikidataTopic("Q41487"),   # type: ignore
                    rdfs_label=String("Court"),
                ),
            )

    metadata = Metadata(
            dcterms_title=String("Glossary of Legal Terms"),
            dcterms_language="en",
            dcterms_coverage="IRL",
            # Info about original source
            dcterms_source=String(cast(str, html.url)),  # type: ignore
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("The Courts Service of Ireland"),
            publiclaw_readingEase=reading_ease(entries),
            dcterms_subject=subject,
        )

    return GlossaryParseResult(metadata, entries)


def _parse_entries(html: HtmlResponse) -> Iterable[GlossaryEntry]:
    """TODO: Refactor into a parent class"""

    def cleanup_defn(defn: str) -> Sentence:
        return pipe(
            defn,
            normalize_nonempty,
            lstrip(":"),  # type: ignore
            ensure_ends_with_period,
            normalize_nonempty,
            capitalize_first_char,
            Sentence,
        )

    def cleanup_phrase(phrase: str) -> String:
        return pipe(
            phrase,
            rstrip(":"),  # type: ignore
            normalize_nonempty,
            String,
        )

    for phrase, defn in _raw_entries(html):
        yield GlossaryEntry(
            phrase=cleanup_phrase(phrase),
            definition=cleanup_defn(defn),
        )


def _raw_entries(html: HtmlResponse) -> Iterable[tuple[Any, Any]]:
    """
    The core of this parser.

    TODO: Refactor all the glossary parsers to need only this function.
    """
    return chunked(
        html.xpath("//p/strong/parent::p/text() | //strong/text()").getall(), 2  # type: ignore
    )
