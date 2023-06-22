from scrapy.http.response.html import HtmlResponse

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult
from ...text import URL, LoCSubject, NonemptyString as String, normalize_whitespace
from ...text import Sentence, ensure_ends_with_period, make_soup, normalize_nonempty


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    parsed_entries = __parse_entries(html)

    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=String("Glossary of Parliamentary Terms for Intermediate Students"),
            dcterms_language="en",
            dcterms_coverage="CAN",
            # Info about original source
            dcterms_source=html.url,
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
    phrases = ["Usher of the Black Rod" if p.startswith("Usher") else p for p in raw_phrases]

    raw_entries = zip(phrases, soup("dd"))

    return tuple(
        GlossaryEntry(
            phrase=String(normalize_whitespace(phrase)),
            definition=Sentence(ensure_ends_with_period(normalize_nonempty(defn.text)).strip("> ")),
        )
        for phrase, defn in raw_entries
    )
