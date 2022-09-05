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
            dcterms_title=String("Family, domestic and sexual violence glossary"),
            dcterms_language="en",
            dcterms_coverage="AUS",
            # Info about original source
            dcterms_source=String(
                "https://www.aihw.gov.au/reports-data/behaviours-risk-factors/domestic-violence/glossary"
            ),
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String(
                "Australian Institute of Health and Welfare"
            ),
            dcterms_subject=(
                Subject(
                    uri=LoCSubject("sh85047071"),  # type: ignore
                    rdfs_label=String("Family violence"),
                ),
                Subject(
                    uri=URL("https://www.wikidata.org/wiki/Q156537"),
                    rdfs_label=String("Domestic violence"),
                ),
            ),
        ),
        entries=parsed_entries,
    )


def __parse_entries(html: HtmlResponse) -> Iterable[GlossaryEntry]:
    """TODO: Refactor into a parent class"""

    for phrase, defn in __raw_entries(html):
        fixed_phrase: String = pipe(phrase, rstrip(": "), String)  # type: ignore

        fixed_definition: Sentence = pipe(
            defn, ensure_ends_with_period, normalize_nonempty, Sentence
        )

        yield GlossaryEntry(fixed_phrase, fixed_definition)


def __raw_entries(response: HtmlResponse) -> Iterable[tuple[Any, Any]]:
    """
    The core of this parser.

    TODO: Refactor all the glossary parsers to need only this function.
    """
    soup = make_soup(response)

    paragraphs = soup.find_all("p")
    strongs = filter(lambda s: s is not None, (p.strong for p in paragraphs))
    strongs = filter(lambda s: s.string != "Indigenous", strongs)  # type: ignore

    return ((phrase.string, "".join(map(str, phrase.next_siblings))) for phrase in strongs)  # type: ignore
