from typing import Any, Iterable
from scrapy.http.response.html import HtmlResponse

from ...text import (
    ensure_ends_with_period,
    NonemptyString as NS,
    make_soup,
    normalize_nonempty,
    Sentence,
)
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...metadata import Metadata


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=NS("Glossary"),
            dcterms_language="en",
            dcterms_coverage=NS("NZL"),
            # Info about original source
            dcterms_source=NS("https://www.justice.govt.nz/about/glossary/"),
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=NS("New Zealand Ministry of Justice"),
        ),
        entries=__parse_entries(html),
    )


def __parse_entries(html: HtmlResponse) -> Iterable[GlossaryEntry]:
    """TODO: Refactor into a parent class"""

    for phrase, defn in __raw_entries(html):
        yield GlossaryEntry(
            phrase=normalize_nonempty(phrase.text),
            definition=Sentence(normalize_nonempty(ensure_ends_with_period(defn.text))),
        )


def __raw_entries(html: HtmlResponse) -> Iterable[tuple[Any, Any]]:
    """
    The core of this parser.

    TODO: Refactor all the glossary parsers to need only this function.
    """
    soup = make_soup(html)
    return ((phrase, phrase.parent.next_sibling) for phrase in soup.find_all("strong"))
