from typing import Any, Iterable
from toolz.functoolz import pipe  # type: ignore
from public_law.flipped import rstrip
from scrapy.http.response.html import HtmlResponse

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject, NonemptyString as String
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
            dcterms_subject=(
                Subject(
                    uri=LoCSubject("sh85071120"),  # type: ignore
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
        fixed_phrase: String = pipe(
            phrase.text,
            rstrip(':'),  # type: ignore
            normalize_nonempty
        )
        
        yield GlossaryEntry(
            phrase=fixed_phrase,
            definition=Sentence(normalize_nonempty(ensure_ends_with_period(defn.text))),
        )


def __raw_entries(html: HtmlResponse) -> Iterable[tuple[Any, Any]]:
    """
    The core of this parser.

    TODO: Refactor all the glossary parsers to need only this function.
    """
    soup = make_soup(html)
    return ((phrase, phrase.parent.next_sibling) for phrase in soup.find_all("strong"))
