from typing import Iterable, List

from scrapy.http.response.html import HtmlResponse

from typed_soup import from_response, TypedSoup

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject
from ...text import NonemptyString as String
from ...text import (Sentence, ensure_ends_with_period,
                     normalize_nonempty)


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    parsed_entries = tuple(__parse_entries(html))

    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=String(
                "Family, domestic and sexual violence glossary"),
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
                    uri=LoCSubject("sh85047071"),
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
        # Clean up the phrase by removing trailing ": " and creating a NonemptyString
        cleaned_phrase = phrase.rstrip(": ")

        fixed_phrase = String(cleaned_phrase)
        fixed_definition = Sentence(defn)

        yield GlossaryEntry(fixed_phrase, fixed_definition)


def __raw_entries(response: HtmlResponse) -> Iterable[tuple[str, str]]:
    """
    The core of this parser.

    TODO: Refactor all the glossary parsers to need only this function.
    """
    soup = from_response(response)
    paragraphs = soup("p")

    # Get all strong elements from paragraphs that have content
    strongs: List[TypedSoup] = []
    for p in paragraphs:
        strong = p.find("strong")
        if strong is not None and strong.string is not None:
            strongs.append(strong)

    # Filter out "Indigenous" entries
    strongs = [
        s for s in strongs
        if s.string != "Indigenous"
    ]

    # Extract phrase and definition
    for s in strongs:
        phrase = s.string or ""
        definition = s.get_content_after_element()

        yield (phrase, definition)
