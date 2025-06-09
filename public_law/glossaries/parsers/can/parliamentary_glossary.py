from scrapy.http.response.html import HtmlResponse

from public_law.shared.models.metadata import Metadata, Subject
from public_law.glossaries.models.glossary import GlossaryEntry, GlossaryParseResult
from public_law.shared.utils.text import URL, LoCSubject
from public_law.shared.utils.text import NonemptyString as String
from public_law.shared.utils.text import (Sentence, ensure_ends_with_period, make_soup,
                       cleanup, normalize_whitespace)


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    parsed_entries = __parse_entries(html)

    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=String(
                "Glossary of Parliamentary Terms for Intermediate Students"),
            dcterms_language="en",
            dcterms_coverage="CAN",
            # Info about original source
            dcterms_source=String(html.url),
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("Parliament of Canada"),
            dcterms_subject=(
                Subject(
                    uri=LoCSubject("sh85075807"),
                    rdfs_label=String("Legislative bodies"),
                ),
                Subject(
                    uri=URL("https://www.wikidata.org/wiki/Q35749"),
                    rdfs_label=String("Parliament"),
                ),
            ),
        ),
        entries=parsed_entries,
    )


def __parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    soup = make_soup(html)

    # Skip the "Committees" entry.
    terms = [t for t in soup("dt") if t.text != 'Committees']

    # Fix the "Usher..." entry.
    raw_phrases = [t.text for t in terms]
    phrases = ["Usher of the Black Rod" if p.startswith(
        "Usher") else p for p in raw_phrases]

    raw_entries = zip(phrases, soup("dd"))

    return tuple(
        GlossaryEntry(
            phrase=String(normalize_whitespace(phrase)),
            definition=Sentence(defn.text),
        )
        for phrase, defn in raw_entries
    )
