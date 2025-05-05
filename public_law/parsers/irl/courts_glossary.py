from typing import Any, Iterable

from more_itertools import chunked
from scrapy.http.response.html import HtmlResponse
from toolz.functoolz import pipe  # type: ignore

from public_law import text

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject
from ...text import NonemptyString as String
from ...text import Sentence, WikidataTopic


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    """
    The top-level, public function of this module. It performs the
    complete parse of the HTTP response.
    """
    metadata = _make_metadata(html)
    entries  = _parse_entries(html)

    return GlossaryParseResult(metadata, entries)


def _make_metadata(html: HtmlResponse) -> Metadata:
    source_url = URL(html.url)
    subjects = (
                Subject(LoCSubject("sh85033571"), String("Courts")),
                Subject(WikidataTopic("Q41487"),  String("Court")),
            )
    
    return Metadata(
            dcterms_title=String("Glossary of Legal Terms"),
            dcterms_language="en",
            dcterms_coverage="IRL",
            # Info about original source
            dcterms_source=source_url,
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("The Courts Service of Ireland"),
            dcterms_subject=subjects,
        )


def _parse_entries(html: HtmlResponse) -> Iterable[GlossaryEntry]:
    """
    TODO: Refactor into a parent class. Write a way to pass lists of
    functions for cleaning up the definitions and phrases.
    """

    def cleanup_definition(definition: str) -> Sentence:
        return pipe(
            definition
            , text.normalize_nonempty
            , text.lstrip(":")                                              # type: ignore
            , text.ensure_ends_with_period
            , text.normalize_nonempty
            , text.capitalize_first_char
            , Sentence
        )

    def cleanup_phrase(phrase: str) -> String:
        return text.pipe(
            phrase
            , text.rstrip(":")                                             # type: ignore
            , text.normalize_nonempty
        )

    for phrase, defn in _raw_entries(html):
        yield GlossaryEntry(
            phrase=cleanup_phrase(phrase),
            definition=cleanup_definition(defn),
        )


def _raw_entries(html: HtmlResponse) -> Iterable[tuple[Any, Any]]:
    """
    The core of this parser.

    TODO: Refactor all the glossary parsers to need only this function.
    """
    return chunked(
        html.xpath("//p/strong/parent::p/text() | //strong/text()").getall(), 2  # type: ignore
    )
