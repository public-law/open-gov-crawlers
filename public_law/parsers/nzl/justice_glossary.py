from typing import Any, Iterable, cast

from bs4 import Tag
from bs4.element import NavigableString
from scrapy.http.response.html import HtmlResponse
from toolz.functoolz import pipe  # type: ignore

from public_law import text

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject
from ...text import NonemptyString as String
from ...text import (Sentence, ensure_ends_with_period, make_soup,
                     normalize_nonempty)
from ...html import parse_html, TypedSoup
from ...result import Result, Ok, Err, cat_oks


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    parsed_entries = tuple(__parse_entries(html))

    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=String("Glossary"),
            dcterms_language="en",
            dcterms_coverage="NZL",
            # Info about original source
            dcterms_source=String(
                "https://www.justice.govt.nz/about/glossary/"),
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("New Zealand Ministry of Justice"),
            dcterms_subject=(
                Subject(
                    uri=LoCSubject("sh85071120"),
                    rdfs_label=String("Justice, Administration of"),
                ),
                Subject(
                    uri=URL("https://www.wikidata.org/wiki/Q16514399"),
                    rdfs_label=String("Administration of justice"),
                ),
            ),
        ),
        entries=parsed_entries,
    )


def __parse_entries(html: HtmlResponse) -> Iterable[GlossaryEntry]:
    """TODO: Refactor into a parent class"""

    for phrase, defn in __raw_entries(html):
        yield GlossaryEntry(
            phrase=normalize_nonempty(phrase.text),
            definition=Sentence(normalize_nonempty(
                ensure_ends_with_period(defn.text))),
        )


def __raw_entries(response: HtmlResponse) -> Iterable[tuple[Any, Any]]:
    """
    The core of this parser.

    TODO: Refactor all the glossary parsers to need only this function.
    """
    soup = make_soup(response)

    def get_next_sibling(tag: Tag) -> Tag | None:
        if not tag.parent:
            return None
        sibling = tag.parent.next_sibling
        if isinstance(sibling, Tag):
            return sibling
        return None

    return ((phrase, get_next_sibling(phrase))
            for phrase in soup.find_all("strong")
            if isinstance(phrase, Tag))
