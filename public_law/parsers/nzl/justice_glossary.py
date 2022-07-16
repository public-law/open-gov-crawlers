from typing import Any, Iterable

from scrapy.http.response.html import HtmlResponse

from ...metadata import Metadata
from ...models.glossary import GlossaryEntry, GlossaryParseResult, reading_ease
from ...text import NonemptyString as String
from ...text import Sentence, ensure_ends_with_period, make_soup, normalize_nonempty


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    parsed_entries = tuple(__parse_entries(html))

    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=String("Glossary"),
            dcterms_language="en",
            dcterms_coverage="NZL",
            # Info about original source
            dcterms_source=String("https://www.justice.govt.nz/about/glossary/"),
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("New Zealand Ministry of Justice"),
            publiclaw_readingEase=reading_ease(parsed_entries),
        ),
        entries=parsed_entries,
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
