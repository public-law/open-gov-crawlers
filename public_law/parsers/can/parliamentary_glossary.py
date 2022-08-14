from scrapy.http.response.html import HtmlResponse

from ...metadata import Metadata, Subject
from ...models.glossary import GlossaryEntry, GlossaryParseResult, reading_ease
from ...text import URL, LoCSubject, NonemptyString as String
from ...text import Sentence, ensure_ends_with_period, make_soup, normalize_nonempty


def parse_glossary(html: HtmlResponse) -> GlossaryParseResult:
    # parsed_entries = __parse_entries(html)
    parsed_entries = []

    return GlossaryParseResult(
        metadata=Metadata(
            dcterms_title=String("Glossary of Parliamentary Terms for Intermediate Students"),
            dcterms_language="en",
            dcterms_coverage="USA",
            # Info about original source
            dcterms_source=html.url,  # type: ignore
            publiclaw_sourceModified="unknown",
            publiclaw_sourceCreator=String("United States Courts"),
            publiclaw_readingEase=reading_ease(parsed_entries),
            dcterms_subject=(
                Subject(
                    uri=LoCSubject("sh85033575"),  # type: ignore
                    rdfs_label=String("Courts--United States"),
                ),
                Subject(
                    uri=URL("https://www.wikidata.org/wiki/Q194907"),
                    rdfs_label=String("United States federal courts"),
                ),
            ),
        ),
        entries=parsed_entries,
    )


def __parse_entries(html: HtmlResponse) -> tuple[GlossaryEntry, ...]:
    soup = make_soup(html)
    raw_entries = zip(soup("dt"), soup("dd"))

    return tuple(
        GlossaryEntry(
            phrase=normalize_nonempty(phrase.text),
            definition=Sentence(ensure_ends_with_period(normalize_nonempty(defn.text))),
        )
        for phrase, defn in raw_entries
    )
